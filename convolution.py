import numpy as np
def convolution(img, kernel):
    img_height = img.shape[0]
    img_width = img.shape[1]

    kernel_height = kernel.shape[0]
    kernel_width = kernel.shape[1]

    H = (kernel_height - 1) // 2
    W = (kernel_width - 1) // 2

    out = np.zeros((img_height, img_width))

    for i in np.arange(H, img_height - H):
        for j in np.arange(W, img_width - W):
            out[i - H, j - W] = np.tensordot(img[i - H:i + H + 1, j - W:j + W + 1], kernel, axes=((0, 1), (0, 1)))
    return out


def ReLU(img):
    img[img < 0] = 0
    img[img > 255] = 255
    return img