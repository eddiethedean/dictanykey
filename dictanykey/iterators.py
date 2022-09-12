from typing import Any, Iterable, Iterator, Mapping


class DictKeyIterator:
    def __init__(self, parent: Mapping) -> None:
        self.parent: Mapping = parent
        self.len: int = len(parent)
        self.iterator: Iterator = iter(parent._get_keys_list())

    def __iter__(self):
        return self

    def __next__(self) -> Any:
        if len(self.parent) != self.len:
            raise RuntimeError('dictionary changed size during iteration')
        return next(self.iterator)
    
    
class DictValueIterator:
    def __init__(self, parent: Mapping) -> None:
        self.parent: Mapping = parent
        self.len: int = len(parent)
        self.iterator: Iterator = iter(parent._get_values_list())

    def __iter__(self):
        return self

    def __next__(self) -> Any:
        if len(self.parent) != self.len:
            raise RuntimeError('dictionary changed size during iteration')
        return next(self.iterator)
    
    
class DictItemIterator:
    def __init__(self, parent: Mapping):
        self.parent: Mapping = parent
        self.len: int = len(parent)
        self.iterator: Iterator = iter(parent._get_items_list())

    def __iter__(self):
        return self

    def __next__(self) -> Any:
        if len(self.parent) != self.len:
            raise RuntimeError('dictionary changed size during iteration')
        return next(self.iterator)