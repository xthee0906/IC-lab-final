import cv2
import numpy as np
import scipy.ndimage as ndimage
import os

def dct_matrix():
    dct_mat = np.zeros((8, 8))
    dct_mat = np.array([[5793, 5793, 5793, 5793, 5793, 5793, 5793, 5793],
                        [8035, 6811, 4551, 1598,-1598,-4551,-6811,-8035],
                        [7568, 3135,-3135,-7568,-7568,-3135, 3135, 7568],
                        [6811,-1598,-8035,-4551, 4551, 8035, 1598,-6811],
                        [5793,-5793,-5793, 5793, 5793,-5793,-5793, 5793],
                        [4551,-8035, 1598, 6811,-6811,-1598, 8035,-4551],
                        [3135,-7568, 7568,-3135,-3135, 7568,-7568, 3135],
                        [1598,-4551, 6811,-8035, 8035,-6811, 4551,-1598]])
    return dct_mat

# YCbCr
def YCbCr_table(image):
    image_YCbCr = np.zeros_like(image).astype(int)
    R = image[:,:,2].astype(int)
    G = image[:,:,1].astype(int)
    B = image[:,:,0].astype(int)
    
    Y  = R*66  + G*129 + B*25 + 4096
    Cb = B*112 - R*38  - G*74 + 32768
    Cr = R*112 - G*94  - B*18 + 32768
    
    image_YCbCr[:,:,0] = np.floor(Y/256 + 0.5)
    image_YCbCr[:,:,2] = np.floor(Cb/256 + 0.5)
    image_YCbCr[:,:,1] = np.floor(Cr/256 + 0.5)

    return image_YCbCr.astype(np.uint8)

def DCT(block):
    dct_matrix_8x8 = dct_matrix()
    block = block - 128
    block_dct_1 = block @ dct_matrix_8x8.T
    block_dct_rounded_1 = np.floor(block_dct_1/16384 + 0.5)
    block_dct_2 = dct_matrix_8x8 @ block_dct_rounded_1
    block_dct_rounded_2 = np.floor(block_dct_2/16384 + 0.5)

    return block_dct_rounded_2

def iDCT(block):
    dct_matrix_8x8 = dct_matrix()
    block_dct_1 = block @ dct_matrix_8x8
    block_dct_rounded_1 = np.floor(block_dct_1/16384 + 0.5)
    block_dct_2 = dct_matrix_8x8.T @ block_dct_rounded_1
    block_dct_rounded_2 = np.floor(block_dct_2/16384 + 0.5)
    block_dct_rounded_2 = block_dct_rounded_2 + 128

    return block_dct_rounded_2

def DCT_matrix_ver(image_YCbCr):
    image_height, image_width, image_channels = image_YCbCr.shape
    dct_image = np.zeros_like(image_YCbCr).astype(int)
    
    for i in range(0, image_height, 8):
        for j in range(0, image_width, 8):
            for ch in range(image_channels):
                block = image_YCbCr[i:i+8, j:j+8, ch].astype(int)
                dct_image[i:i+8, j:j+8, ch] = np.floor(DCT(block) / Q + 0.5)
 
    return dct_image

def iDCT_matrix_ver(image_DCT):
    image_height, image_width, image_channels = image_DCT.shape
    idct_image = np.zeros_like(image_DCT).astype(int)
    
    for i in range(0, image_height, 8):
        for j in range(0, image_width, 8):
            for ch in range(image_channels):
                block = image_DCT[i:i+8, j:j+8, ch].astype(int)
                block = block * Q
                idct_image[i:i+8, j:j+8, ch] = iDCT(block)
            
    return idct_image.astype(np.uint8)


# iDCT for high image Q/2
def iDCT_matrix_hver(image_DCT):
    image_height, image_width, image_channels = image_DCT.shape
    idct_image = np.zeros_like(image_DCT).astype(int)
    
    for i in range(0, image_height, 8):
        for j in range(0, image_width, 8):
            for ch in range(image_channels):
                block = image_DCT[i:i+8, j:j+8, ch].astype(int)
                block = block * Q
                idct_image[i:i+8, j:j+8, ch] = iDCT(block)
            
    return idct_image.astype(np.uint8)

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

def hybrid(image, image1):
    image_high = np.zeros_like(image).astype(int)
    image_YCbCr = YCbCr_table(image)
    iDCT_image = iDCT_matrix_hver(DCT_matrix_ver(image_YCbCr))
    iDCT_image = cv2.cvtColor(iDCT_image, cv2.COLOR_YCrCb2BGR)
    image_high = image.astype(int) - iDCT_image.astype(int)
    cv2.imshow('high', image_high.astype(np.uint8))
    # image_high = image_high.clip(0, 255).astype(np.uint8)
    # cv2.imshow('high', image_high)

    image_low = np.zeros_like(image1).astype(int)
    image_YCbCr = YCbCr_table(image1)
    iDCT_image = iDCT_matrix_ver(DCT_matrix_ver(image_YCbCr))
    iDCT_image = cv2.cvtColor(iDCT_image, cv2.COLOR_YCrCb2BGR)
    image_low = iDCT_image.astype(int)

    return (image_high.astype(int) + image_low.astype(int)).clip(0, 255).astype(np.uint8)

def quantization_table(AC, step):
    Q = np.zeros((8, 8))
    if (AC == 0):
        for i in range(8):
            for j in range(8):
                if (i + j < step-2): Q[i][j] = 16
                elif (i + j < step-1): Q[i][j] = 32
                elif (i + j < step): Q[i][j] = 64
                else: Q[i][j] = 512
    else:
        for i in range(8):
            for j in range(8):
                if (i + j < step): Q[i][j] = 2000
                else: Q[i][j] = 1
    return Q


# Load the image & image1
image = cv2.resize(cv2.imread('../data/dog.bmp'), (256,144)) # hybrid for low
image1 = cv2.resize(cv2.imread('../data/cat.bmp'), (256,144)) # hybrid for high

# Q = quantization_table(0, 3)
# print(Q)

# Q = np.array([
#     [  16,  64,  64, 64, 512, 512, 512, 512],
#     [ 32,  64, 64, 512, 512, 512, 512, 512],
#     [ 64,  512, 512, 512, 512, 512, 512, 512],
#     [512, 512, 512, 512, 512, 512, 512, 512],
#     [512, 512, 512, 512, 512, 512, 512, 512],
#     [512, 512, 512, 512, 512, 512, 512, 512],
#     [512, 512, 512, 512, 512, 512, 512, 512],
#     [512, 512, 512, 512, 512, 512, 512, 512]
# ])

Q = np.array([
    [  16,  64,  512, 512, 512, 512, 512, 512],
    [ 64,  512, 512, 512, 512, 512, 512, 512],
    [ 512,  512, 512, 512, 512, 512, 512, 512],
    [512, 512, 512, 512, 512, 512, 512, 512],
    [512, 512, 512, 512, 512, 512, 512, 512],
    [512, 512, 512, 512, 512, 512, 512, 512],
    [512, 512, 512, 512, 512, 512, 512, 512],
    [512, 512, 512, 512, 512, 512, 512, 512]
])

# image_YCbCr = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)    # to YCbCr
image_YCbCr = YCbCr_table(image)
DCT_image = DCT_matrix_ver(image_YCbCr) #int
iDCT_image = iDCT_matrix_ver(DCT_image)
iDCT_image = cv2.cvtColor(iDCT_image, cv2.COLOR_YCrCb2BGR)    # to YCbCr

cv2.imshow('DCT', DCT_image.astype(np.uint8))
cv2.imshow('iDCT', iDCT_image)
cv2.imshow('hybird', hybrid(image1,image))
cv2.waitKey(0)
cv2.destroyAllWindows()
