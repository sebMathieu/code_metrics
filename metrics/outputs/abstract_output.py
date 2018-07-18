# -*- coding: UTF-8 -*-

import datetime
import os.path

from abc import ABC, abstractmethod

class AbstractOutput(ABC):
    """
    Abstract output.

    :ivar path: Output path.
    """

    def __init__(self, path=".", datetime_format="%Y-%m-%d %H:%M"):
        """
        Constructor.

        :param path: Output path.
        :param datetime_format: Datetime export format.
        """
        self.path = path
        self.datetime_format = datetime_format

    @abstractmethod
    def output(self, results):
        """
        Output the results.

        :param results: Results dictionary.
        """
        raise NotImplementedError

    def dump(self, value):
        """
        Format a value in a basic type (string, float, etc.)

        :param value: Value of any type.
        :return: Dumped value.
        """

        if isinstance(value, datetime.datetime):
            return value.strftime(self.datetime_format)
        return value

    def prettify(self, value):
        """
        Prettify a value to be displayed as a string.

        :param value: Value of any type.
        :return: String.
        """

        if isinstance(value, float) and 0.025 <= value <= 1.0:
            return "%.0f%%" % (value * 100.0)
        elif isinstance(value, datetime.datetime):
            return value.strftime(self.datetime_format)
        elif isinstance(value, str) and os.path.exists(value):
            return str(os.path.normpath(value))

        return str(value)
