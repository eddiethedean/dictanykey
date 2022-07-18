from typing import Mapping, Any, Iterable, Optional
from dictanykey.iterables import DictItems, DictKeys, DictValues

from dictanykey.mapping_mixin import MappingMixin


class UnHashMap(MappingMixin):
    """A dictionary where the keys don't need to be hashable.
       Stores keys in _keys: list
       Stores values in _values: list

       Uses == to compare keys rather than hash function

       Much slower key lookup speeds compared to dict but
       keys don't need to be hashable.
    """
    def __init__(self, data: Optional[Iterable] = None) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
        self._keys: list = []
        self._values: list = []
        self.update(data)

    def __contains__(self, value: Any) -> bool:
        """True if the dictionary has the specified key, else False."""
        return value in self.keys()
            
    def __setitem__(self, key: Any, value: Any) -> None:
        """Set self[key] to value."""
        if key not in self.keys():
            self._keys.append(key)
            self._values.append(value)
        else:
            i = self._getindex(key)
            self._values[i] = value
            
    def _getindex(self, key: Any) -> int:
        """Use _keys.index method to look up and return index of key.
           Raises KeyError if key is not in _keys.
        """
        try:
            return self._keys.index(key)
        except ValueError as e:
            raise KeyError(key)
        
    def __delitem__(self, key: Any) -> None:
        """Delete self[key]."""
        i = self._getindex(key)
        del self._keys[i]
        del self._values[i]

    def __repr__(self) -> str:
        """Return repr(self)."""
        return f'UnHashMap({[(key, value) for key, value in self.items()]})'
    
    def keys(self) -> DictKeys:
        """Returns a set-like object providing a view on self's keys"""
        return DictKeys(self._keys)
    
    def values(self) -> DictValues:
        """Returns an object providing a view on self's values"""
        return DictValues(self._values)
    
    def items(self) -> DictItems:
        """Returns set-like object providing a view on self's items"""
        return DictItems([(key, value) for key, value in zip(self._keys, self._values)])
    
    def get(self, key, default: Optional[Any] = None) -> Any:
        """Return the value for key if key is in the dictionary, else default."""
        try:
            i = self._getindex(key)
        except KeyError:
            return default
        return self._values[i]

    # TODO: pop method
    def pop(self, key, default=None):
        ...
    """Docstring:
       D.pop(k[,d]) -> v, remove specified key and return the corresponding value.

       If key is not found, default is returned if given, otherwise KeyError is raised
    """

    # TODO: popitem method
    def popitem(self):
        ...
    """Docstring:
       Remove and return a (key, value) pair as a 2-tuple.

       Pairs are returned in LIFO (last-in, first-out) order.
       Raises KeyError if the dict is empty.
    """

    def clear(self):
        self._keys: list = []
        self._values: list = []
    
    def fromkeys(iterable, value=None):
        ...
    # TODO: fromkeys method
    """Signature: d.fromkeys(iterable, value=None, /)
       Docstring: Create a new dictionary with keys from iterable and values set to value.
    """