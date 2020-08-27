<<<<<<< HEAD
import numpy as np

=======
>>>>>>> 9c9d46d66d3bff4dae873c5a8892c49a2d50f507
def mean_in_last_week(arr):
    mean = []
    for i in range(len(arr)-6):
        mean.append(arr[i:i+7].mean())
    return np.array(mean)