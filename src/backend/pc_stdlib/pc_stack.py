class PcStack:
    size: int
    top: int
    __elems: list

    def __init__(self, size: int):
        self.size = size
        self.top = 0
        # Over-allocate elems to account for 1-based indexing
        self.__elems = [None] * (size + 1)

    def __getitem__(self, idx: int):
        return self.__elems[idx]

    def __setitem__(self, idx: int, value):
        self.__elems[idx] = value

    def __str__(self) -> str:
        stack_contents: list = self.__elems[1:self.top + 1]
        if len(stack_contents) == 0:
            return "Stack(EMPTY)"
        stack_repr = ", ".join( [ str(e) for e in stack_contents] )
        return f"Stack({stack_repr})"

def NEW_STACK(size: int) -> PcStack:
    return PcStack(size)
