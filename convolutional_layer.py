from layer import Layer
import numpy as np

def conv2(X, k):    
    x_row, x_col = X.shape
    k_row, k_col = k.shape
    data_row, data_col = x_row - k_row + 1, x_col - k_col + 1
    data = np.empty((data_row, data_col))
    for y in range(data_row):
        for x in range(data_col):
            sub = X[y : y + k_row, x : x + k_col]
            data[y,x] = np.sum(sub * k)
    return data

def padding(in_data, size):
    cur_r, cur_w = in_data.shape[0], in_data.shape[1]
    new_r = cur_r + size * 2
    new_w = cur_w + size * 2
    ret = np.zeros((new_r, new_w))
    ret[size:cur_r + size, size:cur_w+size] = in_data
    return ret

def rot180(in_data):
    ret = in_data.copy()
    yEnd = ret.shape[0] - 1
    xEnd = ret.shape[1] - 1
    for y in range(ret.shape[0] / 2):
        for x in range(ret.shape[1]):
            ret[yEnd - y][x] = ret[y][x]
    for y in range(ret.shape[0]):
        for x in range(ret.shape[1] / 2):
            ret[y][xEnd - x] = ret[y][x]
    return ret

class ConvolutuionnalLayer(Layer):
    def __init__(self, input_chanel, output_chanel, kernel_size, learing_rate = 0.01, momentum = 0.9):
        self.weight = np.random.randn(input_chanel, output_chanel, kernel_size, kernel_size)
        self.bias = np.zeros(output_chanel)
        self.learing_rate = learing_rate 
        self.momentum = momentum

        self.prev_gradient_w = np.zeros_like(self.weight) 
        self.prev_gradient_b = np.zeros_like(self.bias)

    def forward_propagation(self, input_data):        
        input_batch, input_channel, input_row, input_col = input_data.shape
        output_chanel, kernel_size = self.weight.shape[1], self.weight.shape[2]
        self.top_val = np.zeros(input_batch, output_chanel, input_row - kernel_size + 1, input_col - kernel_size + 1)
        self.bottom_val = input_data

        for b_id in range(input_batch):
            for o in range(output_chanel):
                for i in range(input_channel):
                    self.top_val[b_id, o] += conv2(input_data[b_id, i], self.weight[i, o])
                self.top_val[b_id, o] += self.bias[o]
        return self.top_val

    def backward_propagation(self, residual):
        input_channel, output_channel, kernel_size = self.weight.shape
        input_batch = residual.shape[0]

        # gradient_b
        self.gradient_b = residual.sum(axis=3).sum(axis=2).sum(axis=0) / input_batch #Tổng tất cả các pixel trong ma trận lỗi chia cho số ma trận trả về mảng 1 chiều
        # gradient_w
        self.gradient_w = np.zeros_like(self.w)
        for b_id in range(input_batch):
            for i in range(input_channel):
                for o in range(output_channel):
                    self.gradient_w[i, o] += conv2(self.bottom_val[b_id], residual[o])
        self.gradient_w /= input_batch
        # gradient_x
        gradient_x = np.zeros_like(self.bottom_val)
        for b_id in range(input_batch):
            for i in range(input_channel):
                for o in range(output_channel):
                    gradient_x[b_id, i] += conv2(padding(residual, kernel_size - 1), rot180(self.weight[i, o])) #??????
        gradient_x /= input_batch
        # update
        self.prev_gradient_w = self.prev_gradient_w * self.momentum - self.gradient_w
        self.weight += self.learing_rate * self.prev_gradient_w
        self.prev_gradient_b = self.prev_gradient_b * self.momentum - self.gradient_b
        self.bias += self.learing_rate * self.prev_gradient_b
        return gradient_x


    
        
