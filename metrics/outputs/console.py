# -*- coding: UTF-8 -*-

from .abstract_output import AbstractOutput
from metrics.report_keys import CODE_PATH, REPORT_DATE

class Console(AbstractOutput):
    """
    Output in the console.
    """

    def output(self, results):
        print('Report for the code in "%s" - %s' % (CODE_PATH, self.prettify(results[REPORT_DATE])))
        for k, v in results.items():
            # Skip some fields
            if k in [CODE_PATH, REPORT_DATE]:
                continue

            # Show
            print("\t%s: %s" % (k, self.prettify(v)))
