# -*- coding: UTF-8 -*-

import json
import os

from .abstract_output import AbstractOutput

class JSON(AbstractOutput):
    """
    Output a RST report.
    """

    def output(self, results):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open('%s' % self.path, 'w') as file:
            json.dump({k: self.dump(v) for k, v in results.items()}, file, indent=4)
