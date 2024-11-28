class PcQueue:
    def __init__(self, size: int):
        self.size: int = size
        self.head = 1
        self.tail = 1
        # over-allocate to accommodate 1-based indexing
        self.__elems = [None] * (size + 1)

    def __getitem__(self, idx: int):
        return self.__elems[idx]

    def __setitem__(self, idx: int, value):
        self.__elems[idx] = value

    def __str__(self) -> str:
        return f"Queue{', '.join( [ str(e) for e in self.__elems ] )}"

def NEW_QUEUE(size: int) -> PcQueue:
    return PcQueue(size)
