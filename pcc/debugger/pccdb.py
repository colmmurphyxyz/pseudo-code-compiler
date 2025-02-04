import io

from ansi_color_codes import Style
from pdb import Pdb
import sys
from types import FrameType
import re

__all__ = ["Pccdb", "set_trace"]

from typing import TextIO, Any, Mapping


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
        return re.match(r"# l:\d+", line) is not None

    def _is_internal_frame(self, frame) -> bool:
        return frame.f_code.co_filename == "/home/colm/PycharmProjects/pcc_fixed/pcc/output.py"

    def user_call(self, frame, argument_list):
        if not self._is_internal_frame(frame):
            # move the return point of the given frame
            self.set_return(frame)
            # execute final line of the current function on the next iteration of the cmdloop
            self.cmdqueue = ["next"] + self.cmdqueue

    def user_line(self, frame):
        print(Style.GREEN)
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

    # def do_z(self, arg):
    #     """Custom step-into for current file, next for external files."""
    #     curframe = self.curframe
    #     filename = curframe.f_code.co_filename
    #
    #     if self._is_internal_frame(curframe):
    #         # Internal function: act like 'step'
    #         print("Stepping into an internal function.")
    #         self.set_step()
    #     else:
    #         # External function: act like 'next'
    #         print("Skipping external function call.")
    #         self.set_next(curframe)
    #     return 1

    do_z = do_step

    def precmd(self, line):
        print("PreCmd", self.curframe.f_lineno)
        return super().precmd(line)

    def postcmd(self, stop, line):
        print("Postcmd", self.curframe.f_lineno)
        return super().postcmd(stop, line)

    # def do_step(self, arg):
    #     print("stepping")
    #     frame = self.curframe
    #     current_file = frame.f_code.co_filename
    #     current_module = inspect.getmodule(frame)
    #     super().do_step(arg)
    #     new_frame = self.curframe
    #     if new_frame:
    #         new_file = new_frame.f_code.co_filename
    #         new_module = inspect.getmodule(new_frame)
    #         if new_file != current_file or new_module != current_module:
    #             self.do_until(None)

    # def do_next(self, arg):
    #     """Execute the next line, stepping over functions."""
    #     print("next")
    #     frame = self.curframe
    #     if frame:
    #         # Get the current line's file and module
    #         current_file = frame.f_code.co_filename
    #         current_module = inspect.getmodule(frame)
    #
    #         # Execute the next line
    #         super().do_next(arg)
    #
    #         # Check if the new frame is in the same file or module
    #         new_frame = self.curframe
    #         if new_frame:
    #             new_file = new_frame.f_code.co_filename
    #             new_module = inspect.getmodule(new_frame)
    #
    #             # If the new frame is in an external module, step out of it
    #             if new_file != current_file or new_module != current_module:
    #                 self.do_until(None)  # Step out of the external function
    #
    # def do_list(self, arg):
    #     print("FGHJK")
    #     self.message("Listing source code")
    #     print(type(arg), repr(arg))
    #     super().do_list(arg)
    #
    # def do_l(self, arg):
    #     print("take this L bozo")
    #
    # def do_longlist(self, arg):
    #     self.do_list(arg)



def set_trace(pc_source_code: str, *, header=None):
    pdb = Pccdb(pc_source_code)
    if header is not None:
        pdb.message(header)
    pdb.set_trace(sys._getframe().f_back)
