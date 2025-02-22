import sys
import pathlib
import unittest

from pcc.backend.pc_stdlib import PcArray

# add the parent directory (repository root) to sys.path.n
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from res.transpiled_pc_examples.ch04.matrix_multiply import MATRIX_MULTIPLY as pc_matrix_multiply

class TestMatrixMultiple(unittest.TestCase):

    def test_matrix_multiply(self):
        A = PcArray(1, 2)
        B = PcArray(1, 2)
        C = PcArray(1, 2)
        A[1] = PcArray.from_py_list([1, 2], 1)
        A[2] = PcArray.from_py_list([3, 4], 1)
        B[1] = PcArray.from_py_list([5, 6], 1)
        B[2] = PcArray.from_py_list([7, 8], 1)
        C[1] = PcArray.from_py_list([0, 0], 1)
        C[2] = PcArray.from_py_list([0, 0], 1)
        pc_matrix_multiply(A, B, C, 2)
        w = C[1][1]
        x = C[1][2]
        y = C[2][1]
        z = C[2][2]
        self.assertEqual(w, 19)
        self.assertEqual(x, 22)
        self.assertEqual(y, 43)
        self.assertEqual(z, 50)

    def test_multipy_by_identity_matrix(self):
        A = PcArray(1, 2)
        B = PcArray(1, 2)
        C = PcArray(1, 2)
        A[1] = PcArray.from_py_list([1, 2], 1)
        A[2] = PcArray.from_py_list([3, 4], 1)
        B[1] = PcArray.from_py_list([1, 0], 1)
        B[2] = PcArray.from_py_list([0, 1], 1)
        C[1] = PcArray.from_py_list([0, 0], 1)
        C[2] = PcArray.from_py_list([0, 0], 1)
        pc_matrix_multiply(A, B, C, 2)
        w = C[1][1]
        x = C[1][2]
        y = C[2][1]
        z = C[2][2]
        self.assertEqual(w, 1)
        self.assertEqual(x, 2)
        self.assertEqual(y, 3)
        self.assertEqual(z, 4)