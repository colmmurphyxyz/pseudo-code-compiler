import sys
import pathlib
# add the source directory to sys.path. This is not a permanent solution
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
from pcc.backend.pc_stdlib import *

from random import randint

def random_list(min_val: int, max_val: int, length: int, start_idx: int) -> tuple[PcArray, list[int]]:
    pc_array = PcArray(start_idx, start_idx + length - 1)
    python_list = []
    for i in range(length):
        val = randint(min_val, max_val)
        pc_array[start_idx + i] = val
        python_list.append(val)
    return pc_array, python_list

def compare_lists(pc_array: PcArray, python_list: list[int], start_idx: int, length: int) -> bool:
    for i in range(length):
        if pc_array[start_idx + i] != python_list[i]:
            return False
    return True