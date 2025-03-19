# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import sys
import pathlib

from pcc.backend.pc_stdlib import PcVertex, PcGraph, PcArray

# add the parent directory (repository root) to sys.path
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))


def make_graph():
    adjmat = PcArray.from_py_list([ PcArray.from_py_list([ 0 for _ in range(5)], 1) for _ in range(5) ])
    adjmat[1][2] = 10
    adjmat[1][4] = 5
    adjmat[2][3] = 1
    adjmat[2][4] = 2
    adjmat[3][5] = 4
    adjmat[4][2] = 3
    adjmat[4][3] = 9
    adjmat[4][5] = 2
    adjmat[5][3] = 6
    adjmat[5][1] = 7

    return PcGraph(adjmat)