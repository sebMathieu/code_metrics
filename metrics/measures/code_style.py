# -*- coding: UTF-8 -*-

import pycodestyle

from metrics.report_keys import CODE_STYLE

def code_style(code_path, results, ignore_codes=None):
    """
    Check code style.

    :param code_path: Path to the source code.
    :param results: Dictionary with the results.
    :param ignore_codes: List of PEP8 code to ignore.
    """

    # Run style guide checker
    if ignore_codes is None:
        ignore_codes = ['E121', 'E123', 'E126', 'E133', 'E226', 'E241', 'E242', 'E704', 'E501', 'W']
    style_guide = pycodestyle.StyleGuide(quiet=True, ignore=ignore_codes)
    report = style_guide.check_files([code_path])

    # Summarize metrics
    results[CODE_STYLE] = 1.0 - max(min(report.total_errors / report.counters['physical lines'], 1.0), 0.0)
