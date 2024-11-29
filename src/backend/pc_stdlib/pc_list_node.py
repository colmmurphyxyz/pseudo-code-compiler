from __future__ import annotations

class PcListNode:
    next: PcListNode
    prev: PcListNode
    key: any

    def __init__(self, next: PcListNode, prev: PcListNode, key: any = None):
        self.prev = prev
        self.next = next
        self.key = key

    def __str__(self) -> str:
        return f"Node({str(self.key)})"

def NEW_LISTNODE(key: any, next: PcListNode, prev: PcListNode) -> PcListNode:
    return PcListNode(next, prev, key)