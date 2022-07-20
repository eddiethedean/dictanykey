from typing import Any, Iterable, Iterator, Protocol


class AnyKeyMapping(Protocol):
    def __len__(self) -> int:
        ...

    def _get_keys_list(self) -> list:
        ...

    def _get_values_list(self) -> list:
        ...

    def _get_items_list(self) -> list[tuple]:
        ...



class DictKeyIterator:
    def __init__(self, parent: AnyKeyMapping) -> None:
        self.parent: AnyKeyMapping = parent
        self.len: int = len(parent)
        self.iterator: Iterator = iter(parent._get_keys_list())

    def __next__(self) -> Any:
        if len(self.parent) != self.len:
            raise RuntimeError('dictionary changed size during iteration')
        return next(self.iterator)
    
    
class DictValueIterator:
    def __init__(self, parent: AnyKeyMapping) -> None:
        self.parent: AnyKeyMapping = parent
        self.len: int = len(parent)
        self.iterator: Iterator = iter(parent._get_values_list())

    def __next__(self) -> Any:
        if len(self.parent) != self.len:
            raise RuntimeError('dictionary changed size during iteration')
        return next(self.iterator)
    
    
class DictItemIterator:
    def __init__(self, parent: AnyKeyMapping):
        self.parent: AnyKeyMapping = parent
        self.len: int = len(parent)
        self.iterator: Iterator = iter(parent._get_items_list())

    def __next__(self) -> Any:
        if len(self.parent) != self.len:
            raise RuntimeError('dictionary changed size during iteration')
        return next(self.iterator)