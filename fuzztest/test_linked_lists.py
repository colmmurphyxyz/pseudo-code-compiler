# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import sys
import pathlib
import unittest

from pcc.backend.pc_stdlib import NEW_LINKED_LIST, NEW_LIST_NODE

# add the parent directory (repository root) to sys.path
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from res.transpiled_pc_examples.ch10.list_delete import LIST_DELETE
from res.transpiled_pc_examples.ch10.list_insert import LIST_INSERT
from res.transpiled_pc_examples.ch10.list_search import LIST_SEARCH
from res.transpiled_pc_examples.ch10.list_prepend import LIST_PREPEND

class TestLinkedLists(unittest.TestCase):
    def test_linked_list_insert(self):
        y = NEW_LIST_NODE(1)
        x = NEW_LIST_NODE(2)
        LIST_INSERT(y, x)
        self.assertEqual(y.prev, x)
        self.assertEqual(x.next, y)

    def test_list_prepend(self):
        l = NEW_LINKED_LIST()
        x = NEW_LIST_NODE(1)
        l.head = x
        y = NEW_LIST_NODE(9)
        LIST_PREPEND(l, y)
        self.assertEqual(l.head, y)

    def test_linked_list_delete(self):
        y = NEW_LIST_NODE(1)
        x = NEW_LIST_NODE(2)
        LIST_INSERT(y, x)
        self.assertEqual(y.prev, x)
        self.assertEqual(x.next, y)
        LIST_DELETE(y, x)
        self.assertEqual(y.next, None)
        self.assertEqual(y.prev, None)

    def test_linked_list_search(self):
        l = NEW_LINKED_LIST()
        y = NEW_LIST_NODE(1)
        x = NEW_LIST_NODE(2)
        l.head = x
        LIST_INSERT(y, x)
        found = LIST_SEARCH(l, 2)
        self.assertEqual(found, x)
        self.assertIsNone(LIST_SEARCH(l, 3))
