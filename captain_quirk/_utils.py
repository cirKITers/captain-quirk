from typing import List, Union
from itertools import zip_longest


EMPTY = 1


class AbstractSyntaxGrid:
    __slots__ = "_columns"

    def __init__(self) -> None:
        self._columns = []

    def append(self, column: List[Union[int, str]]):
        try:
            self._merge(column)
        except IndexError:
            self._columns.append(column)

    def _merge(self, column: List[Union[int, str]]):
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
        return self._columns.copy()
