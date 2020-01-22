import numpy as np

def integration(vect, delta_t, v0):
    """ Basic Integration """

    v = []
    i = 0
    for i in range(len(vect)):
        if i==0 :
            v.append(delta_t[i] * vect[i] + v0)
        else:
            v.append(delta_t[i] * vect[i] + v[i-1])
    return v