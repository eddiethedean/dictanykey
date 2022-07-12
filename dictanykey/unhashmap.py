from typing import Iterator, Mapping
from dictanykey.iterables import DictItems, DictKeys, DictValues

from dictanykey.iterators import DictKeyIterator


class UnHashMap:
    """A dictionary where the keys are not hashed.
       This is strictly slower than dict lookups but
       allows unhashable keys.
    """
    def __init__(self, data=None) -> None:
        self._keys = []
        self._values = []
        if isinstance(data, Mapping):
            data = data.items()
        # unpack data into _keys and _values
        if data is not None:
            for key, value in data:
                self[key] = value
            
    def __contains__(self, value) -> bool:
        return value in self._keys
    
    def __setitem__(self, key, value) -> None:
        if key not in self.keys():
            self._keys.append(key)
            self._values.append(value)
        else:
            i = self._getindex(key)
            self._values[i] = value
            
    def _getindex(self, key) -> int:
        try:
            return self._keys.index(key)
        except ValueError as e:
            raise KeyError(key)
    
    def __getitem__(self, key):
        return self.get(key)
        
    def __delitem__(self, key) -> None:
        i = self._getindex(key)
        del self._keys[i]
        del self._values[i]
        
    def __repr__(self) -> str:
        d = ', '.join(f'{key}: {value}' for key, value in self.items())
        return '{' + f'{d}' + '}'
    
    def __iter__(self) -> Iterator:
        return DictKeyIterator(self.keys())
    
    def __len__(self) -> int:
        return len(self.keys())
    
    def keys(self):
        return DictKeys(self._keys)
    
    def values(self):
        return DictValues(self._values)
    
    def items(self):
        return DictItems([(key, value) for key, value in zip(self._keys, self._values)])
    
    def get(self, key, default=None):
        try:
            i = self._getindex(key)
        except KeyError as e:
            if default is None:
                raise e
            else:
                return default
        return self._values[i]
    
    def __eq__(self, other) -> bool:
        if len(self) != len(other):
            return False
        for key in self.keys():
            if key not in other:
                return False
            if self[key] != other[key]:
                return False
        return True

    def copy(self):
        copy = self.__new__(type(self))
        copy.__init__(self.items())
        return copy

