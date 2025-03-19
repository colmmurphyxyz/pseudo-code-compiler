# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import sys
import pathlib
import unittest

from pcc.backend.pc_stdlib import PcVertex
from res.python_examples.ch19.disjoint_set_list import union

# add the parent directory (repository root) to sys.path
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from graph_utils import make_graph
from res.transpiled_pc_examples.ch20.dijkstra import DIJKSTRA

class TestDijkstra(unittest.TestCase):
    def test_dijkstra(self):
        g = make_graph()
        adjmat = g._adjacency_matrix
        def w(u, k):
            return adjmat[u.key][k.key]
        DIJKSTRA(g, w, g.V[1])
        vertices: list[PcVertex | None] = [ None for _ in range(6) ]
        for v in g.V:
            vertices[v.key] = v
        self.assertIsNone(vertices[1].pi)
        self.assertEqual(vertices[1].d, 0)
        self.assertEqual(vertices[2].pi, vertices[4])
        self.assertEqual(vertices[2].d, 8)
        self.assertEqual(vertices[3].pi, vertices[2])
        self.assertEqual(vertices[3].d, 9)
        self.assertEqual(vertices[4].pi, vertices[1])
        self.assertEqual(vertices[4].d, 5)
        self.assertEqual(vertices[5].pi, vertices[4])
        self.assertEqual(vertices[5].d, 7)