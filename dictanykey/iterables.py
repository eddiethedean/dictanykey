from typing import Iterable, Iterator, Any, Optional

from dictanykey.iterators import DictItemIterator, DictKeyIterator, DictValueIterator


class DictKeys:
    def __init__(self, keys: Iterable) -> None:
        self.keys = keys

    def __len__(self):
        return len(self.keys)

    def __contains__(self, key: Any) -> bool:
        return key in self.keys

    def __iter__(self) -> DictKeyIterator:
        return DictKeyIterator(self.keys)
    
    def __repr__(self) -> str:
        return f'DictKeys({self.keys})'
    
    
class DictValues:
    def __init__(self, values: Iterable):
        self.values = values

    def __len__(self):
        return len(self.values)

    def __contains__(self, value):
        return value in self.values

    def __iter__(self):
        return DictValueIterator(self.values)
    
    def __repr__(self):
        return f'DictValues({self.values})'
    
    
class DictItems:
    def __init__(self, items: Iterable):
        self.items = items

    def __len__(self):
        return len(self.items)

    def __contains__(self, item):
        return item in self.items

    def __iter__(self):
        return DictItemIterator(self.items)
    
    def __repr__(self):
        return f'DictItems({self.items})'


class OrderedKeys:
    def __init__(self, keys: Optional[Iterable] = None) -> None:
        self.keys: list = list(keys) if keys is not None else []
        
    def add(self, key):
        if key not in self.keys:
            self.keys.append(key)
            
    def delete(self, key):
        if key in self.keys:
            i = self.keys.index(key)
            del self.keys[i]
            
    def __iter__(self) -> Iterator:
        return DictKeyIterator(self.keys)