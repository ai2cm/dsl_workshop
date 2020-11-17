import os

import numpy as np

import gt4py
from gt4py import gtscript

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


def run_stencil_scaling(stencil_def, backends, domain, origin, nruns = 5, factor = 2, dtype=np.float64):
    ni, nj, nk = domain
    nhalo = origin[0]
    init_ni = ni
    init_nj = nj

    timings = dict()
    sizes = dict()

    for backend in backends:
        ni = init_ni
        nj = init_nj

        sizes[backend] = []
        timings[backend] = []

        for n in range(0, nruns):
            print(f"Running with {backend} backend ({n})...")

            domain = (ni, nj, nk)
            shape = (ni + 2 * nhalo, nj + 2 * nhalo, nk)

            rand_data = np.random.randn(*shape)
            in_field = gt4py.storage.from_array(rand_data, backend, origin, shape, dtype=dtype)
            out_field = gt4py.storage.zeros(backend, origin, shape, dtype)
            exec_info = {}

            stencil = gtscript.stencil(backend, stencil_def)
            stencil(in_field, out_field, origin=origin, domain=domain, exec_info=exec_info)

            call_time = (exec_info['call_end_time'] - exec_info['call_start_time']) * 1000.
            run_time = (exec_info['run_end_time'] - exec_info['run_start_time']) * 1000.

            timings[backend].append(run_time)
            sizes[backend].append(ni)

            ni *= factor
            nj *= factor

    return timings, sizes
