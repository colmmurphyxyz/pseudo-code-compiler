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

