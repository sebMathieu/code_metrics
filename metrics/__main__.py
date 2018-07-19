# -*- coding: UTF-8 -*-
"""Metrics.
Compute Python code metrics.

Usage:
    metrics [options] <code_path>

where
    <path> is the path to the Python code.

Options:
    --console                   Console output.
    -h                          Display this help.
    --json PATH                 Output the report in a JSON file.
    --rst PATH                  Output the report in a RST file.
    --svg PATH                  Output SVG files in the given path.
    -t PATH                     Test folder path [Default: tests].
"""

import sys

from docopt import docopt

from .metrics import compute_metrics
from .outputs import Console, RST, JSON, SVG

if __name__ == "__main__":
    args = docopt(__doc__)

    # Compute metrics
    code_path = args['<code_path>']
    results = compute_metrics(code_path, tests_path=args['-t'])

    # Select output format
    output_done = False
    for codec in [RST, JSON, SVG, Console]:
        arg_key = '--%s' % codec.__qualname__.lower()
        if args[arg_key] is not None and args[arg_key] != False:
            # Output
            try:
                output_class = codec(path=args[arg_key])
                output_class.output(results)
                output_done = True
            except Exception as e:
                print("Unable to use the output %s. Try using another output type." % output_class.__class__.__qualname__, file=sys.stderr)

    # At least one output
    if not output_done:
        Console().output(results)