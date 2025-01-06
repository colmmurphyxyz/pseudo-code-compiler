class Stack:
    def __init__(self):
        self._elems = []

    def push(self, elem):
        self._elems.append(elem)
        return self

    def pop(self):
        return self._elems.pop()

    def pop_next(self, n: int) -> list:
        results = []
        for _ in range(n):
            results.append(self.pop())
        return results

    def size(self) -> int:
        return len(self._elems)
