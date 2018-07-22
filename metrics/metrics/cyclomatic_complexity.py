# -*- coding: UTF-8 -*-

from radon.cli.harvest import CCHarvester
from radon.complexity import SCORE
from radon.cli import Config

from ..results import MAX_CYCLOMATIC_COMPLEXITY, MAX_CYCLOMATIC_COMPLEXITY_FUNCTION, AVERAGE_CYCLOMATIC_COMPLEXITY

def cyclomatic_complexity(code_path, results):
    """
    Compute all available metrics.

    :param code_path: Path to the source code.
    :param results: Dictionary with the results.
    """
    h = CCHarvester([code_path],
                    Config(min='A', max='F', exclude=None, ignore=None, show_complexity=False, average=False,
                           total_average=False, order=SCORE, no_assert=False, show_closures=False))

    max_complexity = 0
    max_complexity_function = "" # Maximum complexity function pointer
    avg_complexity = 0 # Weighted average complexity by the number of functions
    avg_weight = 0 # Total weight used to compute the average complexity
    for file_path, metrics in h.results:
        for m in metrics:
            # Average
            avg_complexity += m.complexity
            avg_weight += 1

            # Maximum
            if max_complexity < m.complexity:
                max_complexity = m.complexity
                max_complexity_function = "%s in %s:%s with complexity %s" % (m.fullname, file_path, m.lineno, m.complexity)

    # Finish the weighted average
    if avg_weight > 0.0:
        avg_complexity /= avg_weight

    # Populate results
    results[AVERAGE_CYCLOMATIC_COMPLEXITY] = avg_complexity
    results[MAX_CYCLOMATIC_COMPLEXITY] = max_complexity
    results[MAX_CYCLOMATIC_COMPLEXITY_FUNCTION] = max_complexity_function
