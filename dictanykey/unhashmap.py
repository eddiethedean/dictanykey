from typing import Any, Iterable, Iterator, Mapping, Optional
from dictanykey.iterables import DictItems, DictKeys, DictValues
from dictanykey.anykey_utils import anykey_copy, anykey_eq, anykey_getitem, anykey_iter, anykey_len, anykey_setdefault, anykey_str, anykey_update


class UnHashMap:
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
        return value in self._keys
            
    def __setitem__(self, key: Any, value: Any) -> None:
        """Set self[key] to value."""
        if key not in self._keys:
            self._keys.append(key)
            self._values.append(value)
        else:
            i = self._getindex(key)
            self._values[i] = value

    def __getitem__(self, key: Any) -> Any:
        return anykey_getitem(self, key)

    def __len__(self) -> int:
        return anykey_len(self)

    def __str__(self) -> str:
        return anykey_str(self)

    def __iter__(self) -> Iterator:
        return anykey_iter(self)

    def __eq__(self, other: Mapping) -> bool:
        return anykey_eq(self, other)
            
    def _getindex(self, key: Any) -> int:
        """Use _keys.index method to look up and return index of key.
           Raises KeyError if key is not in _keys.
        """
        try:
            return self._keys.index(key)
        except ValueError as e:
            raise KeyError(key)

    def _get_keys_list(self) -> list[Any]:
        return self._keys

    def _get_values_list(self) -> list[Any]:
        return [self[key] for key in self._get_keys_list()]

    def _get_items_list(self) -> list[tuple]:
        return [(key, self[key]) for key in self._get_keys_list()]
        
    def __delitem__(self, key: Any) -> None:
        """Delete self[key]."""
        i = self._getindex(key)
        del self._keys[i]
        del self._values[i]

    def __repr__(self) -> str:
        """Return repr(self)."""
        return f'UnHashMap({[(key, value) for key, value in self._get_items_list()]})'
    
    def keys(self) -> DictKeys:
        """Returns a set-like object providing a view on self's keys"""
        return DictKeys(self)
    
    def values(self) -> DictValues:
        """Returns an object providing a view on self's values"""
        return DictValues(self)
    
    def items(self) -> DictItems:
        """Returns set-like object providing a view on self's items"""
        return DictItems(self)
    
    def get(self, key, default: Optional[Any] = None) -> Any:
        """Return the value for key if key is in the dictionary, else default."""
        try:
            i = self._getindex(key)
        except KeyError:
            return default
        return self._values[i]

    def update(self, data) -> None:
        anykey_update(self, data)
    
    def clear(self):
        self._keys: list = []
        self._values: list = []

    def copy(self):
        return anykey_copy(self)

    def setdefault(self, key: Any, default: Optional[Any] = None) -> Any:
        return anykey_setdefault(self, key, default)