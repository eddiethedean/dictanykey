from typing import Any


class Parent:
    def _get_keys_list(self) -> list[Any]:
        raise NotImplementedError

    def _get_values_list(self) -> list[Any]:
        raise NotImplementedError

    def _get_items_list(self) -> list[tuple[Any, Any]]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
