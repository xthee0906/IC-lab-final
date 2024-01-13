import numpy as np
import cv2

def CheckValue(image, channel):
    c = 0
    a = 0
    R_channel_values = image[:, :, channel] # R
    output_file_path = 'channel_values.txt'
    with open(output_file_path, 'w') as file:
        for row in R_channel_values:
            for value in row:
                c = c + 1
                file.write(str(value).rjust(4) + ' ')
                if (c == 8):
                    file.write('||')
                    c = 0
            file.write('\n')
            a = a+1
            if (a == 8):
                file.write('-'*1024)
                file.write('\n')
                a = 0

def hex_to_decimal_4bit(hex_value):
    # Check if the hex string is valid
    if not all(c in "0123456789abcdefABCDEF" for c in hex_value):
        raise ValueError("Invalid hexadecimal string")

    # Convert hex to decimal
    decimal_value = int(hex_value, 16)

    # If it's a negative number (sign bit is 1), convert from two's complement
    if decimal_value & 0b1000:
        inverted_bits = ((decimal_value ^ 0b1111) + 1) & 0b1111
        decimal_value = -inverted_bits

    return decimal_value

Q_image = np.zeros((144, 256, 3), dtype=int)
block = np.zeros((144, 256, 3), dtype=int)

with open('code_table.txt', 'r') as file:
    code = [int(line) for line in file.readlines()]
with open('len_table.txt', 'r') as file:
    len = [int(line) for line in file.readlines()]


with open('code.txt', 'r') as file:
    lines = file.readlines()
code_arrays = []
for line in lines:
    array = list(map(int, line.split()))
    code_arrays.append(array)

with open('len.txt', 'r') as file:
    lines = file.readlines()
len_arrays = []
for line in lines:
    array = list(map(int, line.split()))
    len_arrays.append(array)

# for array in arrays:
#     print(array)


# decode AC
for m in range(576):
    # 8 for code number
    # print('block'+str(m))
    straight = []
    for k in range(8):
        code_len = len_arrays[m][k]
        code_out = code_arrays[m][k]
        # number of table is 128
        for i in range(128):
            for j in range(128):
                if (code[i] == code_out and len[j] == code_len and i == j):
                    R = i//16
                    L = hex(i%16)[2:]
                    # print('(' + str(R)+','+ str(L) + ')', end=' ')
        if (R == 0 and L == 0): straight.append(0)
        if (R == 0 and L != 0): straight.append(hex_to_decimal_4bit(L))
        if (R == 1 and L != 0): 
            straight.append(0)
            straight.append(hex_to_decimal_4bit(L))
        if (R == 2 and L != 0):
            straight.extend([0, 0])
            straight.append(hex_to_decimal_4bit(L))
        if (R == 3 and L != 0):
            straight.extend([0, 0, 0])
            straight.append(hex_to_decimal_4bit(L))
        if (R == 4 and L != 0):
            straight.extend([0, 0, 0, 0])
            straight.append(hex_to_decimal_4bit(L))
        if (R == 5 and L != 0):
            straight.extend([0, 0, 0, 0, 0])
            straight.append(hex_to_decimal_4bit(L))
        if (R == 6 and L != 0):
            straight.extend([0, 0, 0, 0, 0, 0])
            straight.append(hex_to_decimal_4bit(L))
        if (R == 7 and L != 0):
            straight.extend([0, 0, 0, 0, 0, 0, 0])
            straight.append(hex_to_decimal_4bit(L))
    # print(straight)
    block[8*(m//32)  , (m*8)%256+1] = straight[0]
    block[8*(m//32)+1, (m*8)%256] = straight[1]
    block[8*(m//32)+2, (m*8)%256] = straight[2]
    block[8*(m//32)+1, (m*8)%256+1] = straight[3]
    block[8*(m//32), (m*8)%256+2] = straight[4]
    block[8*(m//32), (m*8)%256+3] = straight[5]
    block[8*(m//32)+1, (m*8)%256+2] = straight[6]
    block[8*(m//32)+2, (m*8)%256+1] = straight[7]

    # print(block[8*(m//32):8*(m//32)+8, (m*8)%256:(m*8)%256+8, 0])
    # print('\n')

CheckValue(block,0)


# for i in range(0, 144, 8):
#     for j in range(0, 256, 8):
#         print(j, end=' ')
        # print(Q_image[i][j][0])
# for k in range(576):
#     print((k*8)%256, end=' ')
#     print(8*(k//32), end='')

# # 印出影像陣列的維度
# cv2.imshow('ss', image.astype(np.uint8))
# cv2.waitKey(0)
# cv2.destroyAllWindows()
