from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import TerminalFormatter

def print_generated_code(stencil):
    """Prints the file stencil._file_name to stdout."""
    with open(stencil._file_name, mode="r") as f:
        code = f.read()
        lexer = guess_lexer(code)
        print(highlight(code, lexer, TerminalFormatter()))

