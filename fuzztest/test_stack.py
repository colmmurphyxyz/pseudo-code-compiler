# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import sys
import pathlib
import unittest

from pcc.backend.pc_stdlib import NEW_STACK

# add the parent directory (repository root) to sys.path
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from res.transpiled_pc_examples.ch10.stack import STACK_EMPTY, PUSH, POP

class TestStack(unittest.TestCase):
    def test_stack_empty(self):
        s = NEW_STACK(5)
        self.assertTrue(STACK_EMPTY(s))
        PUSH(s, 3)
        self.assertFalse(STACK_EMPTY(s))

    def test_push_pop(self):
        s = NEW_STACK(5)
        PUSH(s, 3)
        self.assertEqual(POP(s), 3)
        self.assertTrue(STACK_EMPTY(s))
        PUSH(s, 6)
        PUSH(s, 7)
        PUSH(s, 9)
        self.assertEqual(POP(s), 9)