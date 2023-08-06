import numpy as np
from .distance import distcalc
import warnings



def discords_refine(candidates, series, subseq_len, r, dist_method='norm-eucledean'):
    """
    Parameters
    ----------
    candidates: list
        Candidate set of discords.
        
    series: {numpy.ndarray, list} of shape (, n_samples)
        Time series.
        
    subseq_len: int
        Subsequence length.
        
    r: float
        Range of discords.
    
    Return 
    ----------
    discords: list
        Set of discords include the information of 
        (1) Starting indices of the discords, 
        (2) Subsequence length, 
        (3) The distance between each discord and its nearest neighbor.
        
    """
    
    d_min = np.inf
    
    if candidates == []:
        return np.array([])
    
    series = np.array(series)
    discords = list()
    length = len(series)
    
    for i in range(1, length-subseq_len+1):
        is_discord = True
        
        for j in candidates:
            if i != j:
                dist = distcalc(series[i:i+subseq_len], series[j:j+subseq_len], method=dist_method)
                
                if dist < r:
                    candidates.remove(j)
                    is_discord = False
                else:
                    d_min = min(d_min, dist)
                    
        if is_discord:
            discords.append([j, subseq_len, d_min]) # the third column define the anomaly degree
            
    discords = np.array(discords)
    
    return discords[np.argsort(discords[:, 2])]