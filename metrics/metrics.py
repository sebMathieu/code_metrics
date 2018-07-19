# -*- coding: UTF-8 -*-

import subprocess
import re
from io import StringIO

from deepmerge import always_merger
from radon.cli.harvest import RawHarvester, MIHarvester, CCHarvester
from radon.complexity import LINES
from radon.cli import Config

from .results import initialize_results, LINES_OF_CODE, COMMENT_RATE, TESTS_COVERAGE, MAINTAINABILITY_INDEX

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

    return {k: results[k] for k in sorted(results.keys())}

def raw_metrics(code_path, results):
    """
    Compute raw metrics such as number of lines of code, documentation rate or complexity metrics

    :param code_path: Path to the source code
    :param results: Dictionary to which the results are appended.
    """

    # Lines
    h = RawHarvester([code_path], Config(exclude=None, ignore=None, summary=True))
    file_metrics = dict(h.results)

    # Maintainability
    h = MIHarvester([code_path],
                Config(min='A', max='C', multi=True, exclude=None, ignore=None, show=False, json=False,
                       sort=False))
    mi_metrics = dict(h.results)
    always_merger.merge(file_metrics, mi_metrics)

    # Create a summary for the total of the code
    summary = dict()
    summation_keys = ['loc', 'lloc', 'sloc', 'comments', 'multi', 'blank', 'single_comments']
    for k in summation_keys:
        summary[k] = sum([metrics[k] for metrics in file_metrics.values()])

    # Weighted average summaries
    averaging_keys = {'mi': 'sloc'}
    for key_index, weight_index in averaging_keys.items():
        if summary[weight_index] == 0.0:
            summary[weight_index] = 0.0
        else:
            summary[key_index] = sum([metrics[key_index] * metrics[weight_index] for metrics in file_metrics.values()]) / summary[weight_index]

    # Export results
    results[LINES_OF_CODE] = summary.get('lloc', 0)
    results[COMMENT_RATE] = (float(summary.get('comments', 0)) + float(summary.get('multi', 0))) / (float(summary.get('loc', 1)))
    results[MAINTAINABILITY_INDEX] = summary.get('mi', 0.0) / 100.0

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
    if match is None:
        results[TESTS_COVERAGE] = 0.0
    else:
        results[TESTS_COVERAGE] = float(match.group(1)) / 100.0
