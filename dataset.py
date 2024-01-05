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

def get_RGB_dataset(image, mode):
    image_height, image_width, _ = image.shape
    output_file_path = 'SRAM_RGB.dat'
    with open(output_file_path, 'w') as file:
        for i in range(0, image_height, 8):
            for j in range(0, image_width, 8):
                block_B = image[i:i+8, j:j+8, 0]
                block_G = image[i:i+8, j:j+8, 1]
                block_R = image[i:i+8, j:j+8, 2]
                for row_R in block_R:
                    for value_R in row_R:
                        if (mode == 3):
                            file.write(f'{bin(value_R)[2:].zfill(8)} ')
                        elif (mode == 2):
                            file.write(f'{bin(value_R)[2:]} ')
                        elif (mode == 1):
                            file.write(f'{bin(value_R)[2:].zfill(8)}')
                        else:
                            file.write(f'{value_R} ')
                file.write('\n')
                for row_G in block_G:
                    for value_G in row_G:
                        if (mode == 3):
                            file.write(f'{bin(value_G)[2:].zfill(8)} ')
                        elif (mode == 2):
                            file.write(f'{bin(value_G)[2:]} ')
                        elif (mode == 1):
                            file.write(f'{bin(value_G)[2:].zfill(8)}')
                        else:
                            file.write(f'{value_G} ')
                file.write('\n')
                for row_B in block_B:
                    for value_B in row_B:
                        if (mode == 3):
                            file.write(f'{bin(value_B)[2:].zfill(8)} ')
                        elif (mode == 2):
                            file.write(f'{bin(value_B)[2:]} ')
                        elif (mode == 1):
                            file.write(f'{bin(value_B)[2:].zfill(8)}')
                        else:
                            file.write(f'{value_B} ')
                file.write('\n')

def get_YCbCr_datset(image, mode):
    image_height, image_width, _ = image.shape
    output_file_path = 'SRAM_YCbCr.dat'
    with open(output_file_path, 'w') as file:
        for i in range(0, image_height, 8):
            for j in range(0, image_width, 8):
                block_Y = image[i:i+8, j:j+8, 0]
                block_Cb = image[i:i+8, j:j+8, 1]
                block_Cr = image[i:i+8, j:j+8, 2]
                for row_Y in block_Y:
                    for value_Y in row_Y:
                        if (mode == 3):
                            file.write(f'{bin(value_Y)[2:].zfill(8)} ')
                        elif (mode == 2):
                            file.write(f'{bin(value_Y)[2:]} ')
                        elif (mode == 1):
                            file.write(f'{bin(value_Y)[2:].zfill(8)}')
                        else:
                            file.write(f'{value_Y} ')
                file.write('\n')
                for row_Cb in block_Cb:
                    for value_Cb in row_Cb:
                        if (mode == 3):
                            file.write(f'{bin(value_Cb)[2:].zfill(8)} ')
                        elif (mode == 2):
                            file.write(f'{bin(value_Cb)[2:]} ')
                        elif (mode == 1):
                            file.write(f'{bin(value_Cb)[2:].zfill(8)}')
                        else:
                            file.write(f'{value_Cb} ')
                file.write('\n')
                for row_Cr in block_Cr:
                    for value_Cr in row_Cr:
                        if (mode == 3):
                            file.write(f'{bin(value_Cr)[2:].zfill(8)} ')
                        elif (mode == 2):
                            file.write(f'{bin(value_Cr)[2:]} ')
                        elif (mode == 1):
                            file.write(f'{bin(value_Cr)[2:].zfill(8)}')
                        else:
                            file.write(f'{value_Cr} ')
                file.write('\n')

def get_DCT_datset(image, mode):
    image_height, image_width, _ = image.shape
    output_file_path = 'SRAM_DCT.dat'
    with open(output_file_path, 'w') as file:
        for i in range(0, image_height, 8):
            for j in range(0, image_width, 8):
                block_Y = image[i:i+8, j:j+8, 0]
                block_Cb = image[i:i+8, j:j+8, 1]
                block_Cr = image[i:i+8, j:j+8, 2]
                for row_Y in block_Y:
                    for value_Y in row_Y:
                        if (mode == 3):
                            file.write(f'{bin(value_Y & int("1"*11, 2))[2:].zfill(11)} ')
                        elif (mode == 2):
                            file.write(f'{bin(value_Y & int("1"*11, 2))[2:]} ')
                        elif (mode == 1):
                            file.write(f'{bin(value_Y & int("1"*11, 2))[2:].zfill(11)}')
                        else:
                            file.write(f'{value_Y} ')
                file.write('\n')
                for row_Cb in block_Cb:
                    for value_Cb in row_Cb:
                        if (mode == 3):
                            file.write(f'{bin(value_Cb & int("1"*11, 2))[2:].zfill(11)} ')
                        elif (mode == 2):
                            file.write(f'{bin(value_Cb & int("1"*11, 2))[2:]} ')
                        elif (mode == 1):
                            file.write(f'{bin(value_Cb & int("1"*11, 2))[2:].zfill(11)}')
                        else:
                            file.write(f'{value_Cb} ')
                file.write('\n')
                for row_Cr in block_Cr:
                    for value_Cr in row_Cr:
                        if (mode == 3):
                            file.write(f'{bin(value_Cr & int("1"*11, 2))[2:].zfill(11)} ')
                        elif (mode == 2):
                            file.write(f'{bin(value_Cr & int("1"*11, 2))[2:]} ')
                        elif (mode == 1):
                            file.write(f'{bin(value_Cr & int("1"*11, 2))[2:].zfill(11)}')
                        else:
                            file.write(f'{value_Cr} ')
                file.write('\n')

def get_RGB_golden_forcheck(image):
    B_channel_values = image[:, :, 0] # B
    G_channel_values = image[:, :, 1] # G
    R_channel_values = image[:, :, 2] # R
    output_file_path = 'R_channel_values.txt'
    with open(output_file_path, 'w') as file:
        for row in R_channel_values:
            for value in row:
                file.write(str(value) + '\n')


    output_file_path = 'G_channel_values.txt'
    with open(output_file_path, 'w') as file:
        for row in G_channel_values:
            for value in row:
                file.write(str(value) + '\n')


    output_file_path = 'B_channel_values.txt'
    with open(output_file_path, 'w') as file:
        for row in B_channel_values:
            for value in row:
                file.write(str(value) + '\n')

def get_YCbCr_golden_forcheck(image):
    Y_channel_values = image[:, :, 0] # Y
    Cb_channel_values = image[:, :, 1] # Cb
    Cr_channel_values = image[:, :, 2] # Cr
    output_file_path = 'Y_channel_values.txt'
    with open(output_file_path, 'w') as file:
        for row in Y_channel_values:
            for value in row:
                file.write(str(value) + '\n')


    output_file_path = 'Cb_channel_values.txt'
    with open(output_file_path, 'w') as file:
        for row in Cb_channel_values:
            for value in row:
                file.write(str(value) + '\n')


    output_file_path = 'Cr_channel_values.txt'
    with open(output_file_path, 'w') as file:
        for row in Cr_channel_values:
            for value in row:
                file.write(str(value) + '\n')

def get_DCT_golden_forcheck(image):
    Y_channel_values = image[:, :, 0]  # Y
    Cb_channel_values = image[:, :, 1] # Cb
    Cr_channel_values = image[:, :, 2] # Cr
    output_file_path = 'Y_channel_DCTvalues.txt'
    with open(output_file_path, 'w') as file:
        for row in Y_channel_values:
            for value in row:
                file.write(str(value) + '\n')


    output_file_path = 'Cb_channel_DCTvalues.txt'
    with open(output_file_path, 'w') as file:
        for row in Cb_channel_values:
            for value in row:
                file.write(str(value) + '\n')


    output_file_path = 'Cr_channel_DCTvalues.txt'
    with open(output_file_path, 'w') as file:
        for row in Cr_channel_values:
            for value in row:
                file.write(str(value) + '\n')

def checkvalue(file_path, addr):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        value = lines[addr]
        print(file_path +' in addr.'+ str(addr))
        print(value)



# mode = 3 # fill bit
# mode = 2 # binary
# mode = 1 # output (correct form)
# mode = 0 # deciaml
image = cv2.resize(cv2.imread('../data/cat.bmp'), (256, 144))
get_RGB_golden_forcheck(image)
get_RGB_dataset(image, mode = 1)
file_path = 'SRAM_RGB.dat'
checkvalue(file_path, addr = 0)


image_YCbCr = YCbCr_table(image)
get_YCbCr_golden_forcheck(image_YCbCr)
get_YCbCr_datset(image_YCbCr, mode = 1)
file_path = 'SRAM_YCbCr.dat'
checkvalue(file_path, addr = 0)

DCT_image = DCT_matrix_ver(image_YCbCr)
get_DCT_golden_forcheck(DCT_image)
get_DCT_datset(DCT_image, mode = 1)
file_path = 'SRAM_DCT.dat'
checkvalue(file_path, addr = 0)
