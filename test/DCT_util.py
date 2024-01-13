import cv2
import numpy as np

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
    
    image_YCbCr[:,:,0] = np.round(Y/256)
    image_YCbCr[:,:,1] = np.round(Cb/256)
    image_YCbCr[:,:,2] = np.round(Cr/256)

    return image_YCbCr.astype(np.uint8)

def DCT(block):
    dct_matrix_8x8 = dct_matrix()
    block = block - 128
    block_dct_1 = block @ dct_matrix_8x8.T
    block_dct_rounded_1 = np.round(block_dct_1/16384)
    block_dct_2 = dct_matrix_8x8 @ block_dct_rounded_1
    block_dct_rounded_2 = np.round(block_dct_2/16384)

    return block_dct_rounded_2


def DCT_matrix_ver(image_YCbCr):
    image_height, image_width, image_channels = image_YCbCr.shape
    dct_image = np.zeros_like(image_YCbCr).astype(int)
    
    for i in range(0, image_height, 8):
        for j in range(0, image_width, 8):
            for ch in range(image_channels):
                block = image_YCbCr[i:i+8, j:j+8, ch].astype(int)
                dct_image[i:i+8, j:j+8, ch] = np.round(DCT(block))

    return dct_image






