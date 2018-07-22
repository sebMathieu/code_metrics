# -*- coding: UTF-8 -*-

from deepmerge import always_merger
from radon.cli.harvest import RawHarvester, MIHarvester
from radon.cli import Config

from ..results import LINES_OF_CODE, COMMENT_RATE, MAINTAINABILITY_INDEX

def raw(code_path, results):
    """
    Compute raw metrics such as number of lines of code, documentation rate or complexity metrics

    :param code_path: Path to the source code
    :param results: Dictionary to which the results are appended.
    """

    # Lines
    h = RawHarvester([code_path], Config(exclude=None, ignore=None, summary=True))
    file_metrics = dict(h.results)

    # Maintainability
    h = MIHarvester([code_path],
                Config(min='A', max='C', multi=True, exclude=None, ignore=None, show=False, json=False,
                       sort=False))
    mi_metrics = dict(h.results)
    always_merger.merge(file_metrics, mi_metrics)

    # Create a summary for the total of the code
    summary = dict()
    summation_keys = ['loc', 'lloc', 'sloc', 'comments', 'multi', 'blank', 'single_comments']
    for k in summation_keys:
        summary[k] = sum([metrics[k] for metrics in file_metrics.values()])

    # Weighted average summaries
    averaging_keys = {'mi': 'sloc'}
    for key_index, weight_index in averaging_keys.items():
        if summary[weight_index] == 0.0:
            summary[weight_index] = 0.0
        else:
            summary[key_index] = sum([metrics[key_index] * metrics[weight_index] for metrics in file_metrics.values()]) / summary[weight_index]

    # Export results
    results[LINES_OF_CODE] = summary.get('lloc', 0)
    results[COMMENT_RATE] = (float(summary.get('comments', 0)) + float(summary.get('multi', 0))) / (float(summary.get('loc', 1)))
    results[MAINTAINABILITY_INDEX] = summary.get('mi', 0.0) / 100.0
