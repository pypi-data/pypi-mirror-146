import numpy as np
from .candidate_selection import candidate_select
from .discords_refinement import discords_refine

def drag(series, subseq_len, r, dist_method='norm-eucledean'):
    """Discords Refinement Algorithms

    Parameters
    ----------
    series: {numpy.ndarrays, list}
        Time series or signals to be test.
        
    subseq_len : int
        Subsequence length.
        
    r : int
        Range of discords.
    
    dist_method: str
        Distance measurement.
        
    Returns
    -------
    discords : list
        List containing [anomaly index, subsequence length, anomaly score]
    """
    
    
    candidates = candidate_select(series, subseq_len, r, dist_method)
    discords = discords_refine(candidates, series, subseq_len, r, dist_method)
    return discords