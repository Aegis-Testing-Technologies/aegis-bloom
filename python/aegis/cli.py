"""Command-line interface for AEGIS Bloom."""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional

from .bloom import BloomFilter
from ._version import __version__

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False):
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def bloom_build(args):
    """Build a bloom filter from a directory of files."""
    try:
        input_path = Path(args.input)
        output_path = Path(args.output)
        
        if not input_path.exists():
            logger.error(f"Input path does not exist: {input_path}")
            return 1
        
        logger.info(f"Building bloom filter from {input_path}")
        
        # Create bloom filter
        bloom = BloomFilter.from_directory(
            input_path,
            chunk_size=args.chunk_size,
            false_positive_rate=args.false_positive_rate,
        )
        
        # Save bloom filter
        bloom.save(output_path)
        
        logger.info(f"Bloom filter saved to {output_path}")
        logger.info(f"Added {bloom.metadata['items_added']} chunks from dataset")
        
        return 0
        
    except Exception as e:
        logger.error(f"Failed to build bloom filter: {e}")
        return 1


def bloom_check(args):
    """Check if text appears in a bloom filter."""
    try:
        bloom_path = Path(args.bloom_filter)
        
        if not bloom_path.exists():
            logger.error(f"Bloom filter file does not exist: {bloom_path}")
            return 1
        
        # Load bloom filter
        logger.info(f"Loading bloom filter from {bloom_path}")
        bloom = BloomFilter.load(bloom_path)
        
        results = {}
        
        # Process input files
        for input_file in args.input_files:
            input_path = Path(input_file)
            
            if not input_path.exists():
                logger.warning(f"Input file does not exist: {input_path}")
                results[str(input_path)] = "FILE_NOT_FOUND"
                continue
            
            logger.info(f"Checking {input_path}")
            result = bloom.check_file(input_path)
            results[str(input_path)] = result
            
            # Print result to stdout
            print(f"{input_path}: {result}")
        
        # Save results to JSON if requested
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
            logger.info(f"Results saved to {output_path}")
        
        # Exit with non-zero if any files were MAYBE_PRESENT (for scripting)
        if any(result == "MAYBE_PRESENT" for result in results.values()):
            return 2  # Different exit code for MAYBE_PRESENT
        
        return 0
        
    except Exception as e:
        logger.error(f"Failed to check bloom filter: {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AEGIS Bloom - Copyright compliance toolkit",
        prog="aegis"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"aegis-bloom {__version__}"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # bloom-build command
    build_parser = subparsers.add_parser(
        "bloom-build",
        help="Build a bloom filter from training data"
    )
    build_parser.add_argument(
        "input",
        help="Directory containing training data files"
    )
    build_parser.add_argument(
        "output",
        help="Output path for bloom filter (.bloom file)"
    )
    build_parser.add_argument(
        "--chunk-size",
        type=int,
        default=512,
        help="Text chunk size in bytes (default: 512)"
    )
    build_parser.add_argument(
        "--false-positive-rate",
        type=float,
        default=0.01,
        help="Target false positive rate (default: 0.01)"
    )
    build_parser.set_defaults(func=bloom_build)
    
    # bloom-check command  
    check_parser = subparsers.add_parser(
        "bloom-check",
        help="Check if text appears in training data"
    )
    check_parser.add_argument(
        "input_files",
        nargs="+",
        help="Files to check against the bloom filter"
    )
    check_parser.add_argument(
        "bloom_filter",
        help="Path to bloom filter file"
    )
    check_parser.add_argument(
        "--output", "-o",
        help="Save results to JSON file"
    )
    check_parser.set_defaults(func=bloom_check)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.verbose)
    
    # Show help if no command provided
    if not args.command:
        parser.print_help()
        return 1
    
    # Run the command
    try:
        return args.func(args)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
