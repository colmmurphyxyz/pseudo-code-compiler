class PcStack:
    size: int
    top: int
    __elems: list

    def __init__(self, size: int):
        self.size = size
        self.top = 0
        # Over-allocate elems to account for 1-based indexing
        self.__elems = [None]

    def __getitem__(self, idx: int):
        return self.__elems[idx]

    def __setitem__(self, idx: int, value):
        self.__elems[idx] = value

def NEW_STACK(size: int) -> PcStack:
    return PcStack(size)
