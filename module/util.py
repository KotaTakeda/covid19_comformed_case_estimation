def mean_in_last_week(arr):
    mean = []
    for i in range(len(arr)-6):
        mean.append(arr[i:i+7].mean())
    return np.array(mean)