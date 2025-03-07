import sys
import pathlib
import unittest

from pcc.backend.pc_stdlib import PcVertex

# add the parent directory (repository root) to sys.path
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from graph_utils import make_graph
from res.transpiled_pc_examples.ch20.graph_bfs import BFS

class TestGraphBFS(unittest.TestCase):
    def test_bfs(self):
        g = make_graph()
        BFS(g, g.V[1])
        vertices: list[PcVertex | None] = [ None for _ in range(6) ]
        for v in g.V:
            vertices[v.key] = v
        self.assertIsNone(vertices[1].pi)
        self.assertEqual(vertices[1].d, 0)
        self.assertEqual(vertices[2].pi, vertices[1])
        self.assertEqual(vertices[2].d, 1)
        self.assertEqual(vertices[3].pi, vertices[2])
        self.assertEqual(vertices[3].d, 2)
        self.assertEqual(vertices[4].pi, vertices[1])
        self.assertEqual(vertices[4].d, 1)
        self.assertEqual(vertices[5].pi, vertices[4])
        self.assertEqual(vertices[5].d, 2)
