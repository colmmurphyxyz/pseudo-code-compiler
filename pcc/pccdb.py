from pdb import Pdb
import sys
from types import FrameType

__all__ = ["Pccdb", "set_trace"]

class Pccdb(Pdb):
    def _init__(self):
        super().__init__(stdin=sys.stdin, stdout=sys.stdout, readrc=False)

    def set_next(self, frame: FrameType):
        filename: str = frame.f_globals["__file__"]
        line_number: int = frame.f_lineno
        with open(filename, 'r') as file:
            lines: list[str] = file.readlines()
        print("###", lines[line_number])
        super().set_trace(frame)

def set_trace(*, header=None):
    pdb = Pccdb()
    print("Created Pccdb instance", sys._getframe())
    if header is not None:
        pdb.message(header)
    pdb.set_trace(sys._getframe().f_back)