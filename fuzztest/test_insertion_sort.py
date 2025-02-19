import sys
import pathlib
import unittest
from random import randint

# add the parent directory (repository root) to sys.path.n
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from pcc.backend.pc_stdlib import *
from res.transpiled_pc_examples.ch02.insertion_sort import INSERTION_SORT as pc_insertion_sort
from res.python_examples.ch02.insertion_sort import insertion_sort as py_insertion_sort

from fuzz_test_runner import FuzzTestRunner
from utils import random_list, compare_lists


def _input_generator():
    input_length = randint(0, 100)
    input_min = randint(-100, 10)
    input_max = randint(input_min + 1, 100)
    start_idx = 1
    pc_array, py_array = random_list(input_min, input_max, input_length, start_idx)
    return (pc_array, input_length), (py_array, input_length)

def _output_comparator(pc_output, py_output):
    return pc_output._elems == py_output

class TestInsertionSort(unittest.TestCase):

    def test_insertion_sort(self):
        ftr = FuzzTestRunner(100, _input_generator, (pc_insertion_sort, py_insertion_sort), _output_comparator, inplace_output_key=lambda x: x[0])
        ftr.run_trials()

