from __future__ import annotations

class PcBinaryTree:
    def __init__(self, key: any, left: PcBinaryTree | None = None, right: PcBinaryTree | None = None, parent: PcBinaryTree | None = None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent

    @property
    def p(self) -> PcBinaryTree:
        return self.parent

    @p.setter
    def p(self, value: PcBinaryTree):
        pass

    @property
    def root(self) -> PcBinaryTree:
        x = self
        while x.parent:
            x = x.parent
        return x

    def __str__(self) -> str:
        return f"BinaryTree({str(self.key)})"

    __repr__ = __str__

def NEW_BINARY_TREE(key: any, left: PcBinaryTree | None = None, right: PcBinaryTree | None = None, parent: PcBinaryTree | None = None) -> PcBinaryTree:
    return PcBinaryTree(key, left, right, parent)