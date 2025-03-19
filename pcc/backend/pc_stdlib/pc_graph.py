# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from .pc_array import PcArray
from .pc_vertex import PcVertex

class PcGraph:
    @property
    def V(self): # return all vertices
        return PcArray.from_py_list(list(self._vertices.values()))

    @property
    def v(self):
        return self.V

    def __init__(self, adjacency_matrix: PcArray):
        self._vertices = {}
        self._adjacency_matrix = adjacency_matrix
        for i in range(len(adjacency_matrix)):
            for j in range(len(adjacency_matrix[i + 1])):
                if adjacency_matrix[i + 1][j + 1] != 0:
                    if i + 1 not in self._vertices.keys():
                        self._vertices[i + 1] = PcVertex(i + 1)
                    if j + 1 not in self._vertices.keys():
                        self._vertices[j + 1] = PcVertex(j + 1)

    def Adj(self, u) -> PcArray:
        adjacent = []
        row = self._adjacency_matrix[u.key]
        for i, weight in enumerate(row):
            if weight != 0:
                adjacent.append(self._vertices[i + 1])
        # for v in self.V:
        #     if self._adjacency_matrix[u.key][v.key] != 0:
        #         adjacent.append(v)
        return PcArray.from_py_list(adjacent)

