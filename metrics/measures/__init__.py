# -*- coding: UTF-8 -*-

import datetime

from metrics.report_keys import CODE_PATH, REPORT_DATE
from .raw import raw
from .cyclomatic_complexity import cyclomatic_complexity
from .tests_coverage import tests_coverage
from .code_style import code_style

def compute_metrics(code_path:str, tests_path:str="tests", date=datetime.datetime.now()):
    """
    Compute all available metrics.

    :param code_path: Path to the source code.
    :param tests_path: Path with the unit tests.
    :param date: Current date time.
    :return Dictionary with the results.
    """

    results = {CODE_PATH: code_path, REPORT_DATE:date}
    raw(code_path, results)
    cyclomatic_complexity(code_path, results)
    tests_coverage(code_path, results, tests_path=tests_path)
    code_style(code_path, results)

    return {k: results[k] for k in sorted(results.keys())}