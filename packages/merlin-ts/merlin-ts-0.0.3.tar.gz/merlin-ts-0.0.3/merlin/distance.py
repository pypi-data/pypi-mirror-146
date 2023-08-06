import warnings
import numpy as np
from scipy.spatial import distance

def distcalc(x, y, method='norm-eucledean'):
    """
    Parameters
    ----------
    x: {numpy.ndarray, list} of shape (, n_samples)
        vector.

    y: {numpy.ndarray, list} of shape (, n_samples)
        vector.
    """
    
    if "norm-eucledean":
        return np.sqrt(np.mean((x - y) ** 2))
    elif "eucledean":
        return np.linalg.norm(x - y, ord=2)
    elif "chebyshev":
        return distance.chebyshev(x, y)
    else:
        warnings.warn("Please specify a valid distance metric name.")
        return -1