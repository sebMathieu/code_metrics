# -*- coding: UTF-8 -*-

import subprocess
import re
from io import StringIO

from radon.cli.harvest import RawHarvester
from radon.cli import Config

from .results import initialize_results, LINES_OF_CODE, DOCUMENTATION_RATE, TESTS_COVERAGE

def compute_metrics(code_path:str, tests_path:str="tests"):
    """
    Compute all available metrics.

    :param code_path: Path to the source code.
    :param tests_path: Path with the unit tests.
    :return Dictionary with the results.
    """

    results = initialize_results(code_path)
    raw_metrics(code_path, results)
    tests_coverage(code_path, results, tests_path=tests_path)

    return results

def raw_metrics(code_path, results):
    """
    Compute raw metrics such as number of lines of code or documentation rate.

    :param code_path: Path to the source code
    :param results: Dictionary to which the results are appended.
    """
    config = Config(exclude=None, ignore=None, summary=True)
    harvester = RawHarvester([code_path], config)
    metrics = harvester.results

    # Get the summary which is the last metric of the metrics generator
    summary = dict()
    for m in metrics:
        for k, v in m[1].items():
            try:
                summary[k] += v
            except KeyError:
                summary[k] = v

    # Export results
    results[LINES_OF_CODE] = summary.get('sloc', 0)
    results[DOCUMENTATION_RATE] = (float(summary.get('comments', 0)) + float(summary.get('multi', 0))) / (float(summary.get('loc', 1)))

def tests_coverage(code_path, results, tests_path='tests'):
    # Run the coverage
    cmd = ['coverage', 'run', '--source', code_path, '-m', tests_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print("Unit tests failed.")
        results[TESTS_COVERAGE] = None

    # Get the coverage report
    report_output = StringIO()
    cmd = ['coverage', 'report']
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    report_output.seek(0)
    report = result.stdout.decode()

    # Parse the output report
    total_regex = re.compile(r'TOTAL.+?([0-9\.]+)%$')
    match = total_regex.search(report)

    results[TESTS_COVERAGE] = float(match.group(1)) / 100.0
