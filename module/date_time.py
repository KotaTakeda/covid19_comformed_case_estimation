# np.datetime64

import numpy as np

def datetime_array(basetime, days):
    return np.array([basetime + np.timedelta64(i, 'D') for i in range(days)])