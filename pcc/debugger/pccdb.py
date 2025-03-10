from pdb import Pdb
import sys
import re
import inspect
from types import FrameType
from typing import Any, Mapping
from copy import copy

from .ansi_color_codes import Style

__all__ = ["Pccdb", "set_trace"]


class Pccdb(Pdb):
    active_instance = None

    __pc_source_lines: list[str]

    __current_py_line: str = ""
    __current_py_lineno: int = 1
    __current_pc_line: str = ""
    __current_pc_lineno: int = 0

    _external_locals: set[str] | None
    _external_globals: set[str] | None

    @property
    def pc_source_lines(self) -> list[str]:
        return self.__pc_source_lines

    @property
    def pc_source_path(self) -> str:
        return self.__pc_source_path

    @property
    def pc_source_dirname(self) -> str:
        return "/".join(self.__pc_source_path.split("/")[:-1])

    @property
    def pc_source_filename(self) -> str:
        return self.__pc_source_path.split("/")[-1]

    @property
    def external_locals(self) -> set[str] | None:
        return self._external_locals

    @external_locals.setter
    def external_locals(self, value: set[str]):
        self._external_locals = value

    @property
    def external_globals(self) -> set[str] | None:
        return self._external_globals

    @external_globals.setter
    def external_globals(self, value: set[str]):
        self._external_globals = value

    def __init__(self, pc_source: str, pc_source_path: str, *args, **kwargs):
        Pccdb.active_instance = self
        self.__pc_source_path = pc_source_path
        self.__pc_source_lines = pc_source.splitlines()
        # super().__init__(stdin=sys.stdin, stdout=sys.stdout, readrc=False)
        self.stdout = kwargs["stdout"]
        self.stdin = kwargs["stdin"]
        super().__init__(*args, **kwargs)

    def __del__(self):
        # self._pdb_out.close()
        if self is Pccdb.active_instance:
            Pccdb.active_instance = None

    def get_locals(self) -> Mapping[str, Any]:
        return self.curframe_locals

    def get_locals_sanitised(self) -> dict[str, any]:
        local_variables = self.curframe_locals
        if isinstance(local_variables, str):
            return {"Not": "Available"}
        return {k: v for k, v in local_variables.items() if k not in self._external_locals}

    def get_globals(self) -> dict[str, Any]:
        return self.curframe.f_globals

    def get_globals_sanitised(self) -> dict[str, Any]:
        global_vars = self.curframe.f_globals
        if isinstance(global_vars, str):
            return {"Not": "Available"}
        return {k: v for k, v in global_vars.items() if k not in self._external_globals}

    def _has_line_marker(self, line: str) -> bool:
        return len(re.findall(r"# l:\d+", line)) > 0

    def _is_internal_frame(self, frame) -> bool:
        # TODO: This will have to change in the future
        path: str = frame.f_code.co_filename
        return "output.py" in path

    def user_call(self, frame, argument_list):
        if not self._is_internal_frame(frame):
            # move the return point of the given frame
            self.set_return(frame)
            # execute final line of the current function on the next iteration of the cmdloop
            self.cmdqueue = ["next"] + self.cmdqueue
        super().user_call(frame, argument_list)

    def do_next(self, arg):
        self.set_next(self.curframe)
        return 1

    do_n = do_next

    def do_step(self, arg):
        self.set_step()
        return 1

    do_s = do_step

    do_z = do_step

    def postcmd(self, stop, line):
        print("POSTCMD", stop, line, type(line))
        source, _ = inspect.findsource(self.curframe)
        self.__current_py_lineno = self.curframe.f_lineno
        self.__current_py_line = source[self.__current_py_lineno - 1].strip()
        if self._has_line_marker(self.__current_py_line):
            self.__current_pc_lineno = int(self.__current_py_line.split("l:")[-1])
            self.__current_pc_line = self.__pc_source_lines[self.__current_pc_lineno - 1].strip()

            print(f"{Style.RED}{self.__current_py_lineno} @ {self.__current_py_line}{Style.RESET}")
            print(f"{Style.BLUE}{self.__current_pc_lineno} @ {self.__current_pc_line}{Style.RESET}")
        else:
            print(f"{Style.GREEN}Line {self.__current_py_lineno}:{self.current_py_line} has no line marker{Style.RESET}")
        return super().postcmd(stop, line)

    def do_break(self, arg: str, temporary: bool = False):
        print("DOING BRAKE", arg)
        args = arg.split(":")
        pc_lineno = int(arg.split(":")[-1])
        filename: str = ":".join(args[:-1])
        # on windows, WebPdb will provide absolute paths with a leading \
        # Pdb does not like this
        if filename[0] == "\\":
            filename = filename[1:]
        py_lines, _ = inspect.findsource(self.curframe)
        print("GOT PC LINE", pc_lineno)
        # find the Py line whose line marker is equal to pc_lineno
        py_lineno = None
        for idx, line in enumerate(py_lines):
            if self._has_line_marker(line):
                x = line.split("# l:")
                if len(x) > 1 and int(x[-1]) == pc_lineno:
                    py_lineno = idx + 1
                    break
        if py_lineno is None:
            return f"Cannot set breakpoint at line {pc_lineno} of {filename}"
        new_arg = f"{filename}:{py_lineno}"
        print("NUSTYLE ARG", new_arg)
        return super().do_break(new_arg, temporary)

    do_b = do_break

    def do_clear(self, args: list[str | int]):
        if len(args) == 0:
            # clear all breakpoints
            pass
        else:
            # clear only breakpoints listed in args
            pass

    do_cl = do_clear

    def get_breakpoint_pc_lines(self, filename: str) -> list[int]:
        py_lines: list[int] = self.get_file_breaks(filename)
        return list(map(self._get_pc_line_for, py_lines))

    def _get_pc_line_for(self, py_lineno: int) -> int | None:
        py_lines, _ = inspect.findsource(self.curframe)
        py_line: str = py_lines[py_lineno - 1]
        if self._has_line_marker(py_line):
            pc_line = py_line.split("# l:")
            if len(pc_line) > 1:
                return int(pc_line[-1])
        return None


    @property
    def current_py_line(self) -> str:
        return self.__current_py_line

    @property
    def current_pc_line(self) -> str:
        return self.__current_pc_line

    @property
    def current_py_lineno(self) -> int:
        return self.__current_py_lineno

    @property
    def current_pc_lineno(self) -> int:
        return self.__current_pc_lineno


def set_trace(pc_source_code: str, *, header=None):
    pdb = Pccdb(pc_source_code)
    if header is not None:
        pdb.message(header)
    prev_frame: FrameType = sys._getframe().f_back # pylint: disable=protected-access
    pdb.external_globals = set(copy(prev_frame.f_globals.keys()))
    pdb.external_locals = set(copy(prev_frame.f_locals.keys()))
    pdb.set_trace(prev_frame)
