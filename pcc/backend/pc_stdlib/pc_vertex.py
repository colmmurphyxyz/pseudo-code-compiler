# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

class PcVertex:
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, value):
        self._d = value

    @property
    def pi(self):
        return self._pi

    @pi.setter
    def pi(self, value):
        self._pi = value

    def __init__(self, key: any):
        self.key = key
        self._color = None
        self._d = None
        self._pi = None

    def __eq__(self, other: PcVertex) -> bool:
        return self.key == other.key

    def __str__(self) -> str:
        return f"Vertex({self.key}, {('pi=' + str(self._pi.key)) if self._pi is not None else ''}, {self._color=}, {self._d=})"

    __repr__ = __str__