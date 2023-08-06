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
import datetime 
plt.rcParams.update({'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})

###########################################################################################
###############################     1 MCDM         ###############################
###########################################################################################

####***************************     1.1 Supplier Selection       ****************************###

def load_supplier():
    data = np.array([[ 2.42,  2.8 ,  8.25,  3.09,  8.21,  1.05,  8.  ,  0.75],
       [ 6.51,  1.88,  3.6 ,  6.45,  4.31,  1.21, 13.  ,  0.83],
       [ 8.51,  1.06,  2.97,  9.36,  5.06,  1.22, 12.  ,  0.91],
       [ 4.63,  4.6 ,  5.84,  7.34,  9.2 ,  1.01,  9.  ,  0.72],
       [ 4.62,  7.44,  1.5 ,  8.93,  4.01,  1.03,  7.  ,  0.97],
       [ 7.87,  6.58,  2.93,  6.88,  6.3 ,  1.18, 14.  ,  0.83],
       [ 8.87,  5.94,  3.32,  7.45,  3.  ,  1.13,  6.  ,  1.  ],
       [ 9.15,  4.35,  1.28,  9.2 ,  3.07,  1.04, 15.  ,  0.81],
       [ 8.16,  2.39,  1.74,  8.8 ,  9.41,  1.02,  8.  ,  0.95],
       [ 1.66,  7.7 ,  4.11,  5.76,  5.72,  1.1 , 11.  ,  0.98],
       [ 4.84,  1.58,  9.35,  6.22,  6.59,  1.15,  5.  ,  0.72],
       [ 9.9 ,  2.64,  6.02,  2.34,  8.75,  1.18,  3.  ,  0.71],
       [ 2.91,  1.63,  8.38,  9.87,  1.63,  1.15, 13.  ,  0.87],
       [ 9.05,  9.7 ,  7.03,  7.59,  2.77,  1.04,  8.  ,  0.9 ],
       [ 2.73,  4.66,  1.26,  5.32,  8.42,  1.27, 15.  ,  0.86],
       [ 2.87,  8.49,  8.87,  4.37,  4.04,  1.05, 15.  ,  0.99],
       [ 7.89,  8.75,  4.84,  3.36,  7.51,  1.27,  5.  ,  0.99],
       [ 5.49,  5.26,  9.72,  6.11,  8.87,  1.15, 13.  ,  0.93],
       [ 9.48,  8.47,  3.42,  7.91,  2.62,  1.25,  2.  ,  0.83],
       [ 3.85,  1.16,  9.08,  7.28,  1.05,  1.24, 10.  ,  0.71],
       [ 9.97,  3.4 ,  7.98,  6.43,  9.3 ,  1.07,  6.  ,  0.86],
       [ 7.71,  1.43,  7.12,  3.16,  2.33,  1.26, 11.  ,  0.97],
       [ 5.94,  2.92,  7.56,  4.93,  9.69,  1.28,  7.  ,  0.73],
       [ 3.17,  2.97,  6.01,  2.99,  8.24,  1.15,  3.  ,  0.79],
       [ 2.32,  8.54,  8.21,  5.44,  4.09,  1.02, 11.  ,  0.82],
       [ 8.84,  2.85,  9.89,  7.04,  3.89,  1.05, 14.  ,  0.89],
       [ 6.2 ,  9.97,  3.9 ,  9.54,  7.04,  1.07, 13.  ,  0.73],
       [ 4.37,  7.5 ,  2.15,  9.57,  5.18,  1.23, 13.  ,  0.9 ],
       [ 1.23,  6.58,  2.16,  2.53,  1.65,  1.07,  9.  ,  0.71],
       [ 7.31,  9.63,  6.1 ,  1.19,  3.31,  1.21,  8.  ,  0.83],
       [ 2.05,  3.17,  3.27,  6.93,  4.12,  1.16,  2.  ,  0.82],
       [ 6.32,  5.18,  5.99,  4.46,  4.61,  1.13,  6.  ,  0.95],
       [ 2.18,  2.7 ,  4.14,  4.91,  6.24,  1.02,  2.  ,  0.95],
       [ 3.52,  4.51,  5.25,  2.08,  9.53,  1.2 , 15.  ,  0.75],
       [ 9.09,  4.62,  6.14,  1.77,  1.7 ,  1.05, 13.  ,  0.78],
       [ 8.85,  7.46,  7.86,  7.3 ,  4.18,  1.06, 10.  ,  0.78],
       [ 4.33,  5.27,  7.56,  2.76,  5.09,  1.19,  5.  ,  0.92],
       [ 7.08,  9.1 ,  2.77,  7.08,  7.8 ,  1.27,  2.  ,  0.8 ],
       [ 5.16,  8.31,  1.24,  2.08,  7.01,  1.17, 12.  ,  0.99],
       [ 9.34,  3.97,  7.94,  1.09,  1.3 ,  1.14,  9.  ,  0.78],
       [ 5.67,  8.87,  6.1 ,  6.99,  5.51,  1.03, 10.  ,  0.83],
       [ 1.52,  5.67,  2.64,  6.55,  5.07,  1.01,  9.  ,  0.97],
       [ 9.77,  3.18,  8.64,  2.08,  2.26,  1.1 ,  7.  ,  0.75],
       [ 5.79,  2.63,  1.59,  4.97,  3.71,  1.06, 11.  ,  0.86],
       [ 8.93,  1.16,  5.54,  2.65,  5.89,  1.13,  4.  ,  0.85],
       [ 6.97,  7.13,  5.71,  7.73,  6.76,  1.22,  8.  ,  0.93],
       [ 1.89,  5.08,  1.25,  4.88,  3.43,  1.17,  7.  ,  0.82],
       [ 9.34,  5.29,  7.61,  8.26,  9.71,  1.21,  8.  ,  0.75],
       [ 1.74,  2.12,  6.17,  4.61,  6.9 ,  1.09,  2.  ,  0.94],
       [ 8.96,  2.02,  5.52,  5.1 ,  8.33,  1.04, 13.  ,  0.71],
       [ 8.45,  6.51,  7.1 ,  6.31,  8.14,  1.28, 14.  ,  0.87],
       [ 6.83,  9.46,  1.55,  2.19,  8.23,  1.3 ,  6.  ,  0.97],
       [ 2.43,  9.18,  2.6 ,  4.55,  8.02,  1.13,  2.  ,  0.84],
       [ 2.58,  8.2 ,  9.54,  3.71,  4.64,  1.08,  3.  ,  0.9 ],
       [ 3.92,  6.28,  8.99,  4.01,  4.59,  1.12,  6.  ,  0.96],
       [ 3.52,  2.53,  4.3 ,  8.52,  9.81,  1.19,  3.  ,  0.9 ],
       [ 6.28,  6.16,  9.7 ,  9.14,  7.34,  1.11, 13.  ,  0.75],
       [ 6.61,  2.74,  5.61,  8.7 ,  6.19,  1.21,  6.  ,  0.7 ],
       [ 7.72,  9.74,  9.4 ,  8.36,  2.39,  1.19,  3.  ,  0.78],
       [ 6.14,  8.44,  3.67,  2.22,  7.78,  1.3 , 13.  ,  0.8 ],
       [ 9.65,  8.21,  4.28,  6.35,  4.43,  1.21,  5.  ,  0.72],
       [ 2.44,  8.12,  1.69,  1.64,  2.92,  1.14,  4.  ,  0.84],
       [ 1.72,  1.12,  4.46,  5.47,  8.23,  1.29,  4.  ,  0.73],
       [ 9.36,  8.77,  5.19,  2.4 ,  6.  ,  1.21,  8.  ,  0.87],
       [ 1.41,  5.75,  8.66,  8.02,  3.3 ,  1.21,  5.  ,  0.95],
       [ 1.41,  9.27,  2.75,  1.37,  2.75,  1.07,  2.  ,  0.7 ],
       [ 1.4 ,  4.99,  7.81,  5.59,  2.06,  1.1 ,  7.  ,  0.97],
       [ 6.84,  6.79,  6.57,  6.  ,  8.2 ,  1.17,  4.  ,  0.9 ],
       [ 9.94,  9.48,  9.12,  2.16,  7.14,  1.15,  2.  ,  0.9 ],
       [ 8.39,  2.26,  9.22,  4.23,  1.39,  1.21,  3.  ,  0.78],
       [ 7.22,  6.58,  3.63,  3.98,  1.39,  1.21, 11.  ,  0.89],
       [ 3.05,  1.88,  8.85,  1.68,  9.1 ,  1.07,  6.  ,  1.  ],
       [ 5.15,  2.13,  9.86,  7.81,  7.89,  1.24,  2.  ,  0.79],
       [ 7.8 ,  3.83,  2.02,  2.97,  8.03,  1.22,  2.  ,  0.71],
       [ 6.2 ,  6.81,  9.82,  1.83,  3.64,  1.14,  6.  ,  0.92],
       [ 1.22,  6.97,  6.55,  7.39,  9.1 ,  1.28, 11.  ,  0.76],
       [ 3.58,  1.99,  8.13,  4.22,  1.04,  1.02,  8.  ,  0.84],
       [ 9.85,  2.84,  5.07,  8.7 ,  3.57,  1.06, 11.  ,  0.86],
       [ 8.05,  4.59,  6.97,  7.89,  6.96,  1.21,  2.  ,  0.81],
       [ 5.18,  2.12,  2.34,  9.27,  7.61,  1.16,  3.  ,  0.74],
       [ 4.74,  2.03,  1.07,  7.62,  3.75,  1.27,  4.  ,  0.88],
       [ 6.52,  7.53,  2.89,  2.67,  5.79,  1.02, 15.  ,  0.72],
       [ 4.48,  8.22,  5.41,  9.34,  6.71,  1.28,  8.  ,  0.71],
       [ 6.73,  4.39,  8.63,  1.11,  3.04,  1.21,  8.  ,  0.92],
       [ 7.14,  8.41,  1.07,  8.1 ,  9.32,  1.22,  3.  ,  0.8 ],
       [ 1.96,  4.49,  4.47,  3.69,  2.82,  1.1 , 15.  ,  0.7 ],
       [ 3.97,  4.45,  7.6 ,  5.41,  2.7 ,  1.28,  8.  ,  0.93],
       [ 2.69,  8.84,  9.69,  5.81,  6.2 ,  1.07,  6.  ,  0.83],
       [ 6.86,  3.49,  3.24,  5.41,  4.34,  1.06,  4.  ,  0.99],
       [ 3.39,  2.74,  8.46,  2.83,  3.08,  1.06, 13.  ,  0.8 ],
       [ 3.68,  9.76,  4.93,  7.37,  5.3 ,  1.26, 11.  ,  0.97],
       [ 6.72,  1.5 ,  5.09,  7.41,  9.08,  1.25,  5.  ,  0.74],
       [ 5.76,  1.9 ,  1.79,  4.09,  1.54,  1.04, 15.  ,  0.76],
       [ 4.92,  7.8 ,  5.26,  7.15,  1.84,  1.25, 15.  ,  0.82],
       [ 3.44,  6.82,  5.43,  5.97,  8.91,  1.27, 12.  ,  0.83],
       [ 8.89,  7.72,  4.19,  7.64,  4.14,  1.14,  3.  ,  0.84],
       [ 7.57,  5.47,  4.67,  4.54,  9.68,  1.16, 15.  ,  0.85],
       [ 7.65,  2.07,  9.68,  9.75,  4.2 ,  1.28,  3.  ,  0.87],
       [ 8.88,  6.09,  6.65,  1.49,  3.98,  1.09, 10.  ,  0.96],
       [ 6.76,  9.71,  6.19,  2.13,  5.5 ,  1.11,  8.  ,  0.98]])
    index = [  1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,
             14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,
             27,  28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,  39,
             40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,
             53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,  65,
             66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,
             79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,
             92,  93,  94,  95,  96,  97,  98,  99, 100]
    feature_names = ['Warranty Terms', 'Payment Terms', 'Technical Support',
       'Sustainability Efforts', 'Financial Stability', 'Unit Cost',
       'Lead Time (Days)', 'On Time Delivery']
    supplier = pd.DataFrame(data=data,index = index,columns = feature_names)
    return supplier


####***************************     1.2 Roller Cosater       ****************************###

def load_roller20():
    data = np.array([['10 Inversion Roller Coaster', 'Chimelong Paradise', 'Panyu',
        'Guangzhou, Guangdong', 'China', 'Asia', 'Steel', 'Sit Down',
        'Operating', 2006, 98.4, 45.0, 2788.8, 'YES', 10, nan,
        datetime.time(1, 32), nan, nan],
       ['Abismo', 'Parque de Atracciones de Madrid', 'Madrid', 'Madrid',
        'Spain', 'Europe', 'Steel', 'Sit Down', 'Operating', 2006, 151.6,
        65.2, 1476.4, 'YES', 2, nan, datetime.time(1, 0), 4, nan],
       ['Adrenaline Peak', 'Oaks Amusement Park', 'Portland', 'Oregon',
        'United States', 'North America', 'Steel', 'Sit Down',
        'Operating ', 2018, 72, 45.0, 1050.0, 'YES', 3, nan, nan, nan,
        97.0],
       ['Afterburn', 'Carowinds', 'Charlotte', 'North Carolina',
        'United States', 'North America', 'Steel', 'Inverted',
        'Operating', 1999, 113, 62.0, 2956.0, 'YES', 6, nan,
        datetime.time(2, 47), nan, nan],
       ['Alpengeist', 'Busch Gardens Williamsburg', 'Williamsburg',
        'Virginia', 'United States', 'North America', 'Steel',
        'Inverted', 'Operating', 1997, 195, 67.0, 3828.0, 'YES', 6, 170,
        datetime.time(3, 10), 3.7, nan],
       ['Alpina Blitz', 'Nigloland', 'Dolancourt', 'Champagne-Ardenne',
        'France', 'Europe', 'Steel', 'Sit Down', 'Operating', 2014,
        108.3, 51.6, 2358.9, 'NO', 0, nan, nan, 4.3, nan],
       ['Altair', 'Cinecittà World', 'Rome', 'Rome', 'Italy', 'Europe',
        'Steel', 'Sit Down', 'Operating', 2014, 108.3, 52.8, 2879.8,
        'YES', 10, nan, nan, nan, nan],
       ['American Eagle', 'Six Flags Great America', 'Gurnee',
        'Illinois', 'United States', 'North America', 'Wood', 'Sit Down',
        'Operating', 1981, 127, 66.0, 4650.0, 'NO', 0, 147,
        datetime.time(2, 23), nan, 55.0],
       ['Anaconda', 'Walygator Parc', 'Maizieres-les-Metz ', 'Lorraine',
        'France', 'Europe', 'Wood', 'Sit Down', 'Operating', 1989, 118.1,
        55.9, 3937.0, 'NO', 0, 40, datetime.time(2, 10), nan, nan],
       ['Apocalypse', 'Six Flags America', 'Upper Marlboro', 'Maryland',
        'United States', 'North America', 'Steel', 'Stand Up',
        'Operating', 2012, 100, 55.0, 2900.0, 'YES', 2, 90,
        datetime.time(2, 0), nan, nan],
       ['Apocalypse the Ride', 'Six Flags Magic Mountain', 'Valencia',
        'California', 'United States', 'North America', 'Wood',
        'Sit Down', 'Operating', 2009, 95, 50.1, 2877.0, 'NO', 0, 87.3,
        datetime.time(3, 0), nan, nan],
       ["Apollo's Chariot", 'Busch Gardens Williamsburg', 'Williamsburg',
        'Virginia', 'United States', 'North America', 'Steel',
        'Sit Down', 'Operating', 1999, 170, 73.0, 4882.0, 'NO', 0, 210,
        datetime.time(2, 15), 4.1, 65.0],
       ['Atlantica SuperSplash', 'Europa Park', 'Rust ',
        'Baden Wuerttemberg', 'Germany', 'Europe', 'Steel', 'Sit Down',
        'Operating', 2005, 98.4, 49.7, 1279.5, 'NO', 0, nan,
        datetime.time(3, 20), nan, nan],
       ['Backlot Stunt Coaster', 'Kings Island', 'Kings Mills', 'Ohio',
        'United States', 'North America', 'Steel', 'Sit Down',
        'Operating', 2005, 45.2, 40.0, 1960.0, 'NO', 0, 31.2,
        datetime.time(1, 4), nan, nan],
       ['Balder', 'Liseberg', 'Gothenburg', 'Vastra Gotaland', 'Sweden',
        'Europe', 'Wood', 'Sit Down', 'Operating', 2003, 118.1, 55.9,
        3510.5, 'NO', 0, nan, datetime.time(2, 8), nan, 70.0],
       ['Bandit', 'Movie Park Germany', 'Bottrop ',
        'North Rhine-Westphali', 'Germany', 'Europe', 'Wood', 'Sit Down',
        'Operating', 1999, 91.2, 49.7, 3605.7, 'NO', 0, 81.7,
        datetime.time(1, 30), nan, nan],
       ['Banshee', 'Kings Island', 'Mason', 'Ohio', 'United States',
        'North America', 'Steel', 'Inverted', 'Operating', 2014, 167,
        68.0, 4124.0, 'YES', 7, 150, datetime.time(2, 40), nan, nan],
       ['Bat', 'Kings Island', 'Kings Mills', 'Ohio', 'United States',
        'North America', 'Steel', 'Suspended', 'Operating', 1993, 78,
        51.0, 2352.0, 'NO', 0, nan, datetime.time(1, 52), nan, nan],
       ['Batman - The Dark Knight', 'Six Flags New England', 'Agawam',
        'Massachusetts', 'United States', 'North America', 'Steel',
        'Sit Down', 'Operating ', 2002, 117.8, 55.0, 2600.0, 'YES', 5,
        nan, datetime.time(2, 20), nan, nan],
       ['Batman The Ride', 'Six Flags Great America', 'Gurnee',
        'Illinois', 'United States', 'North America', 'Steel',
        'Inverted', 'Operating', 1992, 100, 50.0, 2700.0, 'YES', 5, nan,
        datetime.time(2, 0), nan, nan]])
    index = range(len(data))
    feature_names = ['Name', 'Park', 'City/Region', 'City/State/Region', 'Country/Region',
       'Geographic Region', 'Construction', 'Type', 'Status',
       'Year/Date Opened', 'Height (feet)', ' Speed (mph)', 'Length (feet)',
       'Inversions (YES or NO)', 'Number of Inversions', 'Drop (feet)',
       'Duration (min:sec)', 'G Force', 'Vertical Angle (degrees)']
    roller = pd.DataFrame(data=data,index = index,columns = feature_names)
    return roller


####***************************     1.3 Aircraft       ****************************###

def load_aircraft():
    data = np.array([[2.0e+00, 1.5e+03, 2.0e+04, 5.5e+06, 5.0e-01, 1.0e+00],
       [2.5e+00, 2.7e+03, 1.8e+04, 6.5e+06, 3.0e-01, 5.0e-01],
       [1.8e+00, 2.0e+03, 2.1e+04, 4.5e+06, 7.0e-01, 7.0e-01],
       [2.2e+00, 1.8e+03, 2.0e+04, 5.0e+06, 5.0e-01, 5.0e-01]])
    index = list('ABCD')
    feature_names = ['最大速度(马赫)', '飞行范围(km)', '最大负载(磅)', '费用(美元)', '可靠性', '灵敏性']
    aircraft = pd.DataFrame(data=data,index = index,columns = feature_names)
    return aircraft











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


