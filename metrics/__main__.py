# -*- coding: UTF-8 -*-
"""Metrics.
Compute Python code metrics.

Usage:
    metrics [options]

Options:
    --console                   Console output.
    -h                          Display this help.
    --json PATH                 Output the report in a JSON file.
    -p PATH                     Path to the source code [Default: .]
    --png PATH                  Output PNG files in the given path
    --rst PATH                  Output the report in a RST file.
    --svg PATH                  Output SVG files in the given path.
    -t PATH                     Test folder path [Default: tests].
"""

import sys

from docopt import docopt

from .metrics import compute_metrics
from .outputs import Console, RST, JSON, SVG, PNG

if __name__ == "__main__":
    args = docopt(__doc__)

    # Compute metrics
    code_path = args['-p']
    results = compute_metrics(code_path, tests_path=args['-t'])

    # Select output format from arguments and output
    output_done = False
    for codec in [RST, JSON, SVG, Console, PNG]:
        arg_key = '--%s' % codec.__qualname__.lower()
        if args[arg_key] is not None and args[arg_key] != False:
            try:
                output_class = codec(path=args[arg_key])
                output_class.output(results)
                output_done = True
            except Exception as e:  # Ensure proper output for the user
                print('Unable to use the output "%s". Try using another output type.' %
                      output_class.__class__.__qualname__, file=sys.stderr)
                raise e

    # At least one output
    if not output_done:
        Console().output(results)
