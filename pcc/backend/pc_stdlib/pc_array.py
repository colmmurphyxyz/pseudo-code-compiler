class PcArray:
    _elems: list
    _start: int
    _end: int

    def __init__(self, start: int, end: int):
        self._start = start
        self._end = end
        # allocate array
        self._elems = [0] * (end - start + 1)

    def __getitem__(self, idx: int):
        if idx < self._start or idx > self._end:
            raise IndexError(f"Index {idx} out of range for array of indexable range [{self._start}, {self._end}]")
        return self._elems[idx - self._start]

    def __setitem__(self, idx: int, val: int):
        if idx < self._start or idx > self._end:
            raise IndexError(f"Index {idx} out of range for array of indexable range [{self._start}, {self._end}]")
        self._elems[idx - self._start] = val

    def __str__(self) -> str:
        return "[" + ", ".join(map(str, self._elems)) + "]"

    __repr__ = __str__

    def __len__(self) -> int:
        return self._end - self._start + 1

def NEW_ARRAY(start: int, end: int) -> PcArray:
    return PcArray(start, end)

if __name__ == "__main__":
    a = PcArray(1, 5)
    print(a)
    print(a._elems)
