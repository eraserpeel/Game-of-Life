import numpy as np

def sigmoid(x): 
    return 1 / (1 + np.exp(-x))
    
def sigmoid_derivative(x):
    out = sigmoid(x)
    return out * (1 - out)
    
def linear(x):
    return 

def linear_derivative(x):
    return 1.0

def gaussian(x): 
    return np.exp(-x**2)

def gaussian_derivative(x):
    return -2 * x * np.exp(-x**2)

def tanh(x):
    return np.tanh(x)

def tanh_derivative(x):
    return 1.0 - np.tanh(x)**2


class BackPropogationNetwork:

    def __init__(self, layer_size):
        self.layer_count = len(layer_size) - 1
        self.shape = layer_size
        self.weights = []
        self.z_layer  = []
        self.activation_layer = []
        self.previous_weight_delta = []
        self.generate_weights(layer_size)

    def generate_weights(self, layer_size):
        for (layer_1, layer_2) in zip(layer_size[:-1], layer_size[1:]):
            self.weights.append(np.random.normal(scale=0.1, size=(layer_2, layer_1 + 1)))
            self.previous_weight_delta.append(np.zeros((layer_2, layer_1 + 1)))
        

    def run(self, input):
        num_cases = input.shape[0]
        self.z_layer = []
        self.activation_layer = []

        for index in range(self.layer_count):
            if index == 0: 
                z_layer_temp = self.weights[0].dot(np.vstack([input.T, np.ones([1, num_cases])]))
            else: 
                z_layer_temp = self.weights[index].dot(np.vstack([self.activation_layer[-1], np.ones([1, num_cases])]))
            
            self.z_layer.append(z_layer_temp)
            self.activation_layer.append(sigmoid(z_layer_temp))
        # print("weights", self.weights)
        # print("------------------------")
        return self.activation_layer[-1].T


    def train_epoch(self, input, target, training_rate = 0.5, momentum = 0.5):
        delta = []
        num_cases = input.shape[0]

        self.run(input)

        for index in reversed(range(self.layer_count)):
            if index == self.layer_count - 1:
                output_delta = self.activation_layer[index] - target.T
                error = np.sum(output_delta**2)
                delta.append(output_delta * sigmoid_derivative(self.z_layer[index]))
            else: 
                delta_pullback = self.weights[index +  1].T.dot(delta[-1])
                delta.append(delta_pullback[:-1, :] * sigmoid_derivative(self.z_layer[index]))

        for index in range(self.layer_count):
            delta_index = self.layer_count - 1 - index

            if index == 0:
                layer_activation_temp = np.vstack([input.T, np.ones([1, num_cases])])
            else: 
                layer_activation_temp = np.vstack([self.activation_layer[index - 1], np.ones([1, self.activation_layer[index - 1].shape[1]])])

            # print("--------------------------------------------------")
            # print(layer_activation_temp)
            # print(delta[delta_index])   
            # print(layer_activation_temp[None, :, :].transpose(2, 0, 1))
            # print(delta[delta_index][None, :, :].transpose(2, 1, 0))

            current_weight_delta = np.sum(layer_activation_temp[None, :, :].transpose(2, 0, 1) * 
                                          delta[delta_index][None, :, :].transpose(2, 1, 0),
                                          axis = 0)            
            # print(current_weight_delta)
            # print("--------------------------------------------------")
            weight_delta = training_rate * current_weight_delta + momentum * self.previous_weight_delta[index]
            # print("outputdelta", output_delta)
            # print("deltas", delta)
            # print("weightdelta", weight_delta)
            self.weights[index] -= weight_delta
            self.previous_weight_delta[index] = weight_delta

        return error