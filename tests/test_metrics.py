# -*- coding: UTF-8 -*-

import unittest
import os

from metrics.measures import raw, cyclomatic_complexity, code_style
import metrics.report_keys as report_keys

TEST_CODE_PATH = "metrics"

class TestMetrics(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Set the working directory to the root.

    def test_raw(self):
        r = {}
        raw(TEST_CODE_PATH, r)

        self.assertIn(report_keys.LINES_OF_CODE, r)
        self.assertIn(report_keys.COMMENT_RATE, r)

        self.assertGreater(r[report_keys.MAINTAINABILITY_INDEX], 0.0)
        self.assertLessEqual(r[report_keys.MAINTAINABILITY_INDEX], 1.0)  # Equal because, perfection is reachable, sometimes  ...

    def test_cyclomatic_complexity(self):
        r = {}
        cyclomatic_complexity(TEST_CODE_PATH, r)

        self.assertLess(r[report_keys.MAX_CYCLOMATIC_COMPLEXITY], 30)
        self.assertLess(r[report_keys.AVERAGE_CYCLOMATIC_COMPLEXITY], 20)
        self.assertIsNotNone(r[report_keys.MAX_CYCLOMATIC_COMPLEXITY_FUNCTION])

    def test_code_style(self):
        r = {}
        code_style(TEST_CODE_PATH, r)
