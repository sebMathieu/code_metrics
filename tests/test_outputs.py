# -*- coding: UTF-8 -*-

import unittest
import os
import shutil
import datetime
import sys
import io
from unittest.mock import patch, mock_open, MagicMock

from metrics.outputs import JSON, RST, Console, SVG

class TestOutputs(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Set the working directory to the root.

        # Data
        self.results = {
            "Code path": "metrics",
            "Report date": datetime.datetime(2018, 6, 24, 1, 2, 3),
            "Lines of code": 127,
            "Documentation rate": 0.32,
            "Tests coverage": 0.6
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
        handle.write.assert_any_call('"Tests coverage"')

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
        self.assertGreaterEqual(report.find("Documentation rate: 32%"), 0)

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
