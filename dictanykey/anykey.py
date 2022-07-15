from typing import Any, Mapping, Optional, Iterable
from dictanykey.iterables import DictItems, DictKeys, DictValues, OrderedKeys

from dictanykey.unhashmap import UnHashMap
from dictanykey.mapping_mixin import MappingMixin


class DictAnyKey(MappingMixin):
    """A dictionary where the keys don't need to be hashable
       Stores hashable keys with values in _hashmap: dict
       Stores unhashable keys with values in _unhashmap: UnHashMap

       Maintains order of items inserted.

       Unhashable key lookups are slower than built in dict.
       Hashable key lookups are the same speed as built in dict.
    """
    def __init__(self, data: Optional[Iterable] = None) -> None:
        self._hashmap: dict = {}
        self._unhashmap = UnHashMap()
        self._keys = OrderedKeys()
        if isinstance(data, Mapping):
            data = data.items()
        if data is not None:
            for key, value in data:
                self[key] = value
                self._keys.add(key)
            
    def __contains__(self, value: Any) -> bool:
        return value in self._keys
    
    def __setitem__(self, key: Any, value: Any) -> None:
        try:
            self._hashmap[key] = value
        except TypeError:
            self._unhashmap[key] = value
        self._keys.add(key)
        
    def __delitem__(self, key: Any) -> None:
        try:
            del self._hashmap[key]
        except (KeyError, TypeError):
            del self._unhashmap[key]
        self._keys.delete(key)

    def __repr__(self) -> str:
        return f'DictAnyKey({[(key, value) for key, value in self.items()]})'
    
    def keys(self) -> DictKeys:
        return DictKeys([key for key in self._keys])
    
    def values(self) -> DictValues:
        return DictValues([self[key] for key in self._keys])
    
    def items(self) -> DictItems:
        return DictItems([(key, self[key]) for key in self._keys])
    
    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        if key not in self.keys():
            return default
        try:
            return self._hashmap[key]
        except (KeyError, TypeError):
            try:
                return self._unhashmap[key]
            except KeyError:
                return default

    # TODO: update method

    # TODO: pop method

    # TODO: popitem method

    # TODO: clear method

    # TODO: setdefault method
    
    # TODO: fromkeys method