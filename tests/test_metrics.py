# -*- coding: UTF-8 -*-

import unittest
import os

from metrics.metrics import raw_metrics, cyclomatic_complexity, code_style
import metrics.results as metric_results

TEST_CODE_PATH = "metrics"

class TestMetrics(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Set the working directory to the root.

    def test_raw(self):
        r = metric_results.initialize_results(TEST_CODE_PATH) # Results dictionary
        raw_metrics(TEST_CODE_PATH, r)

        self.assertIn(metric_results.LINES_OF_CODE, r)
        self.assertIn(metric_results.COMMENT_RATE, r)
        self.assertIn(metric_results.REPORT_DATE, r)

        self.assertGreater(r[metric_results.MAINTAINABILITY_INDEX], 0.0)
        self.assertLessEqual(r[metric_results.MAINTAINABILITY_INDEX], 1.0)  # Equal because, perfection is reachable, sometimes  ...

    def test_cyclomatic_complexity(self):
        r = {}
        cyclomatic_complexity(TEST_CODE_PATH, r)

        self.assertLess(r[metric_results.MAX_CYCLOMATIC_COMPLEXITY], 30)
        self.assertLess(r[metric_results.AVERAGE_CYCLOMATIC_COMPLEXITY], 20)
        self.assertIsNotNone(r[metric_results.MAX_CYCLOMATIC_COMPLEXITY_FUNCTION])

    def test_code_style(self):
        r = {}
        code_style(TEST_CODE_PATH, r)
