import sys
import pathlib
import unittest

from pcc.backend.pc_stdlib import PcArray

# add the parent directory (repository root) to sys.path
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from res.transpiled_pc_examples.ch09.minimum import MINIMUM

class TestMinimum(unittest.TestCase):
    def test_minimum(self):
        n = 5
        a = PcArray.from_py_list([4, 2, 1, 5, 3], 1)
        b = MINIMUM(a, n)
        self.assertEqual(b, 1)
