import os

def print_stencil_code(stencil, show_cpp=True):
    """Prints the file stencil._file_name to stdout."""
    backend = stencil._gt_backend_
    if backend.startswith("gt") and show_cpp:
        build_dir = os.path.splitext(lap_tmp._file_name)[0] + "_pyext_BUILD"
        source_file = os.path.join(build_dir, "computation.cpp")
        with open(source_file, mode="r") as f:
            print(f.read())
    with open(stencil._file_name, mode="r") as f:
        print(f.read())
