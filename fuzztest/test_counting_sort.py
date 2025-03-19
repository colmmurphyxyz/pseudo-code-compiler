# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import sys
import pathlib
import unittest
from random import shuffle

from pcc.backend.pc_stdlib import PcArray

# add the parent directory (repository root) to sys.path
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from res.transpiled_pc_examples.ch08.counting_sort import COUNTING_SORT

class TestCountingSort(unittest.TestCase):
    def test_counting_sort(self):
        n = 10
        nums = [1, 2, 3, 4, 5, 5, 5, 8, 9, 10]
        shuffle(nums)
        a = PcArray.from_py_list(nums, 1)
        b = COUNTING_SORT(a, n, 10)
        self.assertListEqual(b._elems, [1, 2, 3, 4, 5, 5, 5, 8, 9, 10])

    def test_sort_empty_list(self):
        n = 0
        a = PcArray.from_py_list([], 1)
        b = COUNTING_SORT(a, n, 1)
        self.assertListEqual(b._elems, [])

    def test_sort_descending_list(self):
        n = 5
        a = PcArray.from_py_list([5, 4, 3, 2, 1], 1)
        b = COUNTING_SORT(a, n, 5)
        self.assertListEqual(b._elems, [1, 2, 3, 4, 5])

    def test_sort_ascending_list(self):
        n = 5
        a = PcArray.from_py_list([1, 2, 3, 4, 5], 1)
        b = COUNTING_SORT(a, n, 5)
        print(b)
        self.assertListEqual(b._elems, [1, 2, 3, 4, 5])
        # self.assertEqual([1, 2, 3, 4, 5], a._elems)