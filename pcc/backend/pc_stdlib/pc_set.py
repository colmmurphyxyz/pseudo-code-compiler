# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

class PcSet:

    @property
    def elems(self):
        return self._elems

    @staticmethod
    def of(*args):
        return PcSet(*args)

    def __init__(self, *args):
        if len(args) > 0:
            self._elems = set(args)
        else:
            self._elems = set()

    def __iter__(self):
        return self._elems.__iter__()

    def __len__(self):
        return len(self._elems)

    def __or__(self, other):
        return PcSet(*self._elems.union(other.elems))

    def __and__(self, other):
        return PcSet(*self._elems.intersection(other.elems))

    def __add__(self, other):
        return PcSet(*self._elems.union(other.elems))

    def __sub__(self, other):
        return PcSet(self._elems.difference(other.elems))

    def __eq__(self, other):
        return self._elems == other.elems

    def __str__(self):
        return "{" + ", ".join(list(map(str, self._elems))) +"}"

    __repr__ = __str__