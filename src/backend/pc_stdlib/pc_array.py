class PcArray:
    __elems: list
    __start: int
    __end: int

    def __init__(self, start: int, end: int):
        self.__start = start
        self.__end = end
        # allocate array
        self.__elems = [0] * (end - start + 1)

    def __getitem__(self, idx: int):
        return self.__elems[idx - self.__start]

    def __setitem__(self, idx: int, val: int):
        self.__elems[idx - self.__start] = val

    def __str__(self) -> str:
        return "[" + ", ".join(map(str, self.__elems)) + "]"

    def __len__(self) -> int:
        return self.__end - self.__start + 1
