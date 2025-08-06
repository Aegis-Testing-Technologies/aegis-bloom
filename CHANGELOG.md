# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-08-06

### Added
- Initial open source release
- Pure Python bloom filter implementation for copyright compliance
- CLI commands: `aegis bloom-build` and `aegis bloom-check`
- Comprehensive test suite with 6 passing tests
- Automatic fallback when Rust extensions unavailable
- Environment variable `AEGIS_BLOOM_NO_RUST` to force pure Python mode
- Support for processing text files and directories
- Configurable bloom filter parameters (size, false positive rate, chunk size)
- Consecutive chunk requirement for legal compliance (≥3 chunks for MAYBE_PRESENT)
- Save/load functionality with gzip compression
- Package metadata and proper PyPI structure

### Technical Details
- **Package size**: 11 KB (wheel), 13 KB (source)
- **Python compatibility**: 3.8+
- **Dependencies**: None (pure Python)
- **License**: MIT
- **Repository**: https://github.com/Aegis-Testing-Technologies/aegis-bloom

[0.1.0]: https://github.com/Aegis-Testing-Technologies/aegis-bloom/releases/tag/v0.1.0
