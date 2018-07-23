# -*- coding: UTF-8 -*-

import os
import datetime

from jinja2 import Template

from .abstract_output import AbstractOutput
import metrics.report_keys as report_keys

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
        for key in report_keys.__dict__.values():
            # Only keep report keys that can be rendered
            if not isinstance(key, report_keys.ReportKeys) or key.python_type == str or key.abbreviation is None:
                continue

            # Prepare value
            value = results[key]
            if isinstance(value, datetime.datetime):
                value = value.strftime('%m/%d')

            # Obtain color
            if key.ub is None:
                color = self.neutral_color
            else:
                color = self.color_from_float(value, max_value=key.ub, min_value=key.lb, invert=not key.more_is_better)

            # Create icon
            self.icon("%s/metric_%s.svg" % (self.path, key.to_file_name()),
                      key=key.abbreviate(), value=self.prettify(value), color=color)

    def color_from_float(self, value:float, min_value=0.0, max_value=1.0, invert=False):
        """
        Convert a float into a color.

        :param value: Float.
        :param min_value: Minimum value considered as failing.
        :param max_value: Maximum value considered as success.
        :param invert: Set a success as a maximum value instead of the opposite.
        :return: Hexadecimal color.
        """
        if invert:
            max_color, min_color = self.failure_color, self.success_color
        else:
            max_color, min_color = self.success_color, self.failure_color

        if value is None:
            return min_color
        elif value <= min_value:
            return min_color
        elif value >= max_value:
            return max_color
        else:
            r = value / (max_value - min_value) # Success rate in [0,1]

            def hex_to_rgb(hex):
                return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))

            min_color_values = hex_to_rgb(min_color[1:])
            max_color_values = hex_to_rgb(max_color[1:])
            rgb_color = tuple(map(lambda x, y: round((1.0 - r) * x + r * y), min_color_values, max_color_values))
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
