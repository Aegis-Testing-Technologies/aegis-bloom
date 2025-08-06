"""Bloom filter implementation for copyright compliance checking."""

import gzip
import hashlib
import json
import logging
from pathlib import Path
from typing import List, Optional, Union

logger = logging.getLogger(__name__)

# Import Rust bindings when available
try:
    from .aegis_bloom import (
        create_bloom_filter,
        add_to_bloom,
        check_bloom,
        save_bloom,
        load_bloom,
    )
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False
    logger.warning("Rust extensions not available, using pure Python fallback")


class BloomFilter:
    """Bloom filter for copyright compliance checking.
    
    This class provides a simple interface for building and querying
    bloom filters to check if content appears in a training dataset.
    """
    
    def __init__(
        self,
        expected_items: int = 10_000_000,
        false_positive_rate: float = 0.01,
        chunk_size: int = 512,
        consecutive_chunks: int = 3,
    ):
        """Initialize a new bloom filter.
        
        Args:
            expected_items: Expected number of chunks to be added
            false_positive_rate: Target false positive rate (default 1%)
            chunk_size: Size of text chunks in bytes (default 512)
            consecutive_chunks: Number of consecutive chunks required for MAYBE_PRESENT
        """
        self.expected_items = expected_items
        self.false_positive_rate = false_positive_rate
        self.chunk_size = chunk_size
        self.consecutive_chunks = consecutive_chunks
        
        if RUST_AVAILABLE:
            self._filter = create_bloom_filter(expected_items, false_positive_rate)
        else:
            # Fallback to pure Python implementation
            self._filter = self._create_python_filter(expected_items, false_positive_rate)
        
        self.metadata = {
            "expected_items": expected_items,
            "false_positive_rate": false_positive_rate,
            "chunk_size": chunk_size,
            "consecutive_chunks": consecutive_chunks,
            "items_added": 0,
        }
    
    @classmethod
    def from_directory(
        cls,
        directory: Union[str, Path],
        chunk_size: int = 512,
        **kwargs
    ) -> "BloomFilter":
        """Create a bloom filter from all text files in a directory.
        
        Args:
            directory: Path to directory containing text files
            chunk_size: Size of text chunks in bytes
            **kwargs: Additional arguments for BloomFilter constructor
            
        Returns:
            BloomFilter containing all text from the directory
        """
        directory = Path(directory)
        if not directory.exists():
            raise ValueError(f"Directory does not exist: {directory}")
        
        # Count files to estimate expected items
        text_files = list(directory.glob("**/*.txt")) + list(directory.glob("**/*.md"))
        
        # Estimate chunks based on file sizes
        total_size = sum(f.stat().st_size for f in text_files if f.is_file())
        expected_chunks = (total_size // chunk_size) * 2  # Overestimate for overlapping
        
        bloom = cls(expected_items=expected_chunks, chunk_size=chunk_size, **kwargs)
        
        for file_path in text_files:
            try:
                bloom.add_file(file_path)
                logger.debug(f"Added file to bloom filter: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to add file {file_path}: {e}")
        
        logger.info(f"Created bloom filter from {len(text_files)} files")
        return bloom
    
    def add(self, text: str):
        """Add text to the bloom filter.
        
        Args:
            text: Text to add to the filter
        """
        chunks = self._chunk_text(text)
        
        if RUST_AVAILABLE:
            for chunk in chunks:
                add_to_bloom(self._filter, chunk)
        else:
            for chunk in chunks:
                self._add_python(chunk)
        
        self.metadata["items_added"] += len(chunks)
    
    def add_file(self, file_path: Union[str, Path]):
        """Add contents of a file to the bloom filter.
        
        Args:
            file_path: Path to file to add
        """
        file_path = Path(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                # Process file in chunks to handle large files
                while True:
                    chunk = f.read(1024 * 1024)  # Read 1MB at a time
                    if not chunk:
                        break
                    self.add(chunk)
        except Exception as e:
            raise IOError(f"Failed to read file {file_path}: {e}")
    
    def check(self, text: str) -> str:
        """Check if text appears in the bloom filter.
        
        Args:
            text: Text to check
            
        Returns:
            "MAYBE_PRESENT" if text might be in the dataset,
            "NOT_PRESENT" if text is definitely not in the dataset
        """
        chunks = self._chunk_text(text)
        
        if len(chunks) < self.consecutive_chunks:
            return "NOT_PRESENT"
        
        consecutive_hits = 0
        
        for chunk in chunks:
            if RUST_AVAILABLE:
                is_present = check_bloom(self._filter, chunk)
            else:
                is_present = self._check_python(chunk)
            
            if is_present:
                consecutive_hits += 1
                if consecutive_hits >= self.consecutive_chunks:
                    return "MAYBE_PRESENT"
            else:
                consecutive_hits = 0
        
        return "NOT_PRESENT"
    
    def check_file(self, file_path: Union[str, Path]) -> str:
        """Check if a file's contents appear in the bloom filter.
        
        Args:
            file_path: Path to file to check
            
        Returns:
            "MAYBE_PRESENT" or "NOT_PRESENT"
        """
        file_path = Path(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            return self.check(text)
        except Exception as e:
            raise IOError(f"Failed to read file {file_path}: {e}")
    
    def save(self, file_path: Union[str, Path]):
        """Save bloom filter to a compressed file.
        
        Args:
            file_path: Path to save the bloom filter
        """
        file_path = Path(file_path)
        
        if RUST_AVAILABLE:
            # Use Rust serialization
            data = save_bloom(self._filter)
        else:
            # Use Python serialization
            data = self._save_python()
        
        # Add metadata
        full_data = {
            "metadata": self.metadata,
            "filter_data": data.hex() if isinstance(data, bytes) else data,
        }
        
        # Compress and save
        with gzip.open(file_path, 'wt', encoding='utf-8') as f:
            json.dump(full_data, f)
        
        logger.info(f"Saved bloom filter to {file_path} ({file_path.stat().st_size} bytes)")
    
    @classmethod
    def load(cls, file_path: Union[str, Path]) -> "BloomFilter":
        """Load bloom filter from a file.
        
        Args:
            file_path: Path to bloom filter file
            
        Returns:
            Loaded BloomFilter instance
        """
        file_path = Path(file_path)
        
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            full_data = json.load(f)
        
        metadata = full_data["metadata"]
        filter_data = full_data["filter_data"]
        
        # Create new bloom filter with same parameters
        bloom = cls(
            expected_items=metadata["expected_items"],
            false_positive_rate=metadata["false_positive_rate"],
            chunk_size=metadata["chunk_size"],
            consecutive_chunks=metadata["consecutive_chunks"],
        )
        
        if RUST_AVAILABLE:
            # Load Rust filter
            bloom._filter = load_bloom(bytes.fromhex(filter_data))
        else:
            # Load Python filter
            bloom._filter = bloom._load_python(filter_data)
        
        bloom.metadata = metadata
        
        logger.info(f"Loaded bloom filter from {file_path}")
        return bloom
    
    def _chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        chunks = []
        overlap = self.chunk_size // 2  # 50% overlap
        
        for i in range(0, len(text), overlap):
            chunk = text[i:i + self.chunk_size]
            if len(chunk) >= 32:  # Minimum chunk size
                # Hash chunk for consistency
                chunk_hash = hashlib.sha256(chunk.encode('utf-8')).hexdigest()
                chunks.append(chunk_hash)
        
        return chunks
    
    def _create_python_filter(self, expected_items: int, false_positive_rate: float):
        """Create a pure Python bloom filter fallback."""
        # Simple bit array implementation
        import math
        
        # Calculate optimal size and hash functions
        size = int(-expected_items * math.log(false_positive_rate) / (math.log(2) ** 2))
        hash_count = int(size * math.log(2) / expected_items)
        
        return {
            'size': size,
            'hash_count': hash_count,
            'bits': [0] * size,
        }
    
    def _add_python(self, item: str):
        """Add item to Python bloom filter."""
        for i in range(self._filter['hash_count']):
            # Simple hash function
            hash_val = hash(f"{item}:{i}") % self._filter['size']
            self._filter['bits'][hash_val] = 1
    
    def _check_python(self, item: str) -> bool:
        """Check item in Python bloom filter."""
        for i in range(self._filter['hash_count']):
            hash_val = hash(f"{item}:{i}") % self._filter['size']
            if self._filter['bits'][hash_val] == 0:
                return False
        return True
    
    def _save_python(self):
        """Save Python bloom filter."""
        return {
            'size': self._filter['size'],
            'hash_count': self._filter['hash_count'],
            'bits': self._filter['bits'],
        }
    
    def _load_python(self, data):
        """Load Python bloom filter."""
        return data
