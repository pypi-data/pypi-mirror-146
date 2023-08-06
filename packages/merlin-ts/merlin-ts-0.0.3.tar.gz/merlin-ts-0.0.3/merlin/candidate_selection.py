import numpy as np
from .distance import distcalc
import warnings


def candidate_select(series, subseq_len, r, dist_method='norm-eucledean'):
    """
    Parameters
    ----------
    series: {numpy.ndarray, list} of shape (, n_samples)
        Time series.
        
    subseq_len: int
        Subsequence length.
        
    r: float
        Range of discords.
    
    Return 
    ----------
    candidates: list
        Candidates set of discords.
        
    """
    
    series = np.array(series)
    candidates = list()
    length = len(series)
 
    for i in range(1, length-subseq_len+1): # Scan all subsequences
        is_candidate = True
        for j in candidates:
            if i != j:
                if distcalc(series[i:i+subseq_len], series[j:j+subseq_len], method=dist_method) < r:
                    candidates.remove(j)
                    is_candidate = False
        if is_candidate and i not in candidates:
            candidates.append(i)
        
    if len(candidates) == 0:
        warnings.warn("Fail to capture the candidates.")
    
    return candidates 
