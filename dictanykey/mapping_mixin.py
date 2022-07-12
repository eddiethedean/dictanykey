from typing import Iterator, Mapping
from dictanykey.utils import quote_string


class MappingMixin(Mapping):
    def __getitem__(self, key):
        return self.get(key)

    def __str__(self) -> str:
        d = ', '.join(f'{quote_string(key)}: {quote_string(value)}' for key, value in self.items())
        return '{' + f'{d}' + '}'

    def __iter__(self) -> Iterator:
        return iter(self.keys())

    def __eq__(self, other: Mapping) -> bool:
        if not isinstance(other, Mapping):
            return False
        if len(self) != len(other):
            return False
        for key in self.keys():
            if key not in other:
                return False
            if self[key] != other[key]:
                return False
        return True

    def __len__(self) -> int:
        return len(self.keys())

    def copy(self):
        copy = self.__new__(type(self))
        copy.__init__(self.items())
        return copy