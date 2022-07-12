from typing import Any, Iterator, Mapping
from dictanykey.iterables import DictItems, DictKeys, DictValues, OrderedKeys

from dictanykey.unhashmap import UnHashMap

            
class DictAnyKey:
    """A dictionary where the keys don't need to be hashable"""
    def __init__(self, data=None) -> None:
        # Store hashable keys in _hashmap: dict
        self._hashmap = {}
        # Store unhashble keys in _unhashmap: UnHashMap
        self._unhashmap = UnHashMap()
        # keep track of order of keys in _keys: OrderedKeys
        self._keys = OrderedKeys([])
        # pull out items if data is Mapping
        if isinstance(data, Mapping):
            data = data.items()
        # unpack key, value from data
        if data is not None:
            for key, value in data:
                self[key] = value
                self._keys.add(key)
            
    def __contains__(self, value) -> bool:
        return value in self.keys()
    
    def __setitem__(self, key, value) -> None:
        try:
            self._hashmap[key] = value
        except TypeError:
            self._unhashmap[key] = value
        self._keys.add(key)
        
    
    def __getitem__(self, key) -> Any:
        return self.get(key)
        
    def __delitem__(self, key) -> None:
        try:
            del self._hashmap[key]
        except (KeyError, TypeError):
            del self._unhashmap[key]
        self._keys.delete(key)
        
    def __repr__(self) -> str:
        d = ', '.join(f'{key}: {value}' for key, value in self.items())
        return '{' + f'{d}' + '}'
    
    def __iter__(self) -> Iterator:
        return iter(self.keys())
    
    def __len__(self) -> int:
        return len(self.keys())
    
    def __eq__(self, other) -> bool:
        if len(self) != len(other):
            return False
        for key in self.keys():
            if key not in other:
                return False
            if self[key] != other[key]:
                return False
        return True
    
    def keys(self):
        return DictKeys([key for key in self._keys])
    
    def values(self):
        return DictValues([self[key] for key in self._keys])
    
    def items(self):
        return DictItems([(key, self[key]) for key in self._keys])
    
    def get(self, key, default=None):
        try:
            return self._hashmap.get(key)
        except TypeError:
            return self._unhashmap.get(key, default)
    
    def copy(self):
        copy = self.__new__(type(self))
        copy.__init__(self.items())
        return copy