# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from .pc_list_node import PcListNode

class PcLinkedList:
    head: PcListNode | None
    tail: PcListNode | None

    def __init__(self, head: PcListNode | None = None, tail: PcListNode | None = None):
        self.head = head
        self.tail = tail

    def __str__(self) -> str:
        elems: [PcListNode] = []
        if not self.head:
            return "LinkedList()"
        x = self.head
        while x:
            elems.append(x)
            x = x.next
        elems = [ str(elem) for elem in elems ]
        return f"LinkedList({', '.join(elems)})"

def NEW_LINKED_LIST(head: PcListNode | None = None, tail: PcListNode | None = None) -> PcLinkedList:
    return PcLinkedList(head, tail)

