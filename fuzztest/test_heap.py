import sys
import pathlib
import unittest

from pcc.backend.pc_stdlib import PcArray

# add the parent directory (repository root) to sys.path
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from res.transpiled_pc_examples.ch06.heap import PARENT, LEFT, RIGHT, BUILD_MIN_HEAP, MIN_HEAP_MINIMUM, EXTRACT_MIN


def _is_valid_min_heap(nums: list[int], i: int = 0) -> bool:
    if i >= len(nums):
        return True
    if i * 2 + 1 < len(nums):
        if nums[i] > nums[i * 2 + 1]:
            return False
    if i * 2 + 2 < len(nums):
        if nums[i] > nums[i * 2 + 2]:
            return False
    return _is_valid_min_heap(nums, i * 2 + 1) and _is_valid_min_heap(nums, i * 2 + 2)

class TestHeap(unittest.TestCase):
    def test_min_heapify(self):
        heap = PcArray.from_py_list([5, 4, 3, 2, 1], 1)
        BUILD_MIN_HEAP(heap, 5)
        self.assertTrue(_is_valid_min_heap(heap._elems))

    def test_min_heap_minimum(self):
        heap = PcArray.from_py_list([5, 3, 7, 9, -1], 1)
        BUILD_MIN_HEAP(heap, 5)
        self.assertEqual(MIN_HEAP_MINIMUM(heap), -1)

    def test_extract_min(self):
        heap = PcArray.from_py_list([5, 3, 7, 9, -1], 1)
        BUILD_MIN_HEAP(heap, 5)
        self.assertEqual(MIN_HEAP_MINIMUM(heap), -1)
        minimum_element = EXTRACT_MIN(heap)
        self.assertEqual(minimum_element, -1)
        self.assertEqual(heap.heap_size, 4)
        self.assertTrue(_is_valid_min_heap(heap._elems))
        self.assertSetEqual(set(heap._elems), {5, 3, 7, 9})