# from PIL import Image

# with open('pixel_values_ch0.txt', 'r') as file:
#     pixel_values = [int(value) for value in file.read().split()]

# # print(pixel_values)

# width = 256
# height = len(pixel_values) // width

# image = Image.new('L', (width, height))
# image.putdata(pixel_values)

# image.show()

# for i in range(8):
#     print('\n')
#     for j in range(8):
#         print('q' + str(i+1) + str(j+1), end=' ')


# for i in range(8):
#     for j in range(8):
#         print('.Q'+str(i + 1)+str(j + 1)+'('+ 'Q'+str(i + 1)+str(j + 1)+'),')

# c = 0
# for i in range(8):
#     for j in range(8):
#         print('Z'+str(i + 1)+str(j + 1)+' = dct[' +str(c)+ '];')
#         c = c+1

# for i in range(8):
#     for j in range(8):
#         print('$display(\"pattern %0d\", $signed(q'+str(i + 1)+str(j + 1)+'));')


# import numpy as np

# matrix = np.array([[66, 73, 82, 89, 98, 118, 127, 130],
#                    [99, 87, 83, 79, 77, 80, 86, 108],
#                    [79, 80, 85, 92, 94, 76, 66, 71],
#                    [87, 89, 87, 77, 77, 80, 79, 84],
#                    [88, 82, 79, 72, 69, 69, 70, 63],
#                    [107, 116, 105, 90, 81, 71, 70, 72],
#                    [97, 94, 105, 114, 112, 100, 89, 77],
#                    [109, 112, 112, 111, 111, 109, 108, 103]])


# print(np.sum(matrix))

# for i in range(8):
#     for j in range(8):
#         print('assign QM'+str(i + 1)+'_'+str(j + 1)+' = 4096/Q'+str(i + 1)+'_'+str(j + 1)+';')

# for i in range(8):
#     for j in range(8):
#         print('q'+str(i + 1)+str(j + 1)+ ' <= '+'q'+str(i + 1)+str(j + 1)+'_temp[11] ? ' + 'q'+str(i + 1)+str(j + 1)+'_temp[22:12] + 1 : ' + 'q'+str(i + 1)+str(j + 1)+'_temp[22:12];')

        # q11 <= dct11_temp_1[11] ? dct11_temp_1[22:12] + 1 : dct11_temp_1[22:12]; 

# for i in range(8):
#     print('\nreg [22:0]', end='')
#     for j in range(8):
#         print('q'+str(i + 1)+str(j + 1)+'_temp;', end = '')

# c = 0
# order = [11, 
#          12, 21, 
#          31, 22, 13, 
#          14, 23, 32, 41, 
#          51, 42, 33, 24, 15, 
#          16, 25, 34, 43, 52, 61,
#          71, 62, 53, 44, 35, 26, 17,
#          18, 27, 36, 45, 54, 63, 72, 81,
#          82, 73, 64, 55, 46, 37, 28,
#          38, 47, 56, 65, 74, 83,
#          84, 75, 66, 57, 48,
#          58, 67, 76, 85,
#          86, 77, 68,
#          87, 78,
#          88]
# for i in range(8):
#     for j in range(8):
#         print('zig_zag['+str(c)+']'+' = q' + str(order[c])+';')
#         c = c + 1


import numpy as np
quantization_table = np.array([
    [  16,  32,  64, 64, 512, 512, 512, 512],
    [ 32,  64, 64, 512, 512, 512, 512, 512],
    [ 64,  512, 512, 512, 512, 512, 512, 512],
    [512, 512, 512, 512, 512, 512, 512, 512],
    [512, 512, 512, 512, 512, 512, 512, 512],
    [512, 512, 512, 512, 512, 512, 512, 512],
    [512, 512, 512, 512, 512, 512, 512, 512],
    [512, 512, 512, 512, 512, 512, 512, 512]
])

quantization_table_2 = np.array([
    [  16,  32,  64, 128, 512, 512, 512, 512],
    [ 32,  64, 512, 512, 512, 512, 512, 512],
    [ 64,  512, 512, 512, 512, 512, 512, 512],
    [512, 512, 512, 512, 512, 512, 512, 512],
    [512, 512, 512, 512, 16, 512, 512, 512],
    [512, 512, 512, 512, 512, 512, 512, 512],
    [512, 512, 512, 512, 512, 512, 512, 512],
    [512, 512, 512, 512, 512, 512, 512, 512]
])
c = 0
for i in range(8):
    for j in range(8):
        print('assign q'+str(i+1)+'_'+str(j+1)+' = mode_reg ? '+str(quantization_table[i][j])+': ' + str(quantization_table_2[i][j])+';')

# for i in range(15):
# 	print('R['+ str(4*i+3) + ':' + str(4*i) +'] = WW['+ str(i+1) +'] == 200 ? 0 : WW[' + str(i+1) + '] - WW[' + str(i) + '] - 1;')
# 	print('L['+ str(4*i+3) + ':' + str(4*i) +'] = WW['+ str(i+1) +'] == 200 ? 0 : zig_zag[WW[' + str(i+1) + ']];')
# 	print('')


# for i in range(8):
#     for j in range(8):
#         print('.dct'+str(i+1)+str(j+1)+'(' + 'dct_input['+ str(i*8+j)+']),')
# seq = []
# o = [11, 12, 21, 31, 22, 13, 14, 23, 32, 41, 51, 42, 33, 24, 15, 16, 25, 34, 43, 52, 61, 71, 62, 53, 44, 35, 26, 17, 18, 27, 36, 45, 54, 63, 72, 81, 82, 73, 64, 55, 46, 37, 28, 38, 47, 56, 65, 74, 83, 84, 75, 66, 57, 48, 58, 67, 76, 85, 86, 77, 68, 87, 78, 88];
# for i in range(64):
#     seq.append(o[i]%10 - 1)

# print(seq)
        
x = [0, 0, 1, 2, 1, 0, 0, 1, 2, 3, 4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 3, 4, 5, 6, 7, 7, 6, 5, 7, 6, 7]
y = [0, 1, 0, 0, 1, 2, 3, 2, 1, 0, 0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 3, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 5, 6, 7, 6, 7, 7]

