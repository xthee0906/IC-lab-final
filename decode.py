import numpy as np
import cv2

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

def iDCT(block):
    dct_matrix_8x8 = dct_matrix()
    block_dct_1 = block @ dct_matrix_8x8
    block_dct_rounded_1 = np.floor(block_dct_1/16384 + 0.5)
    block_dct_2 = dct_matrix_8x8.T @ block_dct_rounded_1
    block_dct_rounded_2 = np.floor(block_dct_2/16384 + 0.5)
    block_dct_rounded_2 = block_dct_rounded_2 + 128

    return block_dct_rounded_2

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


###### decode ########
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



def read_file(code_table_path, length_table_path, code_path, length_path, DC_code_path, DC_length_path):

    # read Y code and length table
    with open(code_table_path, 'r') as file:
        code = [int(line) for line in file.readlines()]
    with open(length_table_path, 'r') as file:
        len = [int(line) for line in file.readlines()]

    # read Y code value
    with open(code_path, 'r') as file:
        lines = file.readlines()
    code_arrays = []
    for line in lines:
        array = list(map(int, line.split()))
        code_arrays.append(array)

    with open(length_path, 'r') as file:
        lines = file.readlines()
    len_arrays = []
    for line in lines:
        array = list(map(int, line.split()))
        len_arrays.append(array)

    ############## DC decode ###########
    
    with open(DC_length_path, 'r') as file:
        DC_len_array = [int(line) for line in file.readlines()]

    with open(DC_code_path, 'r') as file:
        DC_code_array = []
        c = 0
        for line in file.readlines():
            DC_code_array.append(line[-2:-(DC_len_array[c]+2):-1][::-1])
            c = c +1
    return code, len, code_arrays, len_arrays, DC_code_array


def DC_decoder(DC_code_array):
    DC_decimal = []
    for nn in range(576):
        if (DC_code_array[nn][0:2] == '00'): DC_decimal.append(0)
        elif (DC_code_array[nn][0:3] == '010'):
            if (DC_code_array[nn][3] == '1'): DC_decimal.append(1)
            else: DC_decimal.append(-1)
        elif (DC_code_array[nn][0:3] == '011'):
            if   (DC_code_array[nn][3:5] == '00'): DC_decimal.append(-3)
            elif (DC_code_array[nn][3:5] == '01'): DC_decimal.append(-2)
            elif (DC_code_array[nn][3:5] == '10'): DC_decimal.append(2)
            elif (DC_code_array[nn][3:5] == '11'): DC_decimal.append(3)
        elif (DC_code_array[nn][0:3] == '100'):
            if   (DC_code_array[nn][3:6] == '000'): DC_decimal.append(-7)
            elif (DC_code_array[nn][3:6] == '001'): DC_decimal.append(-6)
            elif (DC_code_array[nn][3:6] == '010'): DC_decimal.append(-5)
            elif (DC_code_array[nn][3:6] == '011'): DC_decimal.append(-4)
            elif (DC_code_array[nn][3:6] == '100'): DC_decimal.append(4)
            elif (DC_code_array[nn][3:6] == '101'): DC_decimal.append(5)
            elif (DC_code_array[nn][3:6] == '110'): DC_decimal.append(6)
            elif (DC_code_array[nn][3:6] == '111'): DC_decimal.append(7)
        elif (DC_code_array[nn][0:3] == '101'):
            if   (DC_code_array[nn][3:7] == '0000'): DC_decimal.append(-15)
            elif (DC_code_array[nn][3:7] == '0001'): DC_decimal.append(-14)
            elif (DC_code_array[nn][3:7] == '0010'): DC_decimal.append(-13)
            elif (DC_code_array[nn][3:7] == '0011'): DC_decimal.append(-12)
            elif (DC_code_array[nn][3:7] == '0100'): DC_decimal.append(-11)
            elif (DC_code_array[nn][3:7] == '0101'): DC_decimal.append(-10)
            elif (DC_code_array[nn][3:7] == '0110'): DC_decimal.append(-9)
            elif (DC_code_array[nn][3:7] == '0111'): DC_decimal.append(-8)
            elif (DC_code_array[nn][3:7] == '1000'): DC_decimal.append(8)
            elif (DC_code_array[nn][3:7] == '1001'): DC_decimal.append(9)
            elif (DC_code_array[nn][3:7] == '1010'): DC_decimal.append(10)
            elif (DC_code_array[nn][3:7] == '1011'): DC_decimal.append(11)
            elif (DC_code_array[nn][3:7] == '1100'): DC_decimal.append(12)
            elif (DC_code_array[nn][3:7] == '1101'): DC_decimal.append(13)
            elif (DC_code_array[nn][3:7] == '1110'): DC_decimal.append(14)
            elif (DC_code_array[nn][3:7] == '1111'): DC_decimal.append(15)
        elif (DC_code_array[nn][0:3] == '110'):
            if   (DC_code_array[nn][3:8] == '00000'): DC_decimal.append(-31)
            elif (DC_code_array[nn][3:8] == '00001'): DC_decimal.append(-30)
            elif (DC_code_array[nn][3:8] == '00010'): DC_decimal.append(-29)
            elif (DC_code_array[nn][3:8] == '00011'): DC_decimal.append(-28)
            elif (DC_code_array[nn][3:8] == '00100'): DC_decimal.append(-27)
            elif (DC_code_array[nn][3:8] == '00101'): DC_decimal.append(-26)
            elif (DC_code_array[nn][3:8] == '00110'): DC_decimal.append(-25)
            elif (DC_code_array[nn][3:8] == '00111'): DC_decimal.append(-24)
            elif (DC_code_array[nn][3:8] == '01000'): DC_decimal.append(-23)
            elif (DC_code_array[nn][3:8] == '01001'): DC_decimal.append(-22)
            elif (DC_code_array[nn][3:8] == '01010'): DC_decimal.append(-21)
            elif (DC_code_array[nn][3:8] == '01011'): DC_decimal.append(-20)
            elif (DC_code_array[nn][3:8] == '01100'): DC_decimal.append(-19)
            elif (DC_code_array[nn][3:8] == '01101'): DC_decimal.append(-18)
            elif (DC_code_array[nn][3:8] == '01110'): DC_decimal.append(-17)
            elif (DC_code_array[nn][3:8] == '01111'): DC_decimal.append(-16)
            elif (DC_code_array[nn][3:8] == '10000'): DC_decimal.append(16)
            elif (DC_code_array[nn][3:8] == '10001'): DC_decimal.append(17)
            elif (DC_code_array[nn][3:8] == '10010'): DC_decimal.append(18)
            elif (DC_code_array[nn][3:8] == '10011'): DC_decimal.append(19)
            elif (DC_code_array[nn][3:8] == '10100'): DC_decimal.append(20)
            elif (DC_code_array[nn][3:8] == '10101'): DC_decimal.append(21)
            elif (DC_code_array[nn][3:8] == '10110'): DC_decimal.append(22)
            elif (DC_code_array[nn][3:8] == '10111'): DC_decimal.append(23)
            elif (DC_code_array[nn][3:8] == '11000'): DC_decimal.append(24)
            elif (DC_code_array[nn][3:8] == '11001'): DC_decimal.append(25)
            elif (DC_code_array[nn][3:8] == '11010'): DC_decimal.append(26)
            elif (DC_code_array[nn][3:8] == '11011'): DC_decimal.append(27)
            elif (DC_code_array[nn][3:8] == '11100'): DC_decimal.append(28)
            elif (DC_code_array[nn][3:8] == '11101'): DC_decimal.append(29)
            elif (DC_code_array[nn][3:8] == '11110'): DC_decimal.append(30)
            elif (DC_code_array[nn][3:8] == '11111'): DC_decimal.append(31)
        elif (DC_code_array[nn][0:4] == '1110'):
            if   (DC_code_array[nn][4:10] == '000000'): DC_decimal.append(-63)
            elif (DC_code_array[nn][4:10] == '000001'): DC_decimal.append(-62)
            elif (DC_code_array[nn][4:10] == '000010'): DC_decimal.append(-61)
            elif (DC_code_array[nn][4:10] == '000011'): DC_decimal.append(-60)
            elif (DC_code_array[nn][4:10] == '000100'): DC_decimal.append(-59)
            elif (DC_code_array[nn][4:10] == '000101'): DC_decimal.append(-58)
            elif (DC_code_array[nn][4:10] == '000110'): DC_decimal.append(-57)
            elif (DC_code_array[nn][4:10] == '000111'): DC_decimal.append(-56)
            elif (DC_code_array[nn][4:10] == '001000'): DC_decimal.append(-55)
            elif (DC_code_array[nn][4:10] == '001001'): DC_decimal.append(-54)
            elif (DC_code_array[nn][4:10] == '001010'): DC_decimal.append(-53)
            elif (DC_code_array[nn][4:10] == '001011'): DC_decimal.append(-52)
            elif (DC_code_array[nn][4:10] == '001100'): DC_decimal.append(-51)
            elif (DC_code_array[nn][4:10] == '001101'): DC_decimal.append(-50)
            elif (DC_code_array[nn][4:10] == '001110'): DC_decimal.append(-49)
            elif (DC_code_array[nn][4:10] == '001111'): DC_decimal.append(-48)
            elif (DC_code_array[nn][4:10] == '010000'): DC_decimal.append(-47)
            elif (DC_code_array[nn][4:10] == '010001'): DC_decimal.append(-46)
            elif (DC_code_array[nn][4:10] == '010010'): DC_decimal.append(-45)
            elif (DC_code_array[nn][4:10] == '010011'): DC_decimal.append(-44)
            elif (DC_code_array[nn][4:10] == '010100'): DC_decimal.append(-43)
            elif (DC_code_array[nn][4:10] == '010101'): DC_decimal.append(-42)
            elif (DC_code_array[nn][4:10] == '010110'): DC_decimal.append(-41)
            elif (DC_code_array[nn][4:10] == '010111'): DC_decimal.append(-40)
            elif (DC_code_array[nn][4:10] == '011000'): DC_decimal.append(-39)
            elif (DC_code_array[nn][4:10] == '011001'): DC_decimal.append(-38)
            elif (DC_code_array[nn][4:10] == '011010'): DC_decimal.append(-37)
            elif (DC_code_array[nn][4:10] == '011011'): DC_decimal.append(-36)
            elif (DC_code_array[nn][4:10] == '011100'): DC_decimal.append(-35)
            elif (DC_code_array[nn][4:10] == '011101'): DC_decimal.append(-34)
            elif (DC_code_array[nn][4:10] == '011110'): DC_decimal.append(-33)
            elif (DC_code_array[nn][4:10] == '011111'): DC_decimal.append(-32)
            elif (DC_code_array[nn][4:10] == '100000'): DC_decimal.append(32)
            elif (DC_code_array[nn][4:10] == '100001'): DC_decimal.append(33)
            elif (DC_code_array[nn][4:10] == '100010'): DC_decimal.append(34)
            elif (DC_code_array[nn][4:10] == '100011'): DC_decimal.append(35)
            elif (DC_code_array[nn][4:10] == '100100'): DC_decimal.append(36)
            elif (DC_code_array[nn][4:10] == '100101'): DC_decimal.append(37)
            elif (DC_code_array[nn][4:10] == '100110'): DC_decimal.append(38)
            elif (DC_code_array[nn][4:10] == '100111'): DC_decimal.append(39)
            elif (DC_code_array[nn][4:10] == '101000'): DC_decimal.append(40)
            elif (DC_code_array[nn][4:10] == '101001'): DC_decimal.append(41)
            elif (DC_code_array[nn][4:10] == '101010'): DC_decimal.append(42)
            elif (DC_code_array[nn][4:10] == '101011'): DC_decimal.append(43)
            elif (DC_code_array[nn][4:10] == '101100'): DC_decimal.append(44)
            elif (DC_code_array[nn][4:10] == '101101'): DC_decimal.append(45)
            elif (DC_code_array[nn][4:10] == '101110'): DC_decimal.append(46)
            elif (DC_code_array[nn][4:10] == '101111'): DC_decimal.append(47)
            elif (DC_code_array[nn][4:10] == '110000'): DC_decimal.append(48)
            elif (DC_code_array[nn][4:10] == '110001'): DC_decimal.append(49)
            elif (DC_code_array[nn][4:10] == '110010'): DC_decimal.append(50)
            elif (DC_code_array[nn][4:10] == '110011'): DC_decimal.append(51)
            elif (DC_code_array[nn][4:10] == '110100'): DC_decimal.append(52)
            elif (DC_code_array[nn][4:10] == '110101'): DC_decimal.append(53)
            elif (DC_code_array[nn][4:10] == '110110'): DC_decimal.append(54)
            elif (DC_code_array[nn][4:10] == '110111'): DC_decimal.append(55)
            elif (DC_code_array[nn][4:10] == '111000'): DC_decimal.append(56)
            elif (DC_code_array[nn][4:10] == '111001'): DC_decimal.append(57)
            elif (DC_code_array[nn][4:10] == '111010'): DC_decimal.append(58)
            elif (DC_code_array[nn][4:10] == '111011'): DC_decimal.append(59)
            elif (DC_code_array[nn][4:10] == '111100'): DC_decimal.append(60)
            elif (DC_code_array[nn][4:10] == '111101'): DC_decimal.append(61)
            elif (DC_code_array[nn][4:10] == '111110'): DC_decimal.append(62)
            elif (DC_code_array[nn][4:10] == '111111'): DC_decimal.append(63)
    # print(DC_decimal)
    return DC_decimal

def AC_decoder(code_table, len_table, code_arrays, len_arrays, DC_decimal):
    block = np.zeros((144, 256, 3), dtype=int)
    for m in range(576):
        # 8 for code number
        straight = []
        for k in range(8):
            code_len = len_arrays[m][k]
            code_out = code_arrays[m][k]
            # number of table is 128
            for i in range(128):
                for j in range(128):
                    if (code_table[i] == code_out and len_table[j] == code_len and i == j):
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
        block[8*(m//32)  , (m*8)%256] = DC_decimal[m]
        block[8*(m//32)  , (m*8)%256+1] = straight[0]
        block[8*(m//32)+1, (m*8)%256] = straight[1]
        block[8*(m//32)+2, (m*8)%256] = straight[2]
        block[8*(m//32)+1, (m*8)%256+1] = straight[3]
        block[8*(m//32), (m*8)%256+2] = straight[4]
        block[8*(m//32), (m*8)%256+3] = straight[5]
        block[8*(m//32)+1, (m*8)%256+2] = straight[6]
        block[8*(m//32)+2, (m*8)%256+1] = straight[7]
    return block

code_Y_table, len_Y_table, code_Y_arrays, len_Y_arrays, DC_code_Y_array = read_file(code_table_path = './dataset/code_table.txt', 
                                                                        length_table_path = './dataset/len_table.txt', 
                                                                        code_path = './dataset/code.txt', 
                                                                        length_path = './dataset/len.txt', 
                                                                        DC_code_path = './dataset/code_DC.txt' , 
                                                                        DC_length_path = './dataset/len_DC.txt')    


DC_decimal_Y = DC_decoder(DC_code_Y_array)
Q_image_Y = AC_decoder(code_Y_table, len_Y_table, code_Y_arrays, len_Y_arrays, DC_decimal_Y)


########## vis ###########
CheckValue(Q_image_Y,0)
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


iDCT_image = iDCT_matrix_ver(Q_image_Y)
iDCT_image = cv2.cvtColor(iDCT_image, cv2.COLOR_YCrCb2BGR)    # to YCbCr

cv2.imshow('iDCT', iDCT_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
