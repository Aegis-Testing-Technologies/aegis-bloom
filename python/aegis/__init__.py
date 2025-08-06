"""AEGIS Bloom - Open-source bloom filter toolkit for copyright compliance."""

from .bloom import BloomFilter
from ._version import __version__

__all__ = ["BloomFilter", "__version__"]
