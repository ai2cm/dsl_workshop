import os

from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import TerminalFormatter

def print_generated_code(stencil, show_cpp=True):
    """Prints the generated code that executes when a stencil is called.

    If the stencil is generated from C++, show_cpp=True will show the C++ code
    instead of the Python wrapper.
    """
    backend = stencil._gt_backend_
    if backend.startswith("gt") and show_cpp:
        build_dir = os.path.splitext(stencil._file_name)[0] + "_pyext_BUILD"
        source_file = os.path.join(build_dir, "computation.cpp")
        with open(source_file, mode="r") as f:
            code = f.read()
            lexer = guess_lexer(code)
            print(highlight(code, lexer, TerminalFormatter()))
    else:
        with open(stencil._file_name, mode="r") as f:
            code = f.read()
            lexer = guess_lexer(code)
            print(highlight(code, lexer, TerminalFormatter()))
