# -*- coding: UTF-8 -*-

import subprocess
import re
import os
import sys
from io import StringIO

from ..results import TESTS_COVERAGE

COVERAGE_FILE = '.coverage'  # Path to the coverage file

def tests_coverage(code_path, results, tests_path='tests'):
    """
    Get the test coverage rate from unit tests.

    :param code_path: Path to the source code.
    :param results: Dictionary with the results.
    :param tests_path: Path with the unit tests.
    """

    # Run the coverage

    if os.path.exists(COVERAGE_FILE):
        os.remove(COVERAGE_FILE)
    cmd = ['coverage', 'run', '--source', code_path, '-m', tests_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    failed = result.stderr.decode().find('FAILED') >= 0
    if failed:
        print("Unit tests failed.", file=sys.stderr)
        results[TESTS_COVERAGE] = None
        return

    # Get the coverage report
    report_output = StringIO()
    cmd = ['coverage', 'report']
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    report_output.seek(0)
    report = result.stdout.decode()

    # Parse the output report
    total_regex = re.compile(r'TOTAL.+?([0-9\.]+)%$')
    match = total_regex.search(report)
    if match is None:
        results[TESTS_COVERAGE] = 0.0
    else:
        results[TESTS_COVERAGE] = float(match.group(1)) / 100.0
