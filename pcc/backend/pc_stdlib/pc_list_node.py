# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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

def NEW_LIST_NODE(key: any, value: any = None, next: PcListNode | None = None, prev: PcListNode | None = None) -> PcListNode:
    return PcListNode(next, prev, key, value)