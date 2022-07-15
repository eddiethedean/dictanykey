from typing import Mapping, Any, Iterable, Optional
from dictanykey.iterables import DictItems, DictKeys, DictValues

from dictanykey.mapping_mixin import MappingMixin


class UnHashMap(MappingMixin):
    """A dictionary where the keys don't need to be hashable.
       Stores keys in _keys: list
       Stores values in _values: list

       Uses == to compare keys rather than hash function

       Much slower key lookup speeds compared to dict but
       keys don't need to be hashable.
    """
    def __init__(self, data: Optional[Iterable] = None) -> None:
        self._keys: list = []
        self._values: list = []
        if isinstance(data, Mapping):
            data = data.items()
        if data is not None:
            for key, value in data:
                self[key] = value

    def __contains__(self, value: Any) -> bool:
        return value in self.keys()
            
    def __setitem__(self, key: Any, value: Any) -> None:
        if key not in self.keys():
            self._keys.append(key)
            self._values.append(value)
        else:
            i = self._getindex(key)
            self._values[i] = value
            
    def _getindex(self, key: Any) -> int:
        try:
            return self._keys.index(key)
        except ValueError as e:
            raise KeyError(key)
        
    def __delitem__(self, key: Any) -> None:
        i = self._getindex(key)
        del self._keys[i]
        del self._values[i]

    def __repr__(self) -> str:
        return f'UnHashMap({[(key, value) for key, value in self.items()]})'
    
    def keys(self) -> DictKeys:
        return DictKeys(self._keys)
    
    def values(self) -> DictValues:
        return DictValues(self._values)
    
    def items(self) -> DictItems:
        return DictItems([(key, value) for key, value in zip(self._keys, self._values)])
    
    def get(self, key, default: Optional[Any] = None) -> Any:
        try:
            i = self._getindex(key)
        except KeyError as e:
            if default is None:
                raise e
            else:
                return default
        return self._values[i]
    
    # TODO: update method

    # TODO: pop method

    # TODO: popitem method

    # TODO: clear method

    # TODO: setdefault method
    
    # TODO: fromkeys method