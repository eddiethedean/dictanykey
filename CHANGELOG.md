# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-XX

### Added
- Initial release of DictAnyKey package
- Support for unhashable keys (lists, dicts, etc.) in dictionaries
- DictAnyKey class with full dict-like interface
- DefaultDictAnyKey class extending collections.defaultdict functionality
- FrozenDictAnyKey class for immutable dictionaries
- value_counts() utility function for counting unhashable values
- Comprehensive test suite with unittest
- Python 3.9+ support
- Type hints throughout codebase
- py.typed marker for PEP 561 compliance

### Features
- Maintains insertion order like built-in dict
- Hashable key lookups at same speed as built-in dict
- Unhashable key lookups with linear search (slower but functional)
- Full compatibility with dict interface (keys, values, items, etc.)
- Support for mixed hashable/unhashable keys in same dictionary
- Proper error handling and edge cases
- Iterator safety with mutation detection

### Technical Details
- Uses dual storage: dict for hashable keys, UnHashMap for unhashable keys
- OrderedKeys class maintains insertion order
- Custom view objects (DictKeys, DictValues, DictItems) for compatibility
- Iterator classes with mutation detection
- Comprehensive type annotations
- Modern packaging with pyproject.toml
