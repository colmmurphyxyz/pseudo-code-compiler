# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import sys
import pathlib
import unittest

from pcc.backend.pc_stdlib import NEW_QUEUE

# add the parent directory (repository root) to sys.path
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from res.transpiled_pc_examples.ch10.queue import ENQUEUE, DEQUEUE

class TestQueue(unittest.TestCase):
    def test_queue(self):
        q = NEW_QUEUE(10)
        ENQUEUE(q, 1)
        ENQUEUE(q, 2)
        self.assertEqual(DEQUEUE(q), 1)
        self.assertEqual(DEQUEUE(q), 2)