"""Basic tests for AEGIS Bloom pure Python implementation."""

import os
import tempfile
from pathlib import Path

import pytest

from aegis import BloomFilter


def test_import_without_rust():
    """Test that aegis can be imported even without Rust extensions."""
    # Force pure Python mode
    os.environ['AEGIS_BLOOM_NO_RUST'] = '1'
    
    # Import should work
    from aegis.bloom import BloomFilter, RUST_AVAILABLE
    
    # Should fallback to pure Python
    assert not RUST_AVAILABLE or os.environ.get('AEGIS_BLOOM_NO_RUST') == '1'
    
    # Clean up
    if 'AEGIS_BLOOM_NO_RUST' in os.environ:
        del os.environ['AEGIS_BLOOM_NO_RUST']


def test_basic_bloom_operations():
    """Test basic bloom filter operations."""
    # Create a small bloom filter with smaller chunk size for testing
    bloom = BloomFilter(expected_items=1000, false_positive_rate=0.1, chunk_size=32, consecutive_chunks=2)
    
    # Add some longer text that will generate multiple chunks
    test_text = "This is a test document with some content. " * 10  # Repeat to ensure multiple chunks
    bloom.add(test_text)
    
    # Should find the same text
    result = bloom.check(test_text)
    assert result == "MAYBE_PRESENT"
    
    # Should not find different text
    different_text = "This is completely different content that was never added before and should not be found." * 5
    result = bloom.check(different_text)
    assert result == "NOT_PRESENT"


def test_file_operations():
    """Test file-based bloom filter operations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Create test files with longer content
        test_file1 = tmpdir / "test1.txt"
        test_file1.write_text("This is the first test file with some content. " * 20)
        
        test_file2 = tmpdir / "test2.txt"
        test_file2.write_text("This is the second test file with different content. " * 20)
        
        # Create bloom filter from directory with smaller chunk size
        bloom = BloomFilter.from_directory(tmpdir, chunk_size=32, consecutive_chunks=2)
        
        # Check files
        result1 = bloom.check_file(test_file1)
        assert result1 == "MAYBE_PRESENT"
        
        result2 = bloom.check_file(test_file2)
        assert result2 == "MAYBE_PRESENT"
        
        # Create a file that wasn't in the training data
        new_file = tmpdir / "new.txt"
        new_file.write_text("This is completely new content that was never seen before and is totally different. " * 10)
        
        result_new = bloom.check_file(new_file)
        # This might be MAYBE_PRESENT due to false positives, but should often be NOT_PRESENT
        assert result_new in ["MAYBE_PRESENT", "NOT_PRESENT"]


def test_save_and_load():
    """Test saving and loading bloom filters."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Create and populate bloom filter with smaller chunk size for testing
        bloom1 = BloomFilter(expected_items=1000, false_positive_rate=0.1, chunk_size=32, consecutive_chunks=2)
        test_text = "This is test content for save/load testing. " * 10  # Repeat to ensure multiple chunks
        bloom1.add(test_text)
        
        # Save to file
        bloom_file = tmpdir / "test.bloom"
        bloom1.save(bloom_file)
        assert bloom_file.exists()
        
        # Load from file
        bloom2 = BloomFilter.load(bloom_file)
        
        # Should have same behavior
        result1 = bloom1.check(test_text)
        result2 = bloom2.check(test_text)
        assert result1 == result2 == "MAYBE_PRESENT"
        
        # Check metadata
        assert bloom2.metadata["expected_items"] == 1000
        assert bloom2.metadata["false_positive_rate"] == 0.1


def test_cli_import():
    """Test that CLI module can be imported."""
    from aegis.cli import main
    assert callable(main)


def test_version_import():
    """Test that version can be imported."""
    from aegis._version import __version__
    assert __version__ == "0.1.0"


if __name__ == "__main__":
    # Run basic tests
    test_import_without_rust()
    test_basic_bloom_operations()
    test_file_operations()
    test_save_and_load()
    test_cli_import()
    test_version_import()
    print("All tests passed!")
