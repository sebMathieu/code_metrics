# -*- coding: UTF-8 -*-

import unittest
import os

from metrics.metrics import raw_metrics
from metrics.results import initialize_results, LINES_OF_CODE, COMMENT_RATE, REPORT_DATE, MAINTAINABILITY_INDEX

TEST_CODE_PATH = "metrics"

class TestMetrics(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Set the working directory to the root.

    def test_raw(self):
        results = initialize_results(TEST_CODE_PATH)
        raw_metrics(TEST_CODE_PATH, results)

        self.assertIn(LINES_OF_CODE, results)
        self.assertIn(COMMENT_RATE, results)
        self.assertIn(REPORT_DATE, results)

        self.assertGreater(results[MAINTAINABILITY_INDEX], 0.0)
        self.assertLessEqual(results[MAINTAINABILITY_INDEX], 1.0)  # Equal because, perfection is reachable, sometimes  ...
