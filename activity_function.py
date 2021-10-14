import math
import numpy as np
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def ReLU(x):
    return np.maximum(x,0)