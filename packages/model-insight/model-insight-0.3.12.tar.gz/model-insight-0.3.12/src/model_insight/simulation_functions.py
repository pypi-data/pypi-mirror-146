# -*- coding: utf-8 -*-
"""
Created on April 13,  2022

@author: wang Haihua
"""

from importlib_metadata import entry_points
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import math
plt.rcParams.update({'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})

###########################################################################################
###############################     1 Queuing Theory        ###############################
###########################################################################################

####***************************     1.1 Normalization       ****************************###

def queue_p0(c,lam,mu):
    '''
    c: Number of service desks
    lam: Average rate of customer arrivals
    mu: Average rate of system services
    '''
    a1 = sum([1/math.factorial(k)*(lam/mu)**k for k in range(c)])
    a2 = (1/math.factorial(c))*(1/(1-lam/(c*mu))*(lam/mu)**c)
    return 1/(a1+a2)


def average_queue(c,lam,mu):
    '''
    c: Number of service desks
    lam: Average rate of customer arrivals
    mu: Average rate of system services
    '''
    p0 = queue_p0(c,lam,mu)
    rou = lam/(c*mu)
    b1 = (c*rou)**c*rou
    b2 = math.factorial(c)*(1-rou)**2
    return b1/b2*p0
