# -*- coding: UTF-8 -*-

import datetime

# Result key constants
CODE_PATH = 'Code path'
REPORT_DATE = 'Report date'
LINES_OF_CODE = 'Lines of code'
COMMENT_RATE = 'Documentation rate'
TESTS_COVERAGE = 'Tests coverage'
MAINTAINABILITY_INDEX = 'Maintainability index'
AVERAGE_CYCLOMATIC_COMPLEXITY = 'Cyclomatic complexity - average'
MAX_CYCLOMATIC_COMPLEXITY = 'Cyclomatic complexity - maximum'
MAX_CYCLOMATIC_COMPLEXITY_FUNCTION = 'Max cyclomatic complexity function'
CODE_STYLE = 'Code style'

def initialize_results(code_path=".", date=datetime.datetime.now()):
    """
    Initialize the results dictionary.

    :param code_path: Path of the code to measure.
    :param date: Current date time.
    :return: Dictionary.
    """

    return {CODE_PATH: code_path, REPORT_DATE:date}
