from typing import Any, Callable, Iterable, Optional, Protocol

class Factory(Protocol):
    __name__: str
    def __call__(self):
        ...


class DefaultAnyKeyMapping(Protocol):
    default_factory: Optional[Factory] = None
    data: Optional[Iterable] = None

    def __init__(
        self,
        default_factory: Optional[Factory] = None, /,
        data: Optional[Iterable] = None
    ):
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

from abc import ABC, abstractmethod

class AnyKeyMapping(ABC):
    @abstractmethod
    def __init__(self, data) -> None:
        ...

    @abstractmethod
    def __getitem__(self, key: Any) -> Any:
        ...


class DefaultMixin:
    def __init__(
        self: DefaultAnyKeyMapping,
        default_factory: Optional[Callable] = None, /,
        data: Optional[Iterable] = None
    ) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
        if default_factory is not None:
            try:
                default_factory()
            except TypeError:
                raise TypeError('first argument must be callable or None')
        super().__init__(data)
        self.default_factory = default_factory

    def __getitem__(self: DefaultAnyKeyMapping, key: Any) -> Any:
        try:
            return super().__getitem__(key)
        except KeyError as e:
            if self.default_factory is None:
                raise e
            self[key] = self.default_factory()
            return self[key]

    def __repr__(self: DefaultAnyKeyMapping) -> str:
        try:
            if self.default_factory is not None:
                name = self.default_factory.__name__
            else:
                name = None
        except AttributeError:
            name = self.default_factory
        return f'{type(self).__name__}({name}, {[(key, value) for key, value in self._get_items_list()]})'

    def copy(self: DefaultAnyKeyMapping):
        return type(self)(self.default_factory, self._get_items_list())