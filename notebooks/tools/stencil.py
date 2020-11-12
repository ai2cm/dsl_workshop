def print_stencil_code(stencil):
    """Prints the file stencil._file_name to stdout."""
    with open(stencil._file_name, mode="r") as f:
        print(f.read())
