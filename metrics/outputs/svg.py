# -*- coding: UTF-8 -*-

import os

from jinja2 import Template

from .abstract_output import AbstractOutput
from metrics.results import LINES_OF_CODE, COMMENT_RATE, TESTS_COVERAGE, REPORT_DATE, MAINTAINABILITY_INDEX

class SVG(AbstractOutput):
    """
    Output SVG tag icons.

    :ivar success_color: Hexadecimal color used in case of success.
    :ivar failure_color: Hexadecimal color used in case of failure.
    :ivar neutral_color: Neutral hexadecimal color .
    """

    def __init__(self, *args, success_color="#4BB543", failure_color="#e05d44", neutral_color="#007ec6", **kwargs):
        """

        :param args: AbstractOutput arguments.
        :param success_color: Hexadecimal color used in case of success.
        :param failure_color: Hexadecimal color used in case of failure.
        :param neutral_color: Neutral hexadecimal color .
        :param kwargs:  AbstractOutput arguments.
        """
        super().__init__(*args, **kwargs)

        self.success_color = success_color
        self.failure_color = failure_color
        self.neutral_color = neutral_color

    def output(self, results):
        # Prepare output folder
        os.makedirs(self.path, exist_ok=True)

        # Output date
        value = results[REPORT_DATE]
        self.icon("%s/metric_date.svg" % self.path, key="Date", value=value.strftime('%m/%d'),
                  color=self.neutral_color)

        # Output lines of code
        value = results[LINES_OF_CODE]
        self.icon("%s/metric_lines.svg" % self.path, key="Lines", value=value,
                  color=self.neutral_color if value > 0 else self.failure_color)

        # Output documentation rate
        value = results[COMMENT_RATE]
        self.icon('%s/metric_comments.svg' % self.path, key="/* */", value=self.prettify(value),
                  color=self.color_from_float(value, max_value=0.45))

        # Output test coverage
        value = results[TESTS_COVERAGE]
        self.icon('%s/metric_tests.svg' % self.path, key="Tests", value=self.prettify(value),
                  color=self.color_from_float(value, min_value=0.2))

        # Output maintainability index
        value = results[MAINTAINABILITY_INDEX]
        self.icon('%s/metric_maintainability_index.svg' % self.path, key="MI", value=self.prettify(value),
                  color=self.color_from_float(value, min_value=0.2, max_value=0.9))

    def color_from_float(self, value:float, min_value=0.0, max_value=1.0):
        """
        Convert a float into a color.

        :param value: Float.
        :param min_value: Minimum value considered as failing.
        :param max_value: Maximum value considered as success.
        :return: Hexadecimal color.
        """

        if value is None:
            return self.failure_color
        elif value <= min_value:
            return self.failure_color
        elif value >= max_value:
            return self.success_color
        else:
            r = value / (max_value - min_value) # Success rate in [0,1]

            def hex_to_rgb(hex):
                return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))

            min_color = hex_to_rgb(self.failure_color[1:])
            max_color = hex_to_rgb(self.success_color[1:])
            rgb_color = tuple(map(lambda x, y: round((1.0 - r) * x + r * y), min_color, max_color))
            return '#%02x%02x%02x' % rgb_color

    @staticmethod
    def icon(path:str, key:str="build", value:str="passing", color:str="#4c1",
             template_path="%s/svg_template.svg" % os.path.dirname(__file__)):
        """
        Create an SVG icon from a template by replacing:
            - {{ key }}
            - {{ value }}
            - {{ color }}

        :param path: Output path of the svg.
        :param key: Key string.
        :param value: Value string.
        :param color: Hexadecimal color.
        :param template_path: Path of the template SVG.
        """

        # Fetch template
        with open(template_path, 'r') as file:
            template = Template(file.read())

        # Create SVG content
        svg_content = template.render(key=key, value=value, color=color)

        # Write it
        with open(path, 'w') as file:
            file.write(svg_content)
