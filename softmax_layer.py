from layer import Layer
import numpy as np

class SoftmaxLayer(Layer):
    def __init__(self):
        pass

    def forward_propagation(self, input_data):
        exp_out = np.exp(input_data)
        self.top_val = exp_out / np.sum(exp_out, axis=1)
        return self.top_val

    def backward_propagation(self, residual):
        return self.top_val - residual