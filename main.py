import numpy as np
import pooling
import convolution as cnn

in_img = np.array([[1, 0, 0, 1, 0],
                   [0, 1, 1, 0, 1],
                   [1, 0, 1, 0, 1],
                   [1, 0, 0, 1, 1],
                   [0, 1, 1, 0, 1]
                   ])

kernel = np.array([[1, 0, 0],
                   [0, 1, 1],
                   [1, 0, 1]])


out_img = cnn.convolution(in_img, kernel)
pool_img = pooling.pool(out_img)
with np.printoptions(suppress=True):
    print(out_img)
    print()
    print(pool_img)
    