from layer import Layer
import numpy as np

class MaxPoolingLayer(Layer):
    def __init__(self, kernel_size, name='MaxPool'):
        self.kernel_size = kernel_size

    def forward(self, input_data):
        input_batch, input_channel, input_row, input_col = input_data.shape
        k = self.kernel_size
        output_row = input_row / k + (1 if input_row % k != 0 else 0)
        output_col = input_col / k + (1 if input_col % k != 0 else 0)

        self.flag = np.zeros_like(input_data)
        ret = np.empty((input_batch, input_channel, output_row, output_col))
        for b_id in range(input_batch):
            for c in range(input_channel):
                for oy in range(output_row):
                    for ox in range(output_col):
                        height = k if (oy + 1) * k <= input_row else input_row - oy * k
                        width = k if (ox + 1) * k <= input_col else input_col - ox * k
                        idx = np.argmax(input_data[b_id, c, oy * k: oy * k + height, ox * k: ox * k + width])
                        offset_row = idx / width
                        offset_col = idx % width
                        self.flag[b_id, c, oy * k + offset_row, ox * k + offset_col] = 1
                        ret[b_id, c, oy, ox] = input_data[b_id, c, oy * k + offset_row, ox * k + offset_col]
        return ret
    def backward(self, residual):
        input_batch, input_channel, input_row, input_col = self.flag
        k = self.kernel_size
        output_row, output_col = residual.shape[2], residual.shape[3]

        gradient_x = np.zeros_like(self.flag)
        for b_id in range(input_batch):
            for c in range(input_channel):
                for oy in range(output_row):
                    for ox in range(output_col):
                        height = k if (oy + 1) * k <= input_row else input_row - oy * k
                        width = k if (ox + 1) * k <= input_col else input_col - ox * k
                        #Bonus
                        idx = np.argmax(residual[b_id, c, oy * k: oy * k + height, ox * k: ox * k + width])
                        offset_row = idx / width
                        offset_col = idx % width
                        self.flag[b_id, c, oy * k + offset_row, ox * k + offset_col] = 1
                        ######
                        gradient_x[b_id, c, oy * k + offset_row, ox * k + offset_col] = residual[b_id, c, oy, ox]
        gradient_x[self.flag == 0] = 0
        return gradient_x
