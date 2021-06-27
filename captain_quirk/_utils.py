from typing import List, Optional, Union
from itertools import zip_longest


EMPTY = 1


class AbstractGate:
    __slots__ = "_label", "_param"

    def __init__(self, label: str, param: Optional[float] = None) -> None:
        self._label = label
        self._param = param

    def to_json(self):
        if self._param is None:
            return self._label
        return {"id": self._label, "arg": str(self._param)}


class AbstractSyntaxGrid:
    __slots__ = "_columns"

    def __init__(self) -> None:
        self._columns = []

    def append(self, column: List[Union[int, AbstractGate]]):
        try:
            self._merge(column)
        except IndexError:
            self._columns.append(column)

    def _merge(self, column: List[Union[int, AbstractGate]]):
        new_column = []
        for old, new in zip_longest(self._columns[-1], column, fillvalue=EMPTY):
            if old == EMPTY:
                new_column.append(new)
            elif new == EMPTY:
                new_column.append(old)
            else:
                raise IndexError
        self._columns[-1] = new_column

    def to_json(self):
        result = [
            [element.to_json() if element != EMPTY else element for element in column]
            for column in self._columns
        ]
        return result
