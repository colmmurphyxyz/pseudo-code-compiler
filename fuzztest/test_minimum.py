# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
