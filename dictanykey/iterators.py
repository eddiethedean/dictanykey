from typing import Iterable


class DictKeyIterator:
    def __init__(self, keys: Iterable):
        self.keys = iter(keys)
        
    def __next__(self):
        return next(self.keys)
    
    
class DictValueIterator:
    def __init__(self, values: Iterable):
        self.values = iter(values)
        
    def __next__(self):
        return next(self.values)
    
    
class DictItemIterator:
    def __init__(self, items):
        self.items = iter(items)
        
    def __next__(self) -> tuple:
        return next(self.items)