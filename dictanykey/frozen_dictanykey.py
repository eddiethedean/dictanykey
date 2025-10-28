from collections.abc import Iterable, Mapping
from typing import Any, Optional, Union

from dictanykey.dictanykey import DictAnyKey
from dictanykey.iterables import OrderedKeys
from dictanykey.unhashmap import UnHashMap


class FrozenDictAnyKey(DictAnyKey):
    """A DictAnyKey that cannot be edited."""

    def __init__(self, data: Optional[Union[Iterable, Mapping]] = None) -> None:
        self._hashmap: dict = {}
        self._unhashmap = UnHashMap()
        self._keys = OrderedKeys()
        if data is None:
            return
        if isinstance(data, Mapping):
            for k in data.keys():
                super().__setitem__(k, data[k])
        else:
            for k, v in data:
                super().__setitem__(k, v)

    def __setitem__(self, key: Any, value: Any) -> None:
        raise TypeError(
            f"'{self.__class__.__name__}' object doesn't support item assignment"
        )

    def __delitem__(self, key: Any) -> None:
        raise TypeError(
            f"'{self.__class__.__name__}' object doesn't support item deletion"
        )

    def clear(self) -> None:
        raise AttributeError(f"'{self.__class__.__name__}' object is read-only")

    def delete(self, key: Any) -> None:
        raise AttributeError(f"'{self.__class__.__name__}' object is read-only")

    def pop(self, key: Any, default: Optional[Any] = None) -> Any:
        raise AttributeError(f"'{self.__class__.__name__}' object is read-only")

    def popitem(self) -> Any:
        raise AttributeError(f"'{self.__class__.__name__}' object is read-only")

    def setdefault(self, key: Any, default: Optional[Any] = None) -> Any:
        raise AttributeError(f"'{self.__class__.__name__}' object is read-only")

    def __repr__(self) -> str:
        return f"FrozenDictAnyKey({[(key, value) for key, value in self._get_items_list()]})"

    def __hash__(self) -> int:
        """Return hash value based on frozenset of items for immutability.
        Note: This will fail if any keys or values are unhashable."""
        try:
            return hash(frozenset(self._get_items_list()))
        except TypeError:
            # If items contain unhashable types, we cannot hash this object
            raise TypeError(f"unhashable type: '{self.__class__.__name__}'") from None
