from __future__ import annotations

from typing import Any

from .pc_array import PcArray


class PcMinHeap:
    def __init__(self, size: int):
        self._size: int = size
        self.array = PcArray(1, size)

    def __getitem__(self, idx: int) -> Any:
        if idx < 1 or idx > self._size:
            raise IndexError(f"Index {idx} out of range for heap of size {self._size}")
        return self.array[idx]

    def __setitem__(self, idx: int, val: Any):
        if idx < 1 or idx > self._size:
            raise IndexError(f"Index {idx} out of range for heap of size {self._size}")
        self.array[idx] = val

    def __str__(self) -> str:
        return "[" + ", ".join(map(str, self.array)) + "]"

    __repr__ = __str__

    def __len__(self) -> int:
        return self._size

def NEW_MINHEAP(size: int) -> PcMinHeap:
    return PcMinHeap(size)