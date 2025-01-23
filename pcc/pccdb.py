from pdb import Pdb
import sys
from types import FrameType
import pathlib

__all__ = ["Pccdb", "set_trace"]


class Pccdb(Pdb):
    __pc_source: list[str]
    __source_directory: str

    @property
    def pc_source(self) -> list[str]:
        return self.__pc_source

    @property
    def source_directory(self) -> str:
        return self.__source_directory

    def __init__(self, pc_source: str):
        pdb_output = open("temp.txt", "a", encoding="utf8")
        super().__init__(stdin=sys.stdin, stdout=pdb_output, readrc=False)

        self.prompt = "(Pccdb) "
        self.__pc_source = pc_source.splitlines()
        self.__source_directory = str(pathlib.Path(__file__).parent.absolute())


    def set_next(self, frame: FrameType):
        filename: str = frame.f_globals["__file__"]
        py_line_number: int = frame.f_lineno
        with open(filename, 'r') as file:
            lines: list[str] = file.readlines()
        print("###", lines[py_line_number].strip())
        pc_line_number: int = int(lines[py_line_number].split("# l:")[1])
        print(f"PC Line Number {pc_line_number}")
        pc_line: str = self.__pc_source.splitlines()[pc_line_number - 1]
        print("@@@", pc_line)
        super().set_trace(frame)

    def do_list(self, arg):
        print("FGHJK")
        self.message("Listing source code")
        print(type(arg), repr(arg))
        super().do_list(arg)

    def do_l(self, arg):
        print("take this L bozo")

    def do_longlist(self, arg):
        self.do_list(arg)

def set_trace(pc_source_file: str, *, header=None):
    with open(pc_source_file, "r") as file:
        pc_source: str = file.read()
    pdb = Pccdb(pc_source)
    print("Created Pccdb instance", sys._getframe())
    if header is not None:
        pdb.message(header)
    pdb.set_trace(sys._getframe().f_back)
