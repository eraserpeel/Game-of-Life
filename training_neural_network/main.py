from neural_network import BackPropogationNetwork
import numpy as np

if __name__ == "__main__":
        a = BackPropogationNetwork((2, 2,   1))
        
        inp  = np.random.normal(scale=1, size=(3, 4))
        print(inp[:-2])
        #print(inp[:, :, :])
        #     err = a.train_epoch(inp, tar)
        inp = np.array([[0, 0], [1, 1], [0, 1], [1, 0]])
        tar = np.array([[0.05], [0.05], [0.95], [0.95]])
        err = a.train_epoch(inp, tar)
        # MAX = 100000
        # MAX_ERR = 1e-5

        # for i in range(MAX - 1):
        #     err = a.train_epoch(inp, tar)
        #     if i % 5000 == 0:
        #         print(i, err)
        #     if err <= MAX_ERR:
        #         print(i, err)
        #         break
        
        # out = a.run(inp)
        # print(inp, "\n", out)   