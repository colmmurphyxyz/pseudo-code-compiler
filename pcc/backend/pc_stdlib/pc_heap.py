from typing import Any

from .pc_array import PcArray

class PcHeap:

    @property
    def heap_size(self) -> int:
        return self._heap_size

    @heap_size.setter
    def heap_size(self, value: int):
        self._heap_size = value

    def __init__(self, size: int):
        self._heap_size = 0
        self._size: int = size
        self.array = PcArray(1, size)

    def __getitem__(self, idx: int) -> Any:
        if idx < 1 or idx > self._size:
            raise IndexError(f"Index {idx} out of range for heap of size {self._heap_size}")
        return self.array[idx]

    def __setitem__(self, idx: int, val: Any):
        if idx < 1 or idx > self._size:
            raise IndexError(f"Index {idx} out of range for heap of size {self._heap_size}")
        self.array[idx] = val

    def __str__(self) -> str:
        return "[" + ", ".join(map(str, self.array.elems)) + "]"

    __repr__ = __str__

    def __len__(self) -> int:
        return self._heap_size


def NEW_HEAP(size: int) -> PcHeap:
    return PcHeap(size)