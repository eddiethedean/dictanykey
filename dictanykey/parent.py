from typing import Protocol


class Parent(Protocol):
    def _get_keys_list(self) -> list:
        ...

    def _get_values_list(self) -> list:
        ...

    def _get_items_list(self) -> list:
        ...

    def __len__(self) -> int:
        ...