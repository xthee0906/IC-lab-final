import cv2
import numpy as np

def get_dataset(image, mode):
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

def checkvalue(file_path, addr):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        value = lines[addr]
        print('Your 512 bits addr.' + str(addr) + ' value')
        print(value)

image = cv2.resize(cv2.imread('../data/cat.bmp'), (256, 144))




# mode = 3 # 8 bit (fill zero)
# mode = 2 # binary
# mode = 1 # output (correct form)
# mode = 0 # deciaml
get_dataset(image, mode = 1)

get_RGB_golden_forcheck(image)

file_path = 'SRAM_RGB.dat'
checkvalue(file_path, addr = 0)




