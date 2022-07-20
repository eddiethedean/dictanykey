from typing import Any, Iterable, Iterator, Mapping, Optional, Protocol, TypeVar, Union, runtime_checkable
from dictanykey.utils import quote_string

@runtime_checkable
class AnyKeyMapping(Protocol):
    def __init__(self, data: list) -> None:
        ...

    def __len__(self) -> int:
        ...

    def __getitem__(self, key: Any) -> Any:
        ...

    def __setitem__(self, key: Any, value: Any) -> None:
        ...

    def _get_keys_list(self) -> list:
        ...

    def _get_items_list(self) -> list:
        ...

    def get(self, key: Any) -> Any:
        ...


class MappingMixin:
    def __getitem__(self: AnyKeyMapping, key: Any) -> Any:
        if key in self._get_keys_list():
            return self.get(key)
        else:
            raise KeyError(key)

    def __str__(self: AnyKeyMapping) -> str:
        d = ', '.join(f'{quote_string(key)}: {quote_string(value)}' for key, value in self._get_items_list())
        return '{' + f'{d}' + '}'

    def __iter__(self: AnyKeyMapping) -> Iterator:
        return iter(self._get_keys_list())

    def __eq__(self: AnyKeyMapping, other: Mapping) -> bool:
        if not {'__len__', '__contains__', '__getitem__'}.issubset(dir(other)):
            return False
        if len(self) != len(other):
            return False
        for key in self._get_keys_list():
            if key not in other:
                return False
            if self[key] != other[key]:
                return False
        return True

    def __len__(self: AnyKeyMapping) -> int:
        return len(self._get_keys_list())

    def _get_values_list(self: AnyKeyMapping) -> list[Any]:
        return [self[key] for key in self._get_keys_list()]

    def _get_items_list(self: AnyKeyMapping) -> list[tuple]:
        return [(key, self[key]) for key in self._get_keys_list()]

    def copy(self: AnyKeyMapping):
        copy = self.__new__(type(self))
        copy.__init__(self._get_items_list())
        return copy

    def setdefault(self: AnyKeyMapping, key: Any, default: Optional[Any] = None) -> Any:
        """Insert key with a value of default if key is not in the dictionary.

           Return the value for key if key is in the dictionary, else default.
        """
        if key not in self:
            self[key] = default
            return default
        return key

    Choosable = TypeVar("Choosable", Iterable, AnyKeyMapping)

    def update(self: AnyKeyMapping, data: Optional[Choosable] = None) -> None:
        """Update self from dict/iterable data.
           If data is present and has a .keys() method, then does:  for k in data: self[k] = data[k]
           If data is present and lacks a .keys() method, then does:  for k, v in data: self[k] = v
        """
        if data is None:
            return

        if isinstance(data, AnyKeyMapping):
            for k in data._get_keys_list():
                self[k] = data[k]
        else:
            for k, v in data:
                self[k] = v