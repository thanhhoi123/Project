import numpy as np
def pool(img, w=2, h=2): #w, h là bước xải ~ stride
    img_height = img.shape[0]
    img_width = img.shape[1]
    new_height = int(img_height / h)
    new_width = int(img_width / w)
    out = np.zeros((new_height, new_width))

    for i in np.arange(0, new_height):
        for j in np.arange(0, new_width):
            top = i * h # nhân bước stride hàng
            left = j * w # nhân bước stride cột
            out[i, j] = np.max(img[top:top + h, left: left + w])

    return out