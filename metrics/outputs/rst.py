# -*- coding: UTF-8 -*-

import rst
import os

from .abstract_output import AbstractOutput
from metrics.results import CODE_PATH, REPORT_DATE

class RST(AbstractOutput):
    """
    Output a RST report.
    """

    def output(self, results):
        # Prepare the rst
        doc = rst.Document('Metrics for the code "%s"' % self.prettify(results[CODE_PATH]))
        doc.add_child(rst.Paragraph('*Date of the report:* %s\n\n' % self.prettify(results[REPORT_DATE])))

        table = rst.Table('Metrics', ['Name', 'Value'])
        for k, v in results.items():
            if k in [CODE_PATH, REPORT_DATE]:
                continue # Skip some fields
            table.add_item((k, self.prettify(v)))
        doc.add_child(table)

        # Write it
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open('%s' % self.path, 'w') as file:
            file.write(doc.get_rst())
