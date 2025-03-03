import sys
import pathlib
import unittest

from pcc.backend.pc_stdlib import PcArray, NEW_LINKED_LIST, NEW_LIST_NODE
from pcc.backend.pc_stdlib import PcLinkedList

# add the parent directory (repository root) to sys.path
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from res.transpiled_pc_examples.ch11.chained_hashing import CHAINED_HASH_INSERT, CHAINED_HASH_SEARCH, CHAINED_HASH_DELETE

class TestChainedHashing(unittest.TestCase):
    def _make_hash_table(self, n: int) -> PcArray:
        hash_table = PcArray.from_py_list([None] * n, 1)
        for i in range(1, n + 1):
            hash_table[i] = NEW_LINKED_LIST()
        return hash_table

    def test_init(self):
        # create PcArray to use as hash table
        n = 10
        hash_table = PcArray.from_py_list([None] * n, 1)
        for i in range(1, n + 1):
            hash_table[i] = NEW_LINKED_LIST()

        self.assertEqual(len(hash_table._elems), n)

    def test_chained_hash_insert(self):
        n = 10
        hash_table = self._make_hash_table(n)
        CHAINED_HASH_INSERT(hash_table, 1, "foo")
        CHAINED_HASH_INSERT(hash_table, 2, "bar")
        CHAINED_HASH_INSERT(hash_table, 3, "baz")

        self.assertEqual(hash_table[1].head.value, "foo")
        self.assertEqual(hash_table[2].head.value, "bar")
        self.assertEqual(hash_table[3].head.value, "baz")

    def test_chained_hash_search(self):
        n = 10
        hash_table = self._make_hash_table(n)
        CHAINED_HASH_INSERT(hash_table, 1, "foo")
        CHAINED_HASH_INSERT(hash_table, 2, "bar")
        CHAINED_HASH_INSERT(hash_table, 1, "baz")

        self.assertEqual(CHAINED_HASH_SEARCH(hash_table, 1), "baz")
        self.assertEqual(CHAINED_HASH_SEARCH(hash_table, 2), "bar")
        self.assertIsNone(CHAINED_HASH_SEARCH(hash_table, 3))

    def test_chained_hash_delete(self):
        n = 10
        hash_table = self._make_hash_table(n)
        CHAINED_HASH_INSERT(hash_table, 1, "foo")
        CHAINED_HASH_INSERT(hash_table, 2, "bar")

        CHAINED_HASH_DELETE(hash_table, 2)
        value = CHAINED_HASH_SEARCH(hash_table, 2)
        self.assertIsNone(value)


