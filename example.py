import numpy as np

def relu(z):
    return np.maximum(0,z)

def relu_prime(z):
    z(z < 0) = 0
    z(z > 0) = 1
    return z

def loss(y_true, y_predict):
    return 0.5*(y_predict - y_true)**2

def loss_prime(y_true, y_predict):
    return y_predict - y_true
