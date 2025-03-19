# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
        return f"Queue{', '.join( [ str(e) for e in self.__elems[1:] ] )}"

    __repr__ = __str__

    def __len__(self) -> int:
        if self.tail >= self.head:
            return self.tail - self.head
        else:
            return self.size + self.tail - self.head

def NEW_QUEUE(size: int) -> PcQueue:
    return PcQueue(size)
