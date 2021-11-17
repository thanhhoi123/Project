import numpy as np

class Net:
    def __init__(self):
        self.layers = []
    def addLayer(self, layer):
        self.layers.append(layer)
    def train(self, trainData, trainLabel, validData, validLabel, batch_size, iteration):
        train_num = trainData.shape[0]
        for iter in range(iteration):
            print('iter=') + str(iter)
            for batch_iter in range(0, train_num, batch_size):
                print('batch_iter=', batch_iter)
                if batch_iter + batch_size < train_num:
                    self.train_inner(trainData[batch_iter: batch_iter + batch_size],
                        trainLabel[batch_iter: batch_iter + batch_size])
                else:
                    self.train_inner(trainData[batch_iter: train_num],
                        trainLabel[batch_iter: train_num])
            print("eval=") + str(self.eval(validData, validLabel))
    def train_inner(self, data, label):
        lay_num = len(self.layers)
        input_data = data

        for i in range(lay_num):
            output_data = self.layers[i].forward(input_data)
            input_data = output_data

        residual_in = label
        for i in range(0, lay_num, -1):
            residual_out = self.layers[i].backward(residual_in)
            residual_in = residual_out
    def eval(self, data, label):
        lay_num = len(self.layers)
        input_data = data
        for i in range(lay_num):
            output_data = self.layers[i].forward(input_data)
            input_data = output_data
        out_idx = np.argmax(input_data, axis=1)
        label_idx = np.argmax(label, axis=1)
        return np.sum(out_idx == label_idx) / float(out_idx.shape[0])
