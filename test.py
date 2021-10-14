import cv2
import numpy as array

image = cv2.imread('honda.jpg',0)
small = cv2.resize(image,(50,50),fx=0.1,fy=0.1)
# show image on window
gray_image = cv2.imshow('graycsale image',image)
cv2.imshow('graycsale image',small)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(image)

# f1 = open("matran.txt", "w") 
# img_H = image.shape[0]
# img_W = image.shape[1]
# for i in range(0, img_H):
#     for j in range(0, img_W):        
#         f1.write(str(image[i][j]))
#         f1.write('\t')
#     f1.writelines('')

# f1.close()



