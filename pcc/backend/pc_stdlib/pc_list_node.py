from __future__ import annotations

class PcListNode:
    next: PcListNode | None
    prev: PcListNode | None
    key: any
    value: any

    def __init__(self, next: PcListNode | None, prev: PcListNode | None, key: any = None, value: any = None):
        self.prev = prev
        self.next = next
        self.key = key
        self.value = value

    def __str__(self) -> str:
        return f"ListNode({str(self.key)})"

def NEW_LIST_NODE(key: any, value: any, next: PcListNode | None = None, prev: PcListNode | None = None) -> PcListNode:
    return PcListNode(next, prev, key, value)