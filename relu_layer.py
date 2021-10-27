from layer import Layer
import numpy as np

class ReLULayer(Layer):
    def __init__(self):
        pass

    def forward_propagation(self, input_data):
        self.top_val = input_data
        ret = input_data
        ret[ret < 0] = 0
        return ret

    def backward_propagation(self, residual):
        gradient_x = residual
        gradient_x[self.top_val < 0] = 0
        return gradient_x
        