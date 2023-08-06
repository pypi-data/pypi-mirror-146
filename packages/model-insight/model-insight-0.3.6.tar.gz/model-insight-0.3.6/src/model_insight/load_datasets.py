# -*- coding: utf-8 -*-
"""
Created on April 13,  2022

@author: wang Haihua
"""

from importlib_metadata import entry_points
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})

###########################################################################################
###############################     1 MCDM         ###############################
###########################################################################################

####***************************     1.1 Supplier Selection       ****************************###

def load_supplier():
    supplier = pd.read_csv('datasets/mcdm_supplier.csv')
    return supplier



















def Normalize_Weights(weights_array,norm_type = 'divide_by_sum'):
    """Normalizes a provided weight array so that the sum equals 1

    Parameters
    ----------
    weights_array : a numpy array containing the raw weights
    
    norm_type : a string specifying the type of normalization to perform
        - 'divide_by_max' divides all values by the maximum value
        - 'divide_by_sum' divides all values by the sum of the values

    Yields
    ------
    temp_weights_array: a copy of the passed weights array with the normalizations performed

    Examples
    --------
    >>> import numpy as np
    >>> import mcdm_functions as mcfunc
    >>> criteria_weights = np.array([2,4,6,7,9])
    >>> temp = mcfunc.Normalize_Weights(criteria_weights,'divide_by_max')
    >>> print(temp)
    
        [ 0.22222222  0.44444444  0.66666667  0.77777778  1.        ]
    """   
    
    temp_weights_array = weights_array.copy()
    
    if norm_type is 'divide_by_max':
        temp_weights_array = temp_weights_array/temp_weights_array.max()

    elif norm_type is 'divide_by_sum':
        temp_weights_array = temp_weights_array/temp_weights_array.sum()
        
    else:
        print('You did not enter a valid type, so no changes were made')
    
    return temp_weights_array


