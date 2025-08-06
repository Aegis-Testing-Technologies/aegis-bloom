# Contributing to AEGIS Bloom

Thank you for your interest in contributing to AEGIS Bloom! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [conduct@aegisprove.com](mailto:conduct@aegisprove.com).

## Getting Started

### What We're Looking For

We welcome contributions in these areas:

- **Bug fixes**: Issues with bloom filter accuracy, performance, or compatibility
- **Performance improvements**: Optimizations to build/query speed or memory usage
- **Documentation**: Examples, tutorials, API documentation improvements
- **Platform support**: Additional OS/architecture support
- **Testing**: More comprehensive test coverage

### What We're NOT Looking For

- **Cryptographic features**: ZK proofs, Nova circuits, etc. are enterprise-only
- **Cloud integrations**: Authentication, remote attestation, etc.
- **Breaking API changes**: Without prior discussion in an issue

## Development Setup

### Prerequisites

- Python 3.8+
- Rust 1.70+ (for native extensions)
- Git with LFS (for test data)

### Local Development

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/aegis-bloom.git
   cd aegis-bloom
   ```

2. **Initialize submodules**
   ```bash
   git submodule update --init --recursive
   ```

3. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

4. **Build Rust extensions** (optional, falls back to Python)
   ```bash
   maturin develop --release
   ```

5. **Run tests**
   ```bash
   pytest
   ```

6. **Run the examples**
   ```bash
   python examples/alice_cookbook_check.py
   ```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `fix/bloom-filter-false-negatives`
- `feature/cli-batch-processing`
- `docs/python-api-examples`

### Code Style

We use automated formatting and linting:

```bash
# Format code
ruff format .

# Check linting
ruff check .

# Type checking
mypy python/aegis/
```

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add batch processing to CLI check command

- Support multiple input files in bloom-check
- Add --output flag for JSON results
- Improve error handling for missing files

Fixes #42
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=aegis --cov-report=html

# Run specific test file
pytest tests/test_bloom_filter.py

# Run performance benchmarks
pytest tests/test_performance.py -m benchmark
```

### Writing Tests

- Add tests for new features in `tests/`
- Use descriptive test names: `test_bloom_filter_handles_large_datasets`
- Include performance tests for critical paths
- Test error conditions and edge cases

### Test Data

Small test datasets are included in the repo. For larger datasets:

```bash
# Generate test data (for performance testing)
python tests/generate_test_data.py
```

## Submitting Changes

### Pull Request Process

1. **Create an issue first** (for non-trivial changes)
   - Describe the problem or feature request
   - Discuss the approach with maintainers
   - Reference any related issues

2. **Prepare your pull request**
   - Update documentation if needed
   - Add tests for new functionality
   - Ensure all tests pass
   - Update CHANGELOG.md if applicable

3. **Submit the pull request**
   - Use a clear title and description
   - Reference the related issue: "Fixes #123"
   - Include screenshots for UI changes
   - Add yourself to AUTHORS.md

4. **Respond to review feedback**
   - Address comments and suggestions
   - Push additional commits as needed
   - Re-request review when ready

### Review Criteria

Pull requests are evaluated on:

- **Correctness**: Does it solve the stated problem?
- **Performance**: No significant performance regressions
- **Compatibility**: Works across supported Python versions
- **Testing**: Adequate test coverage
- **Documentation**: Clear docs and examples

## Release Process

Releases follow semantic versioning (semver):

- **Major** (1.0.0): Breaking API changes
- **Minor** (0.1.0): New features, backwards compatible
- **Patch** (0.0.1): Bug fixes, backwards compatible

### Release Steps (for maintainers)

1. Update version in `pyproject.toml` and `_version.py`
2. Update `CHANGELOG.md` with release notes
3. Create release PR and merge after review
4. Tag release: `git tag v0.1.0 && git push origin v0.1.0`
5. GitHub Actions will build and publish to PyPI

## Community

### Getting Help

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Design discussions and questions
- **Discord**: Real-time chat with the community
- **Email**: [support@aegisprove.com](mailto:support@aegisprove.com) for private inquiries

### Staying Updated

- Watch the repository for notifications
- Follow [@AegisProve](https://twitter.com/aegisprove) on Twitter
- Join our [Discord community](https://discord.gg/aegis)

## License

By contributing to AEGIS Bloom, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors are recognized in:
- `AUTHORS.md` file
- Release notes for significant contributions
- Annual contributor spotlight posts

Thank you for helping make AEGIS Bloom better! 🛡️
