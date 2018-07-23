# -*- coding: UTF-8 -*-

import os

import cairosvg

from .svg import SVG

class PNG(SVG):
    """
    Create PNG images from SVG icon output.

    :ivar keep_svg: Boolean, true to keep intermediate SVG files.
    :ivar scale: Image scale factor.
    """

    def __init__(self, *args, keep_svg=False, scale=4, **kwargs):
        """

        :param args: SVG arguments.
        :param keep_svg: Boolean, true to keep intermediate SVG files.
        :param scale: Image scale factor.
        :param kwargs: SVG arguments.
        """
        super().__init__(*args, **kwargs)

        self.keep_svg = keep_svg
        self.scale = scale

    def list_svg(self, file_suffix=".svg"):
        """
        Get all the files with a given suffix.

        :param file_suffix: Suffix of the files.
        :return: Set of file names in path
        """
        try:
            return  {f for f in os.listdir(self.path) if f.endswith(file_suffix)}
        except FileNotFoundError:
            return {}

    def output(self, results):
        initial_svgs = self.list_svg()

        # Create SVGs
        super().output(results)

        # Convert new svgs into png
        all_svgs = self.list_svg()
        for name in all_svgs:
            new_name = name[:-3] + "png"
            cairosvg.svg2png(url="%s/%s" % (self.path, name), write_to="%s/%s" % (self.path, new_name),
                             scale=self.scale)

        # Remove svgs
        new_svgs = all_svgs.difference(initial_svgs)
        if not self.keep_svg:
            for name in new_svgs:
                os.remove(os.path.join(self.path, name))
