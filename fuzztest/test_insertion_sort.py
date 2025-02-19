import sys
import pathlib
# add the parent directory (repository root) to sys.path.n
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from pcc.backend.pc_stdlib import *
from res.transpiled_pc_examples.ch02.insertion_sort import INSERTION_SORT as pc_insertion_sort
from res.python_examples.ch02.insertion_sort import insertion_sort as py_insertion_sort

from utils import random_list, compare_lists

TRIALS: int = 100
MIN_VAL: int = -100
MAX_VAL: int = 100
LENGTH: int = 100

for i in range(100):
    A, python_list = random_list(MIN_VAL, MAX_VAL, LENGTH, 1)
    pc_insertion_sort(A, LENGTH)
    py_insertion_sort(python_list, LENGTH)
    assert compare_lists(A, python_list, 1, LENGTH)
