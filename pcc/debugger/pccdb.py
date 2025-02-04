from .ansi_color_codes import Style
from pdb import Pdb
import sys
import re

__all__ = ["Pccdb", "set_trace"]

from typing import Any, Mapping


class Pccdb(Pdb):
    active_instance = None

    __pc_source_lines: list[str]

    @property
    def pc_source_lines(self) -> list[str]:
        return self.__pc_source_lines

    def __init__(self, pc_source: str):
        Pccdb.active_instance = self
        self.__pc_source_lines = pc_source.splitlines()
        super().__init__(stdin=sys.stdin, stdout=sys.stdout, readrc=False)
        print(self.cmdqueue)


    def __del__(self):
        # self._pdb_out.close()
        if self is Pccdb.active_instance:
            Pccdb.active_instance = None

    def get_locals(self) -> Mapping[str, Any]:
        return self.curframe_locals

    def get_locals_sanitised(self) -> dict[str, any]:
        local_variables = self.get_locals()
        hidden_names = { "__name__", "__doc__", "__package__", "__loader__", "__spec__", "__annotations__",
                         "__builtins__", "__file__", "__cached__", "pathlib", "sys", "set_trace",
                         "__pdb_convenience_variables"}
        return {k: v for k, v in local_variables.items() if k not in hidden_names}

    def get_globals(self) -> dict[str, Any]:
        return self.curframe.f_globals

    def get_globals_sanitised(self) -> dict[str, Any]:
        hidden_names = {"__name__", "__doc__", "__package__", "__loader__", "__spec__", "__annotations__",
                        "__builtins__", "__file__", "__cached__", "pathlib", "sys", "set_trace",
                        "__pdb_convenience_variables"}
        return {k: v for k, v in self.get_globals().items() if k not in hidden_names}

    def _has_line_marker(self, line: str) -> bool:
        return len(re.findall(r"# l:\d+", line)) > 0

    def _is_internal_frame(self, frame) -> bool:
        return frame.f_code.co_filename == "/home/colm/PycharmProjects/pcc_fixed/pcc/output.py"

    def user_call(self, frame, argument_list):
        if not self._is_internal_frame(frame):
            # move the return point of the given frame
            self.set_return(frame)
            # execute final line of the current function on the next iteration of the cmdloop
            self.cmdqueue = ["next"] + self.cmdqueue
        super().user_call(frame, argument_list)

    def user_line(self, frame):
        # print current line to the console
        super().user_line(frame)

    def do_next(self, arg):
        print("DO_NEXT")
        self.set_next(self.curframe)
        return 1

    do_n = do_next

    def do_step(self, arg):
        print("DO_STEP")
        self.set_step()
        return 1

    do_s = do_step

    do_z = do_step

    def precmd(self, line):
        print("PreCmd", self.curframe.f_lineno)
        return super().precmd(line)

    def postcmd(self, stop, line):
        import inspect
        source, _ = inspect.findsource(self.curframe)
        py_lineno = self.curframe.f_lineno
        py_line = source[py_lineno - 1].strip()
        if self._has_line_marker(py_line):
            pc_line = int(py_line.split("l:")[-1])
            print(f"{Style.RED}{py_lineno=} @ {source[py_lineno - 1].strip()}{Style.RESET}")
            print(f"{Style.BLUE}{pc_line=} @ {self.pc_source_lines[pc_line - 1].strip()}{Style.RESET}")
        return super().postcmd(stop, line)


def set_trace(pc_source_code: str, *, header=None):
    pdb = Pccdb(pc_source_code)
    if header is not None:
        pdb.message(header)
    pdb.set_trace(sys._getframe().f_back)
