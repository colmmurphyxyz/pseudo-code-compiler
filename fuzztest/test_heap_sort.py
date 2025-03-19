# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import sys
import pathlib
import unittest

from pcc.backend.pc_stdlib import PcArray

# add the parent directory (repository root) to sys.path
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from res.transpiled_pc_examples.ch06.heapsort import HEAPSORT

class TestHeapSort(unittest.TestCase):
    def test_heap_sort(self):
        n = 5
        a = PcArray.from_py_list([4, 2, 1, 5, 3], 1)
        HEAPSORT(a, n)
        self.assertListEqual(a._elems, [1, 2, 3, 4, 5])

    def test_sort_empty_list(self):
        n = 0
        a = PcArray.from_py_list([], 1)
        HEAPSORT(a, n)
        self.assertListEqual(a._elems, [])

    def test_sort_descending_list(self):
        n = 5
        a = PcArray.from_py_list([5, 4, 3, 2, 1], 1)
        HEAPSORT(a, n)
        self.assertListEqual(a._elems, [1, 2, 3, 4, 5])

    def test_sort_ascending_list(self):
        n = 5
        a = PcArray.from_py_list([1, 2, 3, 4, 5], 1)
        HEAPSORT(a, n)
        self.assertListEqual(a._elems, [1, 2, 3, 4, 5])