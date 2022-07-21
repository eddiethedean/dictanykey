from typing import Any, Iterator, Mapping, Optional, Iterable
from dictanykey.iterables import DictItems, DictKeys, DictValues, OrderedKeys

from dictanykey.unhashmap import UnHashMap
import dictanykey.anykey_utils as utils

class DictAnyKey:
    """A dictionary where the keys don't need to be hashable
       Stores hashable keys with values in _hashmap: dict
       Stores unhashable keys with values in _unhashmap: UnHashMap

       Maintains order of items inserted.

       Unhashable key lookups are slower than built in dict.
       Hashable key lookups are the same speed as built in dict.
    """
    def __init__(self, data: Optional[Iterable | Mapping] = None) -> None:
        self._hashmap: dict = {}
        self._unhashmap = UnHashMap()
        self._keys = OrderedKeys()
        self.update(data)

    def __getitem__(self, key: Any) -> Any:
        return utils.anykey_getitem(self, key)
        
    def __contains__(self, value: Any) -> bool:
        return value in self._keys
    
    def __setitem__(self, key: Any, value: Any) -> None:
        try:
            self._hashmap[key] = value
        except TypeError:
            self._unhashmap[key] = value
        self._keys.add(key)

    def __len__(self) -> int:
        return utils.anykey_len(self)

    def __str__(self) -> str:
        return utils.anykey_str(self)
        
    def __delitem__(self, key: Any) -> None:
        try:
            del self._hashmap[key]
        except (KeyError, TypeError):
            del self._unhashmap[key]
        self._keys.delete(key)

    def __repr__(self) -> str:
        return f'DictAnyKey({[(key, value) for key, value in self._get_items_list()]})'

    def __iter__(self) -> Iterator:
        return utils.anykey_iter(self)

    def __eq__(self, other: Mapping) -> bool:
        return utils.anykey_eq(self, other)

    def _get_keys_list(self) -> list[Any]:
        return list(self._keys)

    def _get_values_list(self) -> list[Any]:
        return [self[key] for key in self._get_keys_list()]

    def _get_items_list(self) -> list[tuple]:
        return [(key, self[key]) for key in self._get_keys_list()]
    
    def keys(self) -> DictKeys:
        return DictKeys(self)
    
    def values(self) -> DictValues:
        return DictValues(self)
    
    def items(self) -> DictItems:
        return DictItems(self)
    
    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        """Return the value for key if key is in the dictionary, else default."""
        if key not in self._get_keys_list():
            return default
        try:
            return self._hashmap[key]
        except (KeyError, TypeError):
            try:
                return self._unhashmap[key]
            except KeyError:
                return default

    def update(self, data: Optional[Iterable | Mapping] = None) -> None:
        """Update dict from dict/iterable data.
           If data is present and has a .keys() method, then does:  for k in data: self[k] = data[k]
           If data is present and lacks a .keys() method, then does:  for k, v in data: self[k] = v
        """
        utils.anykey_update(self, data)

    def clear(self):
        """Remove all items from self."""
        self._hashmap: dict = {}
        self._unhashmap = UnHashMap()
        self._keys = OrderedKeys()

    def copy(self):
        return utils.anykey_copy(self)

    def setdefault(self, key: Any, default: Optional[Any] = None) -> Any:
        """Insert key with a value of default if key is not in the dictionary.

           Return the value for key if key is in the dictionary, else default.
        """
        return utils.anykey_setdefault(self, key, default)

    # TODO: pop method
    def pop(self, key: Any, default=None):
        """Docstring:
        D.pop(k[,d]) -> v, remove specified key and return the corresponding value.

        If key is not found, default is returned if given, otherwise KeyError is raised
        """
        try:
            value = self[key]
        except KeyError as e:
            if default is None:
                raise e
            else:
                return default
        del self[key]

    # TODO: popitem method
    def popitem(self):
        raise NotImplementedError
        """Docstring:
        Remove and return a (key, value) pair as a 2-tuple.

        Pairs are returned in LIFO (last-in, first-out) order.
        Raises KeyError if the dict is empty.
        """

    # TODO: fromkeys method
    def fromkeys(self, iterable, value: Optional[Any] = None):
        raise NotImplementedError
        """Signature: d.fromkeys(iterable, value=None, /)
        Docstring: Create a new dictionary with keys from iterable and values set to value.
        """