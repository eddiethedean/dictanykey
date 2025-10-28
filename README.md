# DictAnyKey: Python Dictionary That Can Use Any Key

[![PyPI Latest Release](https://img.shields.io/pypi/v/dictanykey.svg)](https://pypi.org/project/dictanykey/)
[![Python Version](https://img.shields.io/pypi/pyversions/dictanykey.svg)](https://pypi.org/project/dictanykey/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**DictAnyKey** is a modern Python package that provides dictionary-like objects capable of using unhashable keys (such as lists and dictionaries) while maintaining excellent performance for hashable keys.

## ✨ Key Features

- 🔑 **Any Key Type**: Use lists, dictionaries, sets, or any unhashable object as keys
- ⚡ **Optimized Performance**: Hashable keys perform at native dict speed
- 📊 **Maintains Order**: Preserves insertion order like Python 3.7+ dictionaries
- 🧊 **Immutable Variant**: `FrozenDictAnyKey` for hashable, immutable dictionaries
- 🎯 **Default Values**: `DefaultDictAnyKey` with customizable default factories
- 📈 **Value Counting**: Built-in `value_counts()` function for frequency analysis
- 🔒 **Type Safe**: Full type hints and mypy compliance
- 🧪 **Well Tested**: Comprehensive test suite with 271+ tests

## 🚀 Quick Start

### Installation

```bash
pip install dictanykey
```

### Basic Usage

```python
from dictanykey import DictAnyKey, FrozenDictAnyKey, DefaultDictAnyKey, value_counts

# Create a dictionary with mixed key types
d = DictAnyKey()

# Hashable keys (fast lookup)
d[1] = "one"
d["hello"] = "world"

# Unhashable keys (slower but supported)
d[[1, 2, 3]] = "list key"
d[{"nested": "dict"}] = "dict key"

print(d)  # {1: 'one', 'hello': 'world', [1, 2, 3]: 'list key', {'nested': 'dict'}: 'dict key'}

# All standard dictionary operations work
print(len(d))           # 4
print(1 in d)           # True
print([1, 2, 3] in d)   # True
print(d.get("missing", "default"))  # default

# Iteration preserves insertion order
for key, value in d.items():
    print(f"{key}: {value}")
# Output:
#   1: one
#   hello: world
#   [1, 2, 3]: list key
#   {'nested': 'dict'}: dict key
```

### Advanced Features

#### FrozenDictAnyKey (Immutable)

```python
# Create immutable dictionary
frozen = FrozenDictAnyKey({1: "one", (1, 2): "tuple"})

# Read operations work normally
print(frozen[1])  # one

# Mutation operations raise errors
try:
    frozen[2] = "two"  # Raises TypeError
except TypeError:
    print("Cannot modify frozen dictionary")  # Cannot modify frozen dictionary

# Can be used as dictionary keys (if all keys are hashable)
if all(isinstance(k, (int, str, tuple)) for k in frozen.keys()):
    other_dict = {frozen: "value"}
    print(other_dict)  # {FrozenDictAnyKey([(1, 'one'), ((1, 2), 'tuple')]): 'value'}
```

#### DefaultDictAnyKey

```python
# Create with default factory
dd = DefaultDictAnyKey(list)  # Default to empty list

# Missing keys automatically get default value
dd["new_key"].append("item")
print(dd["new_key"])  # ['item']

# Works with any callable
dd_int = DefaultDictAnyKey(lambda: 0)
dd_int["count"] += 1
print(dd_int["count"])  # 1
```

#### Value Counting

```python
# Count frequency of values
data = [1, 2, 2, 3, 3, 3, "a", "a", "b"]
counts = value_counts(data)

print(counts)  # {1: 1, 'b': 1, 2: 2, 'a': 2, 3: 3}

# Sort options
counts_asc = value_counts(data, ascending=True)   # Lowest to highest
counts_desc = value_counts(data, ascending=False)  # Highest to lowest
counts_unsorted = value_counts(data, sort=False)   # Preserve original order

print(counts_asc)    # {1: 1, 'b': 1, 2: 2, 'a': 2, 3: 3}
print(counts_desc)   # {3: 3, 2: 2, 'a': 2, 1: 1, 'b': 1}
print(counts_unsorted)  # {1: 1, 2: 2, 3: 3, 'a': 2, 'b': 1}

# Works with unhashable values too!
unhashable_data = [[1, 2], [1, 2], [3, 4], [1, 2]]
unhashable_counts = value_counts(unhashable_data)
print(unhashable_counts)  # {[3, 4]: 1, [1, 2]: 3}
```

## 📋 Requirements

- **Python**: 3.9+ (supports 3.9, 3.10, 3.11, 3.12, 3.13)
- **Dependencies**: None (pure Python)

## 🔧 API Reference

### DictAnyKey

The main dictionary class supporting any key type.

```python
class DictAnyKey(MutableMapping[Any, Any]):
    def __init__(self, data: Optional[Union[Iterable, Mapping]] = None) -> None
    def __getitem__(self, key: Any) -> Any
    def __setitem__(self, key: Any, value: Any) -> None
    def __delitem__(self, key: Any) -> None
    def __len__(self) -> int
    def __iter__(self) -> Iterator[Any]
    def __contains__(self, key: Any) -> bool
    def __eq__(self, other: object) -> bool
    
    # Standard dictionary methods
    def get(self, key: Any, default: Optional[Any] = None) -> Any
    def pop(self, key: Any, default: Optional[Any] = None) -> Any
    def popitem(self) -> tuple[Any, Any]
    def setdefault(self, key: Any, default: Optional[Any] = None) -> Any
    def update(self, data: Optional[Union[Iterable, Mapping]] = None) -> None
    def clear(self) -> None
    def copy(self) -> DictAnyKey
    def fromkeys(cls, keys: Iterable[Any], value: Optional[Any] = None) -> DictAnyKey
    
    # View objects
    def keys(self) -> DictKeys
    def values(self) -> DictValues
    def items(self) -> DictItems
```

### FrozenDictAnyKey

Immutable version of DictAnyKey.

```python
class FrozenDictAnyKey(DictAnyKey):
    def __hash__(self) -> int  # Raises TypeError if keys are unhashable
    # All mutation methods raise AttributeError
```

### DefaultDictAnyKey

Dictionary with default value factory.

```python
class DefaultDictAnyKey(DictAnyKey):
    def __init__(self, default_factory: Optional[Callable[[], Any]], 
                 data: Optional[Union[Iterable, Mapping]] = None) -> None
    # Inherits all DictAnyKey methods
    # Missing keys automatically get default_factory() value
```

### Utility Functions

```python
def value_counts(values: Iterable[Any], 
                sort: bool = True, 
                ascending: bool = True) -> DictAnyKey
```

## 🎯 Use Cases

### Data Processing
```python
# Group data by complex keys
groups = DictAnyKey()
for item in data:
    key = (item.category, item.subcategory, item.tags)
    if key not in groups:
        groups[key] = []
    groups[key].append(item)
```

### Configuration Management
```python
# Use nested structures as keys
config = DictAnyKey()
config[("database", "host")] = "localhost"
config[("database", "port")] = 5432
config[("cache", "redis", "host")] = "redis-server"
```

### Scientific Computing
```python
# Use arrays as keys for matrix operations
matrix_cache = DictAnyKey()
matrix_cache[tuple([1, 2, 3])] = compute_expensive_result([1, 2, 3])
```

## ⚡ Performance Characteristics

- **Hashable Keys**: O(1) lookup, same performance as built-in `dict`
- **Unhashable Keys**: O(n) lookup, where n is the number of unhashable keys
- **Memory**: Slightly higher memory usage due to dual storage (hashmap + list)
- **Insertion Order**: Always preserved, regardless of key type

## 🧪 Testing

The package includes comprehensive tests covering:

- All dictionary operations with various key types
- Edge cases (empty dictionaries, mutation during iteration)
- Performance characteristics
- Type safety and error handling
- Immutable and default dictionary variants

Run tests with:
```bash
pytest tests/
```

## 🔍 Development

### Code Quality Tools

The project uses modern Python tooling:

- **Ruff**: Fast linting and formatting
- **MyPy**: Static type checking
- **Pytest**: Testing framework
- **Black**: Code formatting (via ruff)

```bash
# Format code
ruff format

# Lint code
ruff check

# Type check
mypy dictanykey/

# Run tests
pytest tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆕 Changelog

### Latest Version
- ✅ Fixed critical bugs in `setdefault()`, `pop()`, and `popitem()` methods
- ✅ Added comprehensive test coverage (271+ tests)
- ✅ Modernized to Python 3.9+ with full type hints
- ✅ Added `FrozenDictAnyKey` hash support
- ✅ Optimized performance for key lookups
- ✅ Migrated to `pyproject.toml` configuration
- ✅ Added `value_counts()` utility function
- ✅ Improved documentation and examples

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/eddiethedean/dictanykey/issues)
- **Documentation**: This README and inline docstrings
- **Source**: [GitHub Repository](https://github.com/eddiethedean/dictanykey)

---

**DictAnyKey** - Because sometimes you need a dictionary that accepts anything as a key! 🗝️