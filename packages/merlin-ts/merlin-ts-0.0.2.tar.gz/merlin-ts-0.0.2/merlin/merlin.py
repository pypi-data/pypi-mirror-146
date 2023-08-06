import numpy as np
from pprint import pprint
from time import time
from .distance import distcalc
from .drag import *
import warnings
warnings.filterwarnings("ignore")


# MERLIN
def merlin(series, minL, maxL):
    """
    Parameters
    ----------
    series: {numpy.ndarray, list} of shape (, n_samples)
        Time series.
        
    minL: int
        Subsequence length lower bound.
    
    maxL: int
        Subsequence length upper bound.
    
    Return 
    ----------
    discords: list
        Set of discords include the information of 
        (1) Starting indices of the discords, 
        (2) Subsequence length, 
        (3) The distance between each discord and its nearest neighbor.
    
    discords_: list
        The most anoamoulous record.
    """
    
    maxint = np.inf
    r = 2 * np.sqrt(minL)
    dminL = - maxint
    discords = []
    while dminL < 0:
        D = drag(series, minL, r)
        r = r / 2
        
        if D.shape[0] != 0: 
            break
            
    rstart = r
    distances = [-maxint] * 4
    for i in range(minL, min(minL+4, maxL)):
        di = distances[i - minL]
        dim1 = rstart if i == minL else distances[i - minL - 1]
        r = 0.99 * dim1
        while di < 0:
            D = drag(series, i, r)
            if D is not []:
                di = np.max([p[2] for p in D])
                distances[i - minL] = di
                discords += list(D)
            r = r * 0.99

    for i in range(minL + 4, maxL + 1):
        M = np.mean(distances)
        S = np.std(distances) + 1e-2
        r = M - 2 * S
        di = - maxint
        
        while di < 0:
            D = drag(series, i, r)
            if D: 
                di = np.max([p[2] for p in D])
                discords += D
                
            r = r - S
            
    ndist = []
    for d in discords: 
        if d[2] != maxint: 
            ndist.append(d[2])
            
    dmax = np.argmax(ndist)
    return discords, discords[dmax]
