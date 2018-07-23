# -*- coding: UTF-8 -*-

import datetime

class ReportKeys:
    """
    Key of the metrics report.

    :ivar name: Name of the key.
    :ivar python_type: Python type of the key.
    :ivar abbreviation: Shorter name for the key.
    :ivar lb: Lower bound on the key value to be acceptable.
    :ivar ub: Upper bound on the key value to be acceptable.
    :ivar more_is_better: Boolean true if more is better.
    """

    def __init__(self, name: str, python_type: type = str, abbreviation: str = None, lb = None, ub = None,
                 more_is_better: bool = True):
        """

        :param name: Name of the key.
        :param python_type: Python type of the key.
        :param abbreviation: Shorter name for the key.
        :param lb: Lower bound on the key value to be acceptable.
        :param ub: Upper bound on the key value to be acceptable.
        :param more_is_better: Boolean true if more is better.
        """
        self.name = name
        self.python_type = python_type
        self.abbreviation = abbreviation
        self.lb = lb
        self.ub = ub
        self.more_is_better = more_is_better

    def abbreviate(self):
        """
        Get the abbreviation of this key.

        :return: String.
        :rtype: str
        """
        return self.abbreviation if self.abbreviation is not None else self.name

    def to_file_name(self, new_spaces="_"):
        """
        Get a file name from the key, lower case with underscores.

        :param new_spaces: Replacement for spaces.
        :return: String.
        """
        base_name  = "".join([c for c in self.name.lower() if c.isalpha() or c.isdigit() or c == " "])
        base_name = base_name.replace("  ", " ") # Replace double spaces
        base_name = base_name.replace(" ", new_spaces)
        return base_name

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return str(self) < str(other)

    def __hash__(self):
        return id(self)

# Result key constants
CODE_PATH = ReportKeys('Code path', str)
REPORT_DATE = ReportKeys('Report date', datetime.datetime, abbreviation="Date")
LINES_OF_CODE = ReportKeys('Lines of code', int, abbreviation="Lines", lb=1)
COMMENT_RATE = ReportKeys('Documentation rate', float, abbreviation="/* */", lb=0.0, ub=0.45)
TESTS_COVERAGE = ReportKeys('Tests coverage', float, abbreviation="Tests", lb=0.2, ub=1.0)
MAINTAINABILITY_INDEX = ReportKeys('Maintainability index', float, abbreviation="MI", lb=0.1 ,ub=0.5)
AVERAGE_CYCLOMATIC_COMPLEXITY = ReportKeys('Cyclomatic complexity - average', float, abbreviation="CC~",
                                           more_is_better=False, lb=10, ub=35)
MAX_CYCLOMATIC_COMPLEXITY = ReportKeys('Cyclomatic complexity - maximum', int, abbreviation='CC^',
                                       more_is_better=False, lb=10, ub=35)
MAX_CYCLOMATIC_COMPLEXITY_FUNCTION = ReportKeys('Max cyclomatic complexity function', str)
CODE_STYLE = ReportKeys('Code style', float, abbreviation="Style", lb=0.1, ub=0.95)
