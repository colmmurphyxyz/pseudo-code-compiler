# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com
#
# Copyright (c) 2016 Roman Miroshnychenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import random
import inspect
import os
import sys
import traceback

from contextlib import contextmanager
from copy import copy
from pprint import pformat
from types import FrameType

from .web_console import WebConsole
from .pccdb import Pccdb

__all__ = ["WebDb", "set_trace", "post_mortem", "catch_post_mortem"]

class WebDb(Pccdb):
    """
    The main debugger class

    It provides a web-interface for Python's built-in PDB debugger
    with extra convenience features.
    """
    active_instance = None
    null = object()

    def __init__(self, pc_source_code: str, pc_source_path: str, host='', port=5555, patch_stdstreams=False):
        """
        Initialize the debugger
        :param pc_source_code: Pseudo-Code source of the file being debugged
        :type pc_source_code: str
        :param pc_source_path: Absolute or relative path to the file being debugged
        :type pc_source_path: str
        :param host: web-UI hostname or IP-address
        :type host: str
        :param port: web-UI port. If ``port=-1``, choose a random port value
            between 32768 and 65536.
        :type port: int
        :param patch_stdstreams: redirect all standard input and output
            streams to the web-UI.
        :type patch_stdstreams: bool
        """
        if port == -1:
            random.seed()
            port = random.randint(32768, 65536)
        self.console = WebConsole(host, port, self)
        super().__init__(pc_source_code, pc_source_path, stdin=self.console, stdout=self.console)
        # Borrowed from here: https://github.com/ionelmc/python-remote-pdb
        self._backup = []
        if patch_stdstreams:
            for name in (
                    'stderr',
                    'stdout',
                    '__stderr__',
                    '__stdout__',
                    'stdin',
                    '__stdin__',
            ):
                self._backup.append((name, getattr(sys, name)))
                setattr(sys, name, self.console)
        WebDb.active_instance = self

    def do_quit(self, arg):
        """
        quit || exit || q
        Stop and quit the current debugging session
        """
        for name, fh in self._backup:
            setattr(sys, name, fh)
        self.console.writeline('*** Aborting program ***\n')
        self.console.flush()
        self.console.close()
        WebDb.active_instance = None
        return super().do_quit(arg)

    do_q = do_exit = do_quit

    def do_inspect(self, arg):
        """
        i(nspect) object
        Inspect an object
        """
        if arg in self.curframe_locals:
            obj = self.curframe_locals[arg]
        elif arg in self.curframe.f_globals:
            obj = self.curframe.f_globals[arg]
        else:
            obj = WebDb.null
        if obj is not WebDb.null:
            self.console.writeline(f'{arg} = {type(obj)}:\n')
            for name, value in inspect.getmembers(obj):
                if not (name.startswith('__') and (name.endswith('__'))):
                    repr_value = self._get_repr(value, pretty=True, indent=8)
                    self.console.writeline(f'    {name}: {repr_value}\n')
        else:
            self.console.writeline(f'NameError: name "{arg}" is not defined\n')
        self.console.flush()

    do_i = do_inspect

    @staticmethod
    def _get_repr(obj, pretty=False, indent=1):
        """
        Get string representation of an object

        :param obj: object
        :type obj: object
        :param pretty: use pretty formatting
        :type pretty: bool
        :param indent: indentation for pretty formatting
        :type indent: int
        :return: string representation
        :rtype: str
        """
        if pretty:
            repr_value = pformat(obj, indent)
        else:
            repr_value = repr(obj)
        return repr_value

    def set_continue(self):
        # We do not detach the debugger
        # for correct multiple set_trace() and post_mortem() calls.
        self._set_stopinfo(self.botframe, None, -1)

    def dispatch_return(self, frame, arg):
        # The parent's method needs to be called first.
        ret = super().dispatch_return(frame, arg)
        if frame.f_back is None:
            self.console.writeline('*** Thread finished ***\n')
            if not self.console.closed:
                self.console.flush()
                self.console.close()
                WebDb.active_instance = None
        return ret

    def get_current_frame_data(self):
        """
        Get all date about the current execution frame

        :return: current frame data
        :rtype: dict
        :raises AttributeError: if the debugger does hold any execution frame.
        :raises IOError: if source code for the current execution frame is not accessible.
        """
        lines = self.pc_source_lines
        lineno: int = self.current_pc_lineno
        py_filename = self.curframe.f_code.co_filename
        return {
            # 'dirname': os.path.dirname(os.path.abspath(filename)) + os.path.sep,
            # 'filename': os.path.basename(filename),
            "dirname": self.pc_source_dirname + os.path.sep,
            "filename": self.pc_source_filename,
            'file_listing': "\n".join(lines),
            'current_line': lineno,
            'breakpoints': self.get_breakpoint_pc_lines(py_filename),
            'globals': self.get_globals(),
            'locals': self.get_locals()
        }

    def _format_variables(self, raw_vars):
        """
        :param raw_vars: a `dict` of `var_name: var_object` pairs
        :type raw_vars: dict
        :return: sorted list of variables as a Unicode string
        :rtype: Unicode
        """
        f_vars = []
        for var, value in raw_vars.items():
            if not (var.startswith('__') and var.endswith('__')):
                repr_value = self._get_repr(value)
                f_vars.append(f'{var} = {repr_value}')
        return '\n'.join(sorted(f_vars))

    def get_globals(self):
        """
        Get the listing of global variables in the current scope

        . note:: special variables that start and end with
            double underscores ``__`` are not included.

        :return: a listing of ``var = value`` pairs sorted alphabetically
        :rtype: Unicode
        """
        return self._format_variables(super().get_globals_sanitised())

    def get_locals(self):
        """
        Get the listing of local variables in the current scope

        . note:: special variables that start and end with
            double underscores ``__`` are not included.
            For module scope globals and locals listings are the same.

        :return: a listing of ``var = value`` pairs sorted alphabetically
        :rtype: Unicode
        """
        return self._format_variables(super().get_locals_sanitised())

    def remove_trace(self, frame=None):
        """
        Detach the debugger from the execution stack

        :param frame: the lowest frame to detach the debugger from.
        :type frame: types.FrameType
        """
        sys.settrace(None)
        if frame is None:
            frame = self.curframe
        while frame and frame is not self.botframe:
            del frame.f_trace
            frame = frame.f_back

def set_trace(path: str, pc_source_code: str, host='', port=5555, patch_stdstreams=False):
    """
    Start the debugger

    This method suspends execution of the current script
    and starts a PDB debugging session. The web-interface is opened
    on the specified port (default: ``5555``).

    Example::

        import debugger;debugger.set_trace()

    Subsequent :func:`set_trace` calls can be used as hardcoded breakpoints.

    :param path: Absolute or relative path to the file being debugged
    :type path: str
    :param pc_source_code: Pseudo-Code source of the file being debugged
    :type pc_source_code: str
    :param host: web-UI hostname or IP-address
    :type host: str
    :param port: web-UI port. If ``port=-1``, choose a random port value
     between 32768 and 65536.
    :type port: int
    :param patch_stdstreams: redirect all standard input and output
        streams to the web-UI.
    :type patch_stdstreams: bool
    """
    pdb = WebDb.active_instance
    if pdb is None:
        # print("SRC", pc_source_lines[0])
        pdb = WebDb(pc_source_code, path, host, port, patch_stdstreams)
    else:
        # If the debugger is still attached reset trace to a new location
        pdb.remove_trace()
    prev_frame: FrameType = sys._getframe().f_back  # pylint: disable=protected-access
    pdb.external_globals = set(copy(prev_frame.f_globals).keys()).union({"__pdb_convenience_variables"})
    pdb.external_locals = set(copy(prev_frame.f_locals).keys()).union({"__pdb_convenience_variables"})
    pdb.set_trace(prev_frame)

def post_mortem(tb=None, host='', port=5555, patch_stdstreams=False):
    """
    Start post-mortem debugging for the provided traceback object

    If no traceback is provided the debugger tries to obtain a traceback
    for the last unhandled exception.

    Example::

        try:
            # Some error-prone code
            assert ham == spam
        except:
            debugger.post_mortem()

    :param tb: traceback for post-mortem debugging
    :type tb: types.TracebackType
    :param host: web-UI hostname or IP-address
    :type host: str
    :param port: web-UI port. If ``port=-1``, choose a random port value
        between 32768 and 65536.
    :type port: int
    :param patch_stdstreams: redirect all standard input and output
        streams to the web-UI.
    :type patch_stdstreams: bool
    :raises ValueError: if no valid traceback is provided and the Python
        interpreter is not handling any exception
    """
    # handling the default
    if tb is None:
        # sys.exc_info() returns (type, value, traceback) if an exception is
        # being handled, otherwise it returns (None, None, None)
        t, v, tb = sys.exc_info()
        exc_data = traceback.format_exception(t, v, tb)
    else:
        exc_data = traceback.format_tb(tb)
    if tb is None:
        raise ValueError('A valid traceback must be passed if no '
                         'exception is being handled')
    pdb = WebDb.active_instance
    if pdb is None:
        pdb = WebDb(host, port, patch_stdstreams)
    else:
        pdb.remove_trace()
    pdb.console.writeline('*** Web-PDB post-mortem ***\n')
    pdb.console.writeline(''.join(exc_data))
    pdb.reset()
    pdb.interaction(None, tb)


@contextmanager
def catch_post_mortem(host='', port=5555, patch_stdstreams=False):
    """
    A context manager for tracking potentially error-prone code

    If an unhandled exception is raised inside context manager's code block,
    the post-mortem debugger is started automatically.

    Example::

        with debugger.catch_post_mortem()
            # Some error-prone code
            assert ham == spam

    :param host: web-UI hostname or IP-address
    :type host: str
    :param port: web-UI port. If ``port=-1``, choose a random port value
        between 32768 and 65536.
    :type port: int
    :param patch_stdstreams: redirect all standard input and output
        streams to the web-UI.
    :type patch_stdstreams: bool
    """
    try:
        yield
    except Exception:  # pylint: disable=broad-except
        post_mortem(None, host, port, patch_stdstreams)
