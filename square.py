import numpy as np


def square(t, duty, timeP, len):
    x=np.empty(len)
    for i in range(len):
        if t[i]%timeP<=duty*timeP:
            x[i]=1
        else:
            x[i]=0
    return x
