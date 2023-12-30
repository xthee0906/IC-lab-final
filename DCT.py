import cv2
import numpy as np
import scipy.ndimage as ndimage
import os

def dct_matrix(size):
    dct_mat = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            if i == 0:
                dct_mat[i, j] = 1 / np.sqrt(size)
            else:
                dct_mat[i, j] = np.sqrt(2 / size) * np.cos((2 * j + 1) * i * np.pi / (2*size))
    return dct_mat

def DCT_matrix_ver(image, size):
    dct_image = np.zeros_like(image)
    idct_image = np.zeros_like(image)
    image_height, image_width, image_channels = image.shape
    image_YCbCr = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)    # to YCbCr
    dct_matrix_8x8 = dct_matrix(size)
    for i in range(0, image_height, size):
        for j in range(0, image_width, size):
            for ch in range(image_channels):
                block = image_YCbCr[i:i+size, j:j+size, ch]
                block = block.astype(np.float32) - 128.0
                block_dct = dct_matrix_8x8 @ block @ dct_matrix_8x8.T
                dct_image[i:i+size, j:j+size, ch] = block_dct

                # Inverse DCT with quantization
                block_idct = dct_matrix_8x8.T @ (block_dct * quantization_table) @ dct_matrix_8x8
                block_idct = block_idct.astype(np.float32) + 128.0
                idct_image[i:i+size, j:j+size, ch] = block_idct
    return dct_image, cv2.cvtColor(idct_image, cv2.COLOR_YCrCb2BGR)

def DCT_opencv_ver(image, size):
    dct_image = np.zeros_like(image)
    idct_image = np.zeros_like(image)
    image_height, image_width, image_channels = image.shape
    image_height, image_width, image_channels = image.shape
    image_YCbCr = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)    # to YCbCr
    for i in range(0, image_height, size):
        for j in range(0, image_width, size):
            for ch in range(image_channels):
                block = image_YCbCr[i:i+size, j:j+size, ch]
                block = block.astype(np.float32) - 128.0
                block_dct = cv2.dct(block)
                dct_image[i:i+size, j:j+size, ch] = block_dct

                # Inverse DCT
                block_idct = cv2.idct(block_dct*quantization_table)
                block_idct = block_idct.astype(np.float32) + 128.0
                idct_image[i:i+size, j:j+size, ch] = block_idct
    return dct_image, cv2.cvtColor(idct_image, cv2.COLOR_YCrCb2BGR)

def CheckValue(image, channel):
    image_height, image_width, _ = image.shape
    with open('pixel_values_ch' + str(channel) +'.txt', 'w') as file:
        for i in range(image_height):
            file.write('\n')
            for j in range(image_width):
                file.write(f"{str(image[i, j, channel]).rjust(3)} ")


# Load the image & image1
image = cv2.resize(cv2.imread('../data/EE4292.png'), (256,144)) # hybrid for low
image1 = cv2.resize(cv2.imread('../data/number.png'), (256,144)) # hybrid for high
print('Image size: ' + str(image.shape[1]) +'x' + str(image.shape[0]))

# adjust the quantization table, multi ver. for convenience (1 save 0 discard)
quantization_table = np.array([[1, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]])

# DCT_image hasn't quanti, but iDCT has quanti already for visualize the result.
DCT_image, iDCT_image = DCT_matrix_ver(image, 8)
DCT_image1, iDCT_image1 = DCT_matrix_ver(image1, 8)

# Display the original and processed images
low_image = iDCT_image
high_image = image - low_image
low_image1 = iDCT_image1
high_image1 = image1 - low_image1

cv2.imshow('Original Image', np.hstack((image, image1)))
cv2.imshow('DCT & DCT1', np.hstack((DCT_image, DCT_image1)))
cv2.imshow('low & low1', np.hstack((low_image, low_image1)))
cv2.imshow('high & high1', np.hstack((high_image, high_image1)))
cv2.imshow('hybrid', low_image+high_image1)
cv2.waitKey(0)
cv2.destroyAllWindows()

if not os.path.exists('result'): os.makedirs('result')
cv2.imwrite('result\Original Image.png', np.hstack((image, image1)))
cv2.imwrite('result\DCT.png', np.hstack((DCT_image, DCT_image1)))
cv2.imwrite('result\low.png', np.hstack((low_image, low_image1)))
cv2.imwrite('result\high.png', np.hstack((high_image, high_image1)))
cv2.imwrite('result\hybrid.png', low_image+high_image1)

# Open a text file for writing
# CheckValue(image, 0)