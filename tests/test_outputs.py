# -*- coding: UTF-8 -*-

import unittest
import os
import datetime
from unittest.mock import patch, mock_open

from metrics.outputs import JSON, RST, Console

class MockMkdir(object):
    def __init__(self):
        self.received_args = None

    def __call__(self, *args):
        self.received_args = args

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
        os.mkdir = MockMkdir()

    def tearDown(self):
        os.mkdir = self._orig_mkdir

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
        # TODO mock print
