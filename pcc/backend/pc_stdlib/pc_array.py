# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from typing_extensions import Any, Iterable


class PcArray(Iterable):
    def __iter__(self):
        return self._elems.__iter__()

    _elems: list
    _start: int
    _end: int

    @property
    def elems(self) -> list:
        return self._elems

    @staticmethod
    def of(*args) -> PcArray:
        return PcArray.from_py_list(list(args), 1)

    def __init__(self, start: int, end: int):
        self._start = start
        self._end = end
        # allocate array
        self._elems = [0] * (end - start + 1)

    def __getitem__(self, idx: int) -> Any:
        if idx < self._start or idx > self._end:
            raise IndexError(f"Index {idx} out of range for array of indexable range [{self._start}, {self._end}]")
        return self._elems[idx - self._start]

    def __setitem__(self, idx: int, val: Any):
        if idx < self._start or idx > self._end:
            raise IndexError(f"Index {idx} out of range for array of indexable range [{self._start}, {self._end}]")
        self._elems[idx - self._start] = val

    def __str__(self) -> str:
        return "[" + ", ".join(map(str, self._elems)) + "]"

    __repr__ = __str__

    def __len__(self) -> int:
        return self._end - self._start + 1

    @staticmethod
    def from_py_list(py_list: list, start_idx: int = 1) -> PcArray:
        n = len(py_list)
        pc_array = PcArray(start_idx, start_idx + n - 1)
        for i in range(n):
            pc_array[start_idx + i] = py_list[i]
        return pc_array

    def to_py_list(self) -> list:
        return self._elems

def NEW_ARRAY(start: int, end: int) -> PcArray:
    return PcArray(start, end)
