from abc import abstractmethod

class Layer:
    def __init__(self):
        self.input = None
        self.output = None
        self.input_shape = None
        self.output_shape = None
        raise NotImplementedError   

    @abstractmethod
    def forward_propagation(self, input_data):
        raise NotImplementedError
    
    @abstractmethod
    def backward_propagation(self, residual):
        raise NotImplementedError