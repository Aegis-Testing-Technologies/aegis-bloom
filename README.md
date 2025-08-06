# AEGIS Bloom 🛡️

**Open-source bloom filter toolkit for copyright compliance in AI training**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/aegis-bloom)](https://pypi.org/project/aegis-bloom/)

## Two Files, Zero Arguments

AEGIS Bloom provides dead-simple copyright compliance for AI developers:

```bash
# Build a bloom filter from your training data
aegis bloom-build data/ corpus.bloom

# Check if text appears in the training corpus
aegis bloom-check text.txt corpus.bloom
# Output: NOT_PRESENT or MAYBE_PRESENT
```

That's it. No complex configuration. No cloud dependencies. Just fast, local copyright checks.

## Why AEGIS Bloom?

As AI models face increasing scrutiny over training data usage, developers need tools to:
- ✅ Verify content wasn't in training data (copyright safety)
- ✅ Check for potential contamination (benchmark integrity)  
- ✅ Demonstrate compliance to stakeholders
- ✅ All locally, without sending data to third parties

## Installation

```bash
pip install aegis-bloom
```

Requirements:
- Python 3.8+
- 2GB RAM for typical datasets
- 100MB disk space

## Quick Start

### 1. Build a bloom filter from your dataset

```python
from aegis import BloomFilter

# Create bloom filter from a directory of text files
bloom = BloomFilter.from_directory("data/", chunk_size=512)

# Save for later use (16MB compressed)
bloom.save("corpus.bloom")
```

### 2. Check if content appears in the dataset

```python
# Load existing bloom filter
bloom = BloomFilter.load("corpus.bloom")

# Check a text file
result = bloom.check_file("alice_cookbook.txt")
print(result)  # "MAYBE_PRESENT" or "NOT_PRESENT"

# Check a string directly
result = bloom.check("This is my original content")
```

### 3. Command-line usage

```bash
# Build bloom filter from directory
aegis bloom-build training_data/ my_corpus.bloom

# Check single file
aegis bloom-check manuscript.txt my_corpus.bloom

# Batch check multiple files
aegis bloom-check chapters/*.txt my_corpus.bloom --output results.json
```

## Performance

- **Build time**: <90 seconds for 1GB of text
- **Query time**: <1 second per check
- **Memory usage**: ≤2GB during build
- **False positive rate**: ≤1% (configurable)
- **File size**: ~16MB compressed (64MB raw)

## How It Works

AEGIS Bloom uses a space-efficient probabilistic data structure to encode your training dataset:

1. **Chunking**: Splits text into 512-byte overlapping chunks
2. **Hashing**: Uses SHA-256 for consistent, cryptographic hashing
3. **Bloom filter**: Encodes presence with multiple hash functions
4. **Consecutive detection**: Requires ≥3 consecutive chunks for MAYBE_PRESENT

This approach provides:
- **No false negatives**: If it says NOT_PRESENT, the content definitely wasn't in training data
- **Low false positives**: ~1% chance of incorrectly flagging content as present
- **Privacy preserving**: Original content cannot be reconstructed from the bloom filter

## Examples

See the [`examples/`](examples/) directory for:
- Alice's cookbook copyright check
- Academic paper contamination detection
- Batch processing pipelines
- Integration with training workflows

## Advanced Usage

### Custom parameters

```python
bloom = BloomFilter(
    expected_items=10_000_000,  # Expected number of chunks
    false_positive_rate=0.001,   # Target 0.1% false positive rate
    chunk_size=1024,             # Larger chunks for books
    consecutive_chunks=5         # Require 5 chunks for match
)
```

### Streaming large datasets

```python
bloom = BloomFilter()
for file_path in dataset.iter_files():
    bloom.add_file(file_path)  # Processes file in chunks
bloom.save("large_corpus.bloom")
```

## Looking for Cryptographically Bound Proofs?

AEGIS Bloom is the open-source component of the larger AEGIS platform. For cryptographic proofs binding model weights to training data, Zero-Knowledge attestations, and enterprise compliance features:

**[→ Join the waitlist](https://aegisprove.com)**

## License

AEGIS Bloom is MIT licensed. See [LICENSE](LICENSE) for details.

For enterprise features and support, see [LICENSE-README.md](LICENSE-README.md).

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

- 📧 Email: support@aegisprove.com
- 🐛 Issues: [GitHub Issues](https://github.com/Aegis-Testing-Technologies/aegis-bloom/issues)
- 💬 Discord: [Join our community](https://discord.gg/aegis)

---

Built with ❤️ by [AEGIS Testing Technologies](https://aegisprove.com)
