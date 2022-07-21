from typing import Any, Iterable, Iterator, Mapping, Optional, Protocol, runtime_checkable
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


def anykey_getitem(d: AnyKeyMapping, key: Any) -> Any:
    if key in d._get_keys_list():
        return d.get(key)
    else:
        raise KeyError(key)

def anykey_str(d: AnyKeyMapping) -> str:
    s = ', '.join(f'{quote_string(key)}: {quote_string(value)}' for key, value in d._get_items_list())
    return '{' + f'{s}' + '}'

def anykey_iter(d: AnyKeyMapping) -> Iterator:
    return iter(d._get_keys_list())

def anykey_eq(d: AnyKeyMapping, other: Mapping) -> bool:
    if not {'__len__', '__contains__', '__getitem__'}.issubset(dir(other)):
        return False
    if len(d) != len(other):
        return False
    for key in d._get_keys_list():
        if key not in other:
            return False
        if d[key] != other[key]:
            return False
    return True

def anykey_len(d: AnyKeyMapping) -> int:
    return len(d._get_keys_list())

def anykey_copy(d: AnyKeyMapping):
    copy = d.__new__(type(d))
    copy.__init__(d._get_items_list())
    return copy

def anykey_setdefault(d: AnyKeyMapping, key: Any, default: Optional[Any] = None) -> Any:
    """Insert key with a value of default if key is not in the dictionary.

        Return the value for key if key is in the dictionary, else default.
    """
    if key not in d:
        d[key] = default
        return default
    return key

def anykey_update(d: AnyKeyMapping, data: Optional[Iterable | AnyKeyMapping] = None) -> None:
    """Update dict from dict/iterable data.
       If data is present and has a .keys() method, then does:  for k in data: self[k] = data[k]
       If data is present and lacks a .keys() method, then does:  for k, v in data: self[k] = v
    """
    if data is None:
        return

    if isinstance(data, AnyKeyMapping):
        for k in data._get_keys_list():
            d[k] = data[k]
    else:
        for k, v in data:
            d[k] = v