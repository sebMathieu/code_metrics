# -*- coding: UTF-8 -*-

import unittest
import os
import datetime
import sys
import io
from unittest.mock import patch, mock_open, MagicMock

from metrics.outputs import JSON, RST, Console, SVG, PNG
import metrics.results as metrics_results

class TestOutputs(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Set the working directory to the root.

        # Data
        self.results = {
            metrics_results.CODE_PATH: "metrics",
            metrics_results.REPORT_DATE: datetime.datetime(2018, 6, 24, 1, 2, 3),
            metrics_results.LINES_OF_CODE: 127,
            metrics_results.COMMENT_RATE: 0.32,
            metrics_results.TESTS_COVERAGE: None,
            metrics_results.MAINTAINABILITY_INDEX: 0.82,
            metrics_results.AVERAGE_CYCLOMATIC_COMPLEXITY: 3.5,
            metrics_results.MAX_CYCLOMATIC_COMPLEXITY: 9,
            metrics_results.MAX_CYCLOMATIC_COMPLEXITY_FUNCTION: "...",
            metrics_results.CODE_STYLE: 0.8
        }

        # Mock
        self._orig_mkdir = os.mkdir
        os.mkdir = MagicMock()

        self._orig_stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        os.mkdir = self._orig_mkdir
        sys.stdout = self._orig_stdout

    def test_json(self):
        out = JSON("test.json")
        m = mock_open()
        with patch('metrics.outputs.json.open', m):
            out.output(self.results)
        m.assert_called_once_with('test.json', 'w')
        handle = m()
        handle.write.assert_any_call('"%s"' % metrics_results.TESTS_COVERAGE)

    def test_rst(self):
        out = RST("test.rst")
        m = mock_open()
        with patch('metrics.outputs.rst.open', m):
            out.output(self.results)
        m.assert_called_once_with('test.rst', 'w')

    def test_console(self):
        out = Console()
        out.output(self.results)

        # Fetch output
        sys.stdout.seek(0)
        report = sys.stdout.read()
        self.assertGreaterEqual(report.find("%s: 32%%" % metrics_results.COMMENT_RATE), 0)
        self.assertGreaterEqual(report.find("%s: Failed" % metrics_results.TESTS_COVERAGE), 0)

    def test_svg(self):
        output_path = os.path.dirname(__file__)
        out = SVG(path=output_path)
        out.output(self.results)

        # Check
        svg_names = [f for f  in os.listdir(output_path) if f.endswith(".svg")]
        self.assertGreaterEqual(len(svg_names), 3)

        # Clean
        for f in svg_names:
            os.remove('%s/%s' % (output_path, f))

    def test_png(self):
        output_path = os.path.dirname(__file__)
        out = PNG(path=output_path)
        out.output(self.results)

        # Check
        png_names = [f for f  in os.listdir(output_path) if f.endswith(".png")]
        self.assertGreaterEqual(len(png_names), 3)

        # Clean
        for f in png_names:
            os.remove('%s/%s' % (output_path, f))
