# -*- coding: UTF-8 -*-
"""Metrics.
Compute Python code metrics.

Usage:
    metrics [options] <code_path>

where
    <path> is the path to the Python code.

Options:
    -h                          Display this help.
    --rst PATH                  Output the report in a RST file.
    --json PATH                  Output the report in a JSON file.
"""

import sys

from docopt import docopt

from .metrics import compute_metrics
from .outputs import Console, RST, JSON

if __name__ == "__main__":
    args = docopt(__doc__)

    # Compute metrics
    code_path = args['<code_path>']
    results = compute_metrics(code_path)

    # Select output format
    out = Console()
    for codec in [RST, JSON]:
        arg_key = '--%s' % codec.__qualname__.lower()
        if args[arg_key] is not None:
            out = codec(path=args[arg_key])

    # Output
    try:
        out.output(results)
    except Exception as e:
        print("Unable to use the output %s. Try using another output type." % out.__class__.__qualname__, file=sys.stderr)
        raise e