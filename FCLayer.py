from layer import Layer
import numpy as np

class FCLayer(Layer):
    def __init__(self, input_num, output_num, learning_rate = 0.01, momentum = 0.9):
        self.input_num = input_num
        self.output_num = output_num
        self.weighs = np.random.rand(input_num, output_num)
        self.bias = np.random.rand(output_num, 1)
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.prev_grad_W = np.zeros_like(self.weighs)
        self.prev_grad_b = np.zeros_like(self.bias)
    
    def forward_propagation(self, input_data):
        self.topVal = np.dot(self.weighs.T, input_data) + self.bias
        self.bottomVal = input_data
        return self.topVal
    
    def backward_propagation(self, loss):
        batch_size = loss.shape[0]
        grad_w = np.dot(self.bottomVal, loss.T) / batch_size
        grad_b = np.sum(loss) / batch_size
        residual_x = np.dot(self.weighs, loss)
        self.prev_grad_w = self.prev_grad_w * self.momentum - grad_w
        self.prev_grad_b = self.prev_grad_b * self.momentum - grad_b
        self.weighs -= self.learning_rate * self.prev_grad_w
        self.bias -= self.learning_rate * self.prev_grad_b
        return residual_x
