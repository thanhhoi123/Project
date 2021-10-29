from layer import Layer
import numpy as np

class FlattenLayer(Layer):
    def __init__(self):
        pass

    def forward_propagation(self, input_data):
        self.input_batch, self.input_channel, self.row, self.column = input_data.shape
        return input_data.reshape(self.input_batch, self.input_channel * self.row * self.column)

    def backward_propagation(self, residual):
        return residual.reshape(self.input_batch, self.input_channel, self.row, self.column)