import numpy as np


def gini_coefficient(x):
    mad = np.abs(np.subtract.outer(x, x)).mean()
    relative_mad = mad / np.mean(x)
    return 0.5 * relative_mad
