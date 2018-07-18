# -*- coding: UTF-8 -*-

import datetime


CODE_PATH = 'Code path'
REPORT_DATE = 'Report date'
LINES_OF_CODE = 'Lines of code'
DOCUMENTATION_RATE = 'Documentation rate'
TESTS_COVERAGE = 'Tests coverage'


def initialize_results(code_path=".", date=datetime.datetime.now()):
    """
    Initialize the results dictionary.

    :param code_path: Path of the code to measure.
    :param date: Current date time.
    :return: Dictionary.
    """

    return {CODE_PATH: code_path, REPORT_DATE:date}
