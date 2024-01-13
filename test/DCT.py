import cv2
import numpy as np
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

def dct_matrix_table(size):
    dct_mat = np.zeros((size, size))
    dct_mat = np.array([[5793, 5793, 5793, 5793, 5793, 5793, 5793, 5793],
                        [8035, 6811, 4551, 1598,-1598,-4551,-6811,-8035],
                        [7568, 3135,-3135,-7568,-7568,-3135, 3135, 7568],
                        [6811,-1598,-8035,-4551, 4551, 8035, 1598,-6811],
                        [5793,-5793,-5793, 5793, 5793,-5793,-5793, 5793],
                        [4551,-8035, 1598, 6811,-6811,-1598, 8035,-4551],
                        [3135,-7568, 7568,-3135,-3135, 7568,-7568, 3135],
                        [1598,-4551, 6811,-8035, 8035,-6811, 4551,-1598]])
    return dct_mat

def YCbCr_table(R, G, B):
    Y  = R*66  + G*129 + B*25 + 4096
    Cb = B*112 - R*38  - G*74 + 32768
    Cr = R*112 - G*94  - B*18 + 32768
    return np.round(Y/256), np.round(Cb/256), np.round(Cr/256)

def DCT_matrix_ver(image, size):
    dct_image = np.zeros_like(image).astype(int)
    idct_image = np.zeros_like(image).astype(int)
    image_height, image_width, image_channels = image.shape
    image_YCbCr = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb).astype(int)    # to YCbCr
    # CheckValue(image_YCbCr,0)
    dct_matrix_8x8 = dct_matrix(size)
    for i in range(0, image_height, size):
        for j in range(0, image_width, size):
            for ch in range(image_channels):
                block = image_YCbCr[i:i+size, j:j+size, ch]
                block = block - 128.0
                block_dct = dct_matrix_8x8 @ block @ dct_matrix_8x8.T
                dct_image[i:i+size, j:j+size, ch] = np.round(block_dct)
                # Inverse DCT with quantization
                block_idct = dct_matrix_8x8.T @ (dct_image[i:i+size, j:j+size, ch]*quantization_table) @ dct_matrix_8x8
                block_idct = block_idct + 128.0
                idct_image[i:i+size, j:j+size, ch] = block_idct.astype(int)
    CheckValue(dct_image,0)
    return dct_image.astype(np.uint8), cv2.cvtColor(idct_image.astype(np.uint8), cv2.COLOR_YCrCb2BGR)


def CheckValue(image, channel):
    image_height, image_width, _ = image.shape
    with open('pixel_values_ch' + str(channel) +'.txt', 'w') as file:
        c = 0
        b = 0
        for i in range(image_height):
            file.write('\n')

            for j in range(image_width):
                file.write(f"{str(image[i, j, channel]).rjust(3)} ")
                c = c + 1
                if (c == 8):
                    c = 0
                    file.write('||')


# Load the image & image1
image = cv2.resize(cv2.imread('../data/dog.bmp'), (256,144)) # hybrid for low
image1 = cv2.resize(cv2.imread('../data/cat.bmp'), (256,144)) # hybrid for high
print('Image size: ' + str(image.shape[1]) +'x' + str(image.shape[0]))

# adjust the quantization table, multi ver. for convenience (1 save 0 discard)
quantization_table = np.array([[0.7, 0.6, 0.5, 0, 0, 0, 0, 0],
                               [0.6, 0.5, 0, 0, 0, 0, 0, 0],
                               [0.5, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]])


# quantization_table = np.array([[17, 18, 21, 256, 256, 256, 256, 256],
#                                [18, 21, 256, 256, 256, 256, 256, 256],
#                                [21, 256, 256, 256, 256, 256, 256, 256],
#                                [256, 256, 256, 256, 256, 256, 256, 256],
#                                [256, 256, 256, 256, 256, 256, 256, 256],
#                                [256, 256, 256, 256, 256, 256, 256, 256],
#                                [256, 256, 256, 256, 256, 256, 256, 256],
#                                [256, 256, 256, 256, 256, 256, 256, 256]])

# quantization_table = np.array([
#     [16, 11, 10, 72, 72, 72, 51, 61],
#     [12, 12, 72, 72, 72, 58, 60, 55],
#     [14, 72, 72, 72, 40, 57, 69, 56],
#     [72, 72, 72, 29, 51, 87, 80, 62],
#     [72, 72, 37, 56, 68, 109, 103, 77],
#     [72, 35, 55, 64, 81, 104, 113, 92],
#     [49, 64, 78, 87, 103, 121, 120, 101],
#     [72, 92, 95, 98, 112, 100, 103, 99]
# ])

# quantization_table = 1.0/ quantization_table
# print(CheckValue(image,0))

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
cv2.imshow('jpeg', np.hstack((low_image, low_image1)))
cv2.imshow('de', 1*(np.hstack((image, image1))-np.hstack((low_image, low_image1))+np.hstack((high_image, high_image1))))
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