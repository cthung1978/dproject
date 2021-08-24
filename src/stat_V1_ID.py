# -- coding:big5--
import numpy as np

def jump_collection (data, jump=1, col=4, num=1):
    count = np.zeros(50, dtype='i8')

    # �@�C�@�C
    for index in range(jump, np.size(data, 0)) :
        if data[index-jump][col] == num:

            #print data[index]   ## U1D1.2.3..�v���C�X�F�����B���X�C
            count[data[index][4]] = count[data[index][4]] + 1
            count[data[index][5]] = count[data[index][5]] + 1
            count[data[index][6]] = count[data[index][6]] + 1
            count[data[index][7]] = count[data[index][7]] + 1
            count[data[index][8]] = count[data[index][8]] + 1
            count[data[index][9]] = count[data[index][9]] + 1
    return count

### �v�����
def weighting_function(jump, weight, data):
    countdata = np.zeros(2 * 50, dtype='i8')
    countdata = countdata.reshape(2, 50)
    for U in range(jump):
        for num in range(1, 50):
            for r in range(1, 50):
                if data[U][r-1] == num:
                    countdata[1][num] = countdata[1][num] + weight[r];
    countdata[0] = np.argsort(-countdata[1])
    return countdata

# hcy1--------------------------------------------------
data = np.loadtxt('CT_002.txt', dtype='i8')
# �C�L  jump = 1300  ��� ( ���} print D1_2_3_4[U] )
order_outputfile = open('V1_01_order_output.txt', mode='w')
static_outputfile = open('V1_01_static_output.txt', mode='w')

# �A2 �Ϭq�ܼ�
# �ܼƳ]�w�b�o�̡F��J "���� div = /�Bdiv1 = * " " �W�� = 0 ���C�p��"�C
# 2
div_L4549 = 1
div1_L4549 = 1
# 4
div_L4849 = 0
div1_L4849 = 0
# 6
div_L4749 = 0
div1_L4749 = 0
#-------------
# 1
div_R0105 = 1
div1_R0105 = 1
# 3
div_R0102 = 0
div1_R0102 = 0
# 5
div_R0103 = 0
div1_R0103 = 0

# �ɮ׬O�_��� (��J " = 1 �C�L " " = 0 ���C�L ")
flag_dist_L4549 = 1
flag_dist_L4849 = 0
flag_dist_L4749 = 0
#-------------------
flag_dist_R0105 = 1
flag_dist_R0102 = 0
flag_dist_R0103 = 0

#-------------------------------------------------------
# numpy �� size ��� �d�߸�ƪ��� 0 ��ܦC
# print np.size(data, 0)
# numpy �� size ��� �d�߸�ƪ��� 1 �����
# print np.size(data, 1)
# numpy �� size ��� �d�߸���`�Ӽ�
# print np.size(data)

a = jump_collection (data, 1, 6, 20)
#print a

#U = 1
#D = 1

# �̫�@����� index = np.size(data, 0) - 1
# "�ù�" ��X���ơB����B�y�X
watch = data[np.size(data, 0)-1]
print watch

# hcy1 -------------------------------------------
# �n�����C�� jump ---- ( ��J�G50 ~ 1500 )

jump = 100
#-------------------------------------------------
rawdata = np.zeros(jump * 7 * 2 * 50, dtype='i8')
rawdata = rawdata.reshape(jump, 7, 2, 50)
for U in range (1, jump+1):
    # �C�X�`����---------------------------------
    #print U
    watch = data[np.size(data, 0)-U]
    #print watch
    for D in range (4, 11):
        a = jump_collection (data, U, D, watch[D])
        dumy = a + 1
        dumy[0] = 0

        # print ("U=", U, "D=", D-3, a)
        #print ("U=", U, "D=", D-3, a)
        sortdata = np.argsort(-dumy)

        #print ("Sort U=", U, "D=", D, sortdata)
        #print ("Sort U=", U, "D=", D-3, sortdata)

        outstring = str(U) + '\t' + str(D-3) + '\t'
        rawdata[U-1][D-4][0] = sortdata
        rawdata[U-1][D-4][1] = a

        for i in range(np.size(sortdata)):
            outstring = outstring + str(sortdata[i]) + '\t'
        outstring = outstring + '\n'
        order_outputfile.write(outstring)
order_outputfile.close()

for U in range (1, jump+1):
    # �C�X�`����---------------------------------
    #print U
    for D in range (4, 11):
        outstring = str(U) + '\t' + str(D-3) + '\t'
        for i in range(np.size(rawdata[U-1][D-4][1])):
            outstring = outstring + str(rawdata[U-1][D-4][1][i]) + '\t'
        outstring = outstring + '\n'
        static_outputfile.write(outstring)
static_outputfile.close()

## UxDy ��Ƥw�g��X���ɮ� �O���馳�@�� rawdata[U][D][?] �ѫ���p��
## rawdata[0][0][0][0] ��� U1D1 �}�����X�Ĥ@�W
## rawdata[0][0][1][0] ��� U1D1 �}�����X�X�{����

## �� �}�l  ### �s�� "�C��" �����զX (�|�X�@���B�@ 35 ��) #####################################################################
## 01  �w�q�ɮ׬y���� �b �A1 �}�l
D1_2_3_4 = np.zeros(jump * 50, dtype='i8')
D1_2_3_4 = D1_2_3_4.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        # ---------------------- [1] ------------------- [2] ------------------- [3] ------------------- [4] -- (�ж��ƥش� 1 )
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][1][1][col] + rawdata[U][2][1][col] + rawdata[U][3][1][col]
    D1_2_3_4[U] = np.argsort(-tmpdata)
    # �C�L D1�B2 �B.... 6�B7 �C�@ 1300 �C�C ��X�ɦW�GV1_01_order_output -------------
    #print D1_2_3_4[U]

## 02
D1_2_3_5 = np.zeros(jump * 50, dtype='i8')
D1_2_3_5 = D1_2_3_5.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        # ---------------------- [1] ------------------- [2] ------------------- [3] ------------------- [5] -- (�ж��ƥش� 1 )
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][1][1][col] + rawdata[U][2][1][col] + rawdata[U][4][1][col]
    D1_2_3_5[U] = np.argsort(-tmpdata)
    #print D1_2_3_5[U]

## 03
D1_2_3_6 = np.zeros(jump * 50, dtype='i8')
D1_2_3_6 = D1_2_3_6.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       2                       3                       6
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][1][1][col] + rawdata[U][2][1][col] + rawdata[U][5][1][col]
    D1_2_3_6[U] = np.argsort(-tmpdata)
    #print D1_2_3_6[U]

## 04
D1_2_3_7 = np.zeros(jump * 50, dtype='i8')
D1_2_3_7 = D1_2_3_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       2                       3                       7
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][1][1][col] + rawdata[U][2][1][col] + rawdata[U][6][1][col]
    D1_2_3_7[U] = np.argsort(-tmpdata)
    #print D1_2_3_7[U]

## 05
D1_2_4_5 = np.zeros(jump * 50, dtype='i8')
D1_2_4_5 = D1_2_4_5.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       2                       4                       5
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][1][1][col] + rawdata[U][3][1][col] + rawdata[U][4][1][col]
    D1_2_4_5[U] = np.argsort(-tmpdata)
    #print D1_2_4_5[U]

## 06
D1_2_4_6 = np.zeros(jump * 50, dtype='i8')
D1_2_4_6 = D1_2_4_6.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       2                       4                       6
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][1][1][col] + rawdata[U][3][1][col] + rawdata[U][5][1][col]
    D1_2_4_6[U] = np.argsort(-tmpdata)
    #print D1_2_4_6[U]

## 07
D1_2_4_7 = np.zeros(jump * 50, dtype='i8')
D1_2_4_7 = D1_2_4_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       2                       4                       7
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][1][1][col] + rawdata[U][3][1][col] + rawdata[U][6][1][col]
    D1_2_4_7[U] = np.argsort(-tmpdata)
    #print D1_2_4_7[U]

## 08
D1_2_5_6 = np.zeros(jump * 50, dtype='i8')
D1_2_5_6 = D1_2_5_6.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       2                       5                       6
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][1][1][col] + rawdata[U][4][1][col] + rawdata[U][5][1][col]
    D1_2_5_6[U] = np.argsort(-tmpdata)
    #print D1_2_5_6[U]

## 09
D1_2_5_7 = np.zeros(jump * 50, dtype='i8')
D1_2_5_7 = D1_2_5_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       2                       5                       7
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][1][1][col] + rawdata[U][4][1][col] + rawdata[U][6][1][col]
    D1_2_5_7[U] = np.argsort(-tmpdata)
    #print D1_2_5_7[U]

## 10
D1_2_6_7 = np.zeros(jump * 50, dtype='i8')
D1_2_6_7 = D1_2_6_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       2                       6                       7
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][1][1][col] + rawdata[U][5][1][col] + rawdata[U][6][1][col]
    D1_2_6_7[U] = np.argsort(-tmpdata)
    #print D1_2_6_7[U]

## 11
D1_3_4_5 = np.zeros(jump * 50, dtype='i8')
D1_3_4_5 = D1_3_4_5.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       3                       4                       5
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][2][1][col] + rawdata[U][3][1][col] + rawdata[U][4][1][col]
    D1_3_4_5[U] = np.argsort(-tmpdata)
    #print D1_3_4_5[U]

## 12
D1_3_4_6 = np.zeros(jump * 50, dtype='i8')
D1_3_4_6 = D1_3_4_6.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       3                       4                       6
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][2][1][col] + rawdata[U][3][1][col] + rawdata[U][5][1][col]
    D1_3_4_6[U] = np.argsort(-tmpdata)
    #print D1_3_4_6[U]

## 13
D1_3_4_7 = np.zeros(jump * 50, dtype='i8')
D1_3_4_7 = D1_3_4_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       3                       4                       7
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][2][1][col] + rawdata[U][3][1][col] + rawdata[U][6][1][col]
    D1_3_4_7[U] = np.argsort(-tmpdata)
    #print D1_3_4_7[U]

## 14
D1_3_5_6 = np.zeros(jump * 50, dtype='i8')
D1_3_5_6 = D1_3_5_6.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       3                       5                       6
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][2][1][col] + rawdata[U][4][1][col] + rawdata[U][5][1][col]
    D1_3_5_6[U] = np.argsort(-tmpdata)
    #print D1_3_5_6[U]

## 15
D1_3_5_7 = np.zeros(jump * 50, dtype='i8')
D1_3_5_7 = D1_3_5_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       3                       5                       7
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][2][1][col] + rawdata[U][4][1][col] + rawdata[U][6][1][col]
    D1_3_5_7[U] = np.argsort(-tmpdata)
    #print D1_3_5_7[U]

## 16
D1_3_6_7 = np.zeros(jump * 50, dtype='i8')
D1_3_6_7 = D1_3_6_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       3                       6                       7
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][2][1][col] + rawdata[U][5][1][col] + rawdata[U][6][1][col]
    D1_3_6_7[U] = np.argsort(-tmpdata)
    #print D1_3_6_7[U]

## 17
D1_4_5_6 = np.zeros(jump * 50, dtype='i8')
D1_4_5_6 = D1_4_5_6.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       4                       5                       6
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][3][1][col] + rawdata[U][4][1][col] + rawdata[U][5][1][col]
    D1_4_5_6[U] = np.argsort(-tmpdata)
    #print D1_4_5_6[U]

## 18
D1_4_5_7 = np.zeros(jump * 50, dtype='i8')
D1_4_5_7 = D1_4_5_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       4                       5                       7
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][3][1][col] + rawdata[U][4][1][col] + rawdata[U][6][1][col]
    D1_4_5_7[U] = np.argsort(-tmpdata)
    #print 18_D1_4_5_7[U]

## 19
D1_4_6_7 = np.zeros(jump * 50, dtype='i8')
D1_4_6_7 = D1_4_6_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       4                       6                       7
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][3][1][col] + rawdata[U][5][1][col] + rawdata[U][6][1][col]
    D1_4_6_7[U] = np.argsort(-tmpdata)
    #print D1_4_6_7[U]

## 20
D1_5_6_7 = np.zeros(jump * 50, dtype='i8')
D1_5_6_7 = D1_5_6_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         1                       5                       6                       7
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][4][1][col] + rawdata[U][5][1][col] + rawdata[U][6][1][col]
    D1_5_6_7[U] = np.argsort(-tmpdata)
    #print D1_5_6_7[U]

## 21
D2_3_4_5 = np.zeros(jump * 50, dtype='i8')
D2_3_4_5 = D2_3_4_5.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         2                       3                       4                       5
        tmpdata[col] = rawdata[U][1][1][col] + rawdata[U][2][1][col] + rawdata[U][3][1][col] + rawdata[U][4][1][col]
    D2_3_4_5[U] = np.argsort(-tmpdata)
    #print D2_3_4_5[U]

## 22
D2_3_4_6 = np.zeros(jump * 50, dtype='i8')
D2_3_4_6 = D2_3_4_6.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         2                       3                       4                       6
        tmpdata[col] = rawdata[U][1][1][col] + rawdata[U][2][1][col] + rawdata[U][3][1][col] + rawdata[U][5][1][col]
    D2_3_4_6[U] = np.argsort(-tmpdata)
    #print D2_3_4_6[U]

## 23
D2_3_4_7 = np.zeros(jump * 50, dtype='i8')
D2_3_4_7 = D2_3_4_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         2                       3                       4                       7
        tmpdata[col] = rawdata[U][1][1][col] + rawdata[U][2][1][col] + rawdata[U][3][1][col] + rawdata[U][6][1][col]
    D2_3_4_7[U] = np.argsort(-tmpdata)
    #print D2_3_4_7[U]

## 24
D2_3_5_6 = np.zeros(jump * 50, dtype='i8')
D2_3_5_6 = D2_3_5_6.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         2                       3                       5                       6
        tmpdata[col] = rawdata[U][1][1][col] + rawdata[U][2][1][col] + rawdata[U][4][1][col] + rawdata[U][5][1][col]
    D2_3_5_6[U] = np.argsort(-tmpdata)
    #print D2_3_5_6[U]

## 25
D2_3_5_7 = np.zeros(jump * 50, dtype='i8')
D2_3_5_7 = D2_3_5_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         2                       3                       5                       7
        tmpdata[col] = rawdata[U][1][1][col] + rawdata[U][2][1][col] + rawdata[U][4][1][col] + rawdata[U][6][1][col]
    D2_3_5_7[U] = np.argsort(-tmpdata)
    #print D2_3_5_7[U]

## 26
D2_3_6_7 = np.zeros(jump * 50, dtype='i8')
D2_3_6_7 = D2_3_6_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         2                       3                       6                       7
        tmpdata[col] = rawdata[U][1][1][col] + rawdata[U][2][1][col] + rawdata[U][5][1][col] + rawdata[U][6][1][col]
    D2_3_6_7[U] = np.argsort(-tmpdata)
    #print D2_3_6_7[U]

## 27
D2_4_5_6 = np.zeros(jump * 50, dtype='i8')
D2_4_5_6 = D2_4_5_6.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         2                       4                       5                       6
        tmpdata[col] = rawdata[U][1][1][col] + rawdata[U][3][1][col] + rawdata[U][4][1][col] + rawdata[U][5][1][col]
    D2_4_5_6[U] = np.argsort(-tmpdata)
    #print D2_4_5_6[U]

## 28
D2_4_5_7 = np.zeros(jump * 50, dtype='i8')
D2_4_5_7 = D2_4_5_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         2                       4                       5                       7
        tmpdata[col] = rawdata[U][1][1][col] + rawdata[U][3][1][col] + rawdata[U][4][1][col] + rawdata[U][6][1][col]
    D2_4_5_7[U] = np.argsort(-tmpdata)
    #print D2_4_5_7[U]

## 29
D2_4_6_7 = np.zeros(jump * 50, dtype='i8')
D2_4_6_7 = D2_4_6_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         2                       4                       6                       7
        tmpdata[col] = rawdata[U][1][1][col] + rawdata[U][3][1][col] + rawdata[U][5][1][col] + rawdata[U][6][1][col]
    D2_4_6_7[U] = np.argsort(-tmpdata)
    #print D2_4_6_7[U]

## 30
D2_5_6_7 = np.zeros(jump * 50, dtype='i8')
D2_5_6_7 = D2_5_6_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         2                       5                       6                       7
        tmpdata[col] = rawdata[U][1][1][col] + rawdata[U][4][1][col] + rawdata[U][5][1][col] + rawdata[U][6][1][col]
    D2_5_6_7[U] = np.argsort(-tmpdata)
    #print D2_5_6_7[U]

## 31
D3_4_5_6 = np.zeros(jump * 50, dtype='i8')
D3_4_5_6 = D3_4_5_6.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         3                       4                       5                       6
        tmpdata[col] = rawdata[U][2][1][col] + rawdata[U][3][1][col] + rawdata[U][4][1][col] + rawdata[U][5][1][col]
    D3_4_5_6[U] = np.argsort(-tmpdata)
    #print D3_4_5_6[U]

## 32
D3_4_5_7 = np.zeros(jump * 50, dtype='i8')
D3_4_5_7 = D3_4_5_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         3                       4                       5                       7
        tmpdata[col] = rawdata[U][2][1][col] + rawdata[U][3][1][col] + rawdata[U][4][1][col] + rawdata[U][6][1][col]
    D3_4_5_7[U] = np.argsort(-tmpdata)
    #print D3_4_5_7[U]

## 33
D3_4_6_7 = np.zeros(jump * 50, dtype='i8')
D3_4_6_7 = D3_4_6_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         3                       4                       6                       7
        tmpdata[col] = rawdata[U][2][1][col] + rawdata[U][3][1][col] + rawdata[U][5][1][col] + rawdata[U][6][1][col]
    D3_4_6_7[U] = np.argsort(-tmpdata)
    #print D3_4_6_7[U]

## 34
D3_5_6_7 = np.zeros(jump * 50, dtype='i8')
D3_5_6_7 = D3_5_6_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         3                       5                       6                       7
        tmpdata[col] = rawdata[U][2][1][col] + rawdata[U][4][1][col] + rawdata[U][5][1][col] + rawdata[U][6][1][col]
    D3_5_6_7[U] = np.argsort(-tmpdata)
    #print D3_5_6_7[U]

## 35
D4_5_6_7 = np.zeros(jump * 50, dtype='i8')
D4_5_6_7 = D4_5_6_7.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        #                         4                       5                       6                       7
        tmpdata[col] = rawdata[U][3][1][col] + rawdata[U][4][1][col] + rawdata[U][5][1][col] + rawdata[U][6][1][col]
    D4_5_6_7[U] = np.argsort(-tmpdata)
    #print D4_5_6_7[U]

## D1234567
D1234567 = np.zeros(jump * 50, dtype='i8')
D1234567 = D1234567.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        #print  rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col], rawdata[U][4][1][col], rawdata[U][5][1][col], rawdata[U][6][1][col]
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][1][1][col] + rawdata[U][2][1][col] + rawdata[U][3][1][col] + rawdata[U][4][1][col] + rawdata[U][5][1][col] + rawdata[U][6][1][col]
    D1234567[U] = np.argsort(-tmpdata)

## �� ���� ####################################################################################################################################################

## �A1 �}�l  ##########################################################################################################################################
# ���N�ܼƨ��N�᭱�Ҧ���  weighting_functio(jump, countColRange, target_Dw_x_y_z)
#target_Dw_x_y_z = D1_2_3_4
target_Dw_x_y_z = D1234567

# �H�U�w�q�ɮ׬y����
targer_w = 1
targer_x = 2
targer_y = 3
targer_z = 4

## �W�] ID �ק�
#- countdata = np.zeros(49 * 2 * 50)         ## �� ID 48
#- countdata = countdata.reshape(49, 2, 50)  ## �� ID 48
countdata = np.zeros(51 * 2 * 50)
countdata = countdata.reshape(51, 2, 50)

# �w�q�ĴX�� =======================================================
# �A1 �ϲĤ@�� [�q 0 �}�l�� 48 (�p 49 ��)]
# 01
ID = 0
# �w�q��� countColRange ���w�n�έp�����C
#- countColRange = np.zeros(50, dtype='i8')  ## �� ID 48  "����"
countColRange = np.zeros(50, dtype='i8')
# �s�� [��� (���X)] = �ƶq
countColRange[1] = 1
countColRange[2] = 1
countColRange[3] = 1
countColRange[4] = 1

countColRange[10] = 1
countColRange[11] = 1
countColRange[12] = 1
countColRange[13] = 1

countColRange[20] = 1
countColRange[21] = 1
countColRange[22] = 1
countColRange[23] = 1

countColRange[30] = 1
countColRange[31] = 1
countColRange[32] = 1
countColRange[33] = 1

countColRange[40] = 1
countColRange[41] = 1
countColRange[42] = 1
countColRange[43] = 1
#--------------------------------------------- target_Dw_x_y_z
res = weighting_function(jump, countColRange,  target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �o�@�q�O "�ù�" ��X �A�� �Ĥ@�ժ� ���X�B��ơC
# ���t �A2 DIST_V1_01_R_0101_factor = 0 (1�B2�B3....�ܤƭ�)�C
# print countdata[ID][0]
# print countdata[ID][1]

# �w�q�ĴX�� =======================================================
# 02
ID = 1
# �w�q��� countColRange ���w�n�έp����� ==========================
countColRange = np.zeros(50, dtype='i8')
# �s�� -- [���] = �ƶq
countColRange[2] = 1
countColRange[3] = 1
countColRange[4] = 1
countColRange[5] = 1

countColRange[11] = 1
countColRange[12] = 1
countColRange[13] = 1
countColRange[14] = 1

countColRange[21] = 1
countColRange[22] = 1
countColRange[23] = 1
countColRange[24] = 1

countColRange[31] = 1
countColRange[32] = 1
countColRange[33] = 1
countColRange[34] = 1

countColRange[41] = 1
countColRange[42] = 1
countColRange[43] = 1
countColRange[44] = 1

res = weighting_function(jump, countColRange,  target_Dw_x_y_z )
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

#print countdata[ID][0]
#print countdata[ID][1]


# �w�q�ĴX�� =======================================================
# 03
ID = 2
# �w�q��� countColRange ���w�n�έp����� ==========================
countColRange = np.zeros(50, dtype='i8')
countColRange[3] = 1
countColRange[4] = 1
countColRange[5] = 1
countColRange[6] = 1

countColRange[12] = 1
countColRange[13] = 1
countColRange[14] = 1
countColRange[15] = 1

countColRange[22] = 1
countColRange[23] = 1
countColRange[24] = 1
countColRange[25] = 1

countColRange[32] = 1
countColRange[33] = 1
countColRange[34] = 1
countColRange[35] = 1

countColRange[42] = 1
countColRange[43] = 1
countColRange[44] = 1
countColRange[45] = 1

res = weighting_function(jump, countColRange,  target_Dw_x_y_z )
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� =======================================================
# 04
ID = 3
# �w�q��� countColRange ���w�n�έp����� ==========================
countColRange = np.zeros(50, dtype='i8')
countColRange[4] = 1
countColRange[5] = 1
countColRange[6] = 1
countColRange[7] = 1

countColRange[13] = 1
countColRange[14] = 1
countColRange[15] = 1
countColRange[16] = 1

countColRange[23] = 1
countColRange[24] = 1
countColRange[25] = 1
countColRange[26] = 1

countColRange[33] = 1
countColRange[34] = 1
countColRange[35] = 1
countColRange[36] = 1

countColRange[43] = 1
countColRange[44] = 1
countColRange[45] = 1
countColRange[46] = 1

res = weighting_function(jump, countColRange,  target_Dw_x_y_z )
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� =======================================================
# 05
ID = 4
# �w�q��� countColRange ���w�n�έp����� ==========================
countColRange = np.zeros(50, dtype='i8')
countColRange[5] = 1
countColRange[6] = 1
countColRange[7] = 1
countColRange[8] = 1

countColRange[14] = 1
countColRange[15] = 1
countColRange[16] = 1
countColRange[17] = 1

countColRange[24] = 1
countColRange[25] = 1
countColRange[26] = 1
countColRange[27] = 1

countColRange[34] = 1
countColRange[35] = 1
countColRange[36] = 1
countColRange[37] = 1

countColRange[44] = 1
countColRange[45] = 1
countColRange[46] = 1
countColRange[47] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z )
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� =========================================================
# 06
ID = 5
# �w�q��� countColRange ���w�n�έp����� ============================
countColRange = np.zeros(50, dtype='i8')
countColRange[6] = 1
countColRange[7] = 1
countColRange[8] = 1
countColRange[9] = 1

countColRange[15] = 1
countColRange[16] = 1
countColRange[17] = 1
countColRange[18] = 1

countColRange[25] = 1
countColRange[26] = 1
countColRange[27] = 1
countColRange[28] = 1

countColRange[35] = 1
countColRange[36] = 1
countColRange[37] = 1
countColRange[38] = 1

countColRange[45] = 1
countColRange[46] = 1
countColRange[47] = 1
countColRange[48] = 1

res = weighting_function(jump, countColRange,  target_Dw_x_y_z  )
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� =======================================================
# 07
ID = 6
# �w�q��� countColRange ���w�n�έp����� ==========================
countColRange = np.zeros(50, dtype='i8')
countColRange[7] = 1
countColRange[8] = 1
countColRange[9] = 1
countColRange[10] = 1

countColRange[16] = 1
countColRange[17] = 1
countColRange[18] = 1
countColRange[19] = 1

countColRange[26] = 1
countColRange[27] = 1
countColRange[28] = 1
countColRange[29] = 1

countColRange[36] = 1
countColRange[37] = 1
countColRange[38] = 1
countColRange[39] = 1

countColRange[46] = 1
countColRange[47] = 1
countColRange[48] = 1
countColRange[49] = 1

res = weighting_function(jump, countColRange,  target_Dw_x_y_z )
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 08
ID = 7
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[8] = 1
countColRange[9] = 1
countColRange[10] = 1
countColRange[11] = 1

countColRange[17] = 1
countColRange[18] = 1
countColRange[19] = 1
countColRange[20] = 1

countColRange[27] = 1
countColRange[28] = 1
countColRange[29] = 1
countColRange[30] = 1

countColRange[37] = 1
countColRange[38] = 1
countColRange[39] = 1
countColRange[40] = 1

countColRange[47] = 1
countColRange[48] = 1
countColRange[49] = 1
countColRange[1] = 1

res = weighting_function(jump, countColRange,  target_Dw_x_y_z )
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 09
ID = 8
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[9] = 1
countColRange[10] = 1
countColRange[11] = 1
countColRange[12] = 1

countColRange[18] = 1
countColRange[19] = 1
countColRange[20] = 1
countColRange[21] = 1

countColRange[28] = 1
countColRange[29] = 1
countColRange[30] = 1
countColRange[31] = 1

countColRange[38] = 1
countColRange[39] = 1
countColRange[40] = 1
countColRange[41] = 1

countColRange[48] = 1
countColRange[49] = 1
countColRange[1] = 1
countColRange[2] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z )
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 10
ID = 9
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[10] = 1
countColRange[11] = 1
countColRange[12] = 1
countColRange[13] = 1

countColRange[19] = 1
countColRange[20] = 1
countColRange[21] = 1
countColRange[22] = 1

countColRange[29] = 1
countColRange[30] = 1
countColRange[31] = 1
countColRange[32] = 1

countColRange[39] = 1
countColRange[40] = 1
countColRange[41] = 1
countColRange[42] = 1

countColRange[49] = 1
countColRange[1] = 1
countColRange[2] = 1
countColRange[3] = 1

res = weighting_function(jump, countColRange,  target_Dw_x_y_z )
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 11
ID = 10
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[11] = 1
countColRange[12] = 1
countColRange[13] = 1
countColRange[14] = 1

countColRange[20] = 1
countColRange[21] = 1
countColRange[22] = 1
countColRange[23] = 1

countColRange[30] = 1
countColRange[31] = 1
countColRange[32] = 1
countColRange[33] = 1

countColRange[40] = 1
countColRange[41] = 1
countColRange[42] = 1
countColRange[43] = 1

countColRange[1] = 1
countColRange[2] = 1
countColRange[3] = 1
countColRange[4] = 1

res = weighting_function(jump, countColRange,  target_Dw_x_y_z  )
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 12
ID = 11
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[12] = 1
countColRange[13] = 1
countColRange[14] = 1
countColRange[15] = 1

countColRange[21] = 1
countColRange[22] = 1
countColRange[23] = 1
countColRange[24] = 1

countColRange[31] = 1
countColRange[32] = 1
countColRange[33] = 1
countColRange[34] = 1

countColRange[41] = 1
countColRange[42] = 1
countColRange[43] = 1
countColRange[44] = 1

countColRange[2] = 1
countColRange[3] = 1
countColRange[4] = 1
countColRange[5] = 1

res = weighting_function(jump, countColRange,  target_Dw_x_y_z )
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 13
ID = 12
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[13] = 1
countColRange[14] = 1
countColRange[15] = 1
countColRange[16] = 1

countColRange[22] = 1
countColRange[23] = 1
countColRange[24] = 1
countColRange[25] = 1

countColRange[32] = 1
countColRange[33] = 1
countColRange[34] = 1
countColRange[35] = 1

countColRange[42] = 1
countColRange[43] = 1
countColRange[44] = 1
countColRange[45] = 1

countColRange[3] = 1
countColRange[4] = 1
countColRange[5] = 1
countColRange[6] = 1

res = weighting_function(jump, countColRange,  target_Dw_x_y_z   )
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 14
ID = 13
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[14] = 1
countColRange[15] = 1
countColRange[16] = 1
countColRange[17] = 1

countColRange[23] = 1
countColRange[24] = 1
countColRange[25] = 1
countColRange[26] = 1

countColRange[33] = 1
countColRange[34] = 1
countColRange[35] = 1
countColRange[36] = 1

countColRange[43] = 1
countColRange[44] = 1
countColRange[45] = 1
countColRange[46] = 1

countColRange[4] = 1
countColRange[5] = 1
countColRange[6] = 1
countColRange[7] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z  )
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 15
ID = 14
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[15] = 1
countColRange[16] = 1
countColRange[17] = 1
countColRange[18] = 1

countColRange[24] = 1
countColRange[25] = 1
countColRange[26] = 1
countColRange[27] = 1

countColRange[34] = 1
countColRange[35] = 1
countColRange[36] = 1
countColRange[37] = 1

countColRange[44] = 1
countColRange[45] = 1
countColRange[46] = 1
countColRange[47] = 1

countColRange[5] = 1
countColRange[6] = 1
countColRange[7] = 1
countColRange[8] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z  )
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 16
ID = 15
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[16] = 1
countColRange[17] = 1
countColRange[18] = 1
countColRange[19] = 1

countColRange[25] = 1
countColRange[26] = 1
countColRange[27] = 1
countColRange[28] = 1

countColRange[35] = 1
countColRange[36] = 1
countColRange[37] = 1
countColRange[38] = 1

countColRange[45] = 1
countColRange[46] = 1
countColRange[47] = 1
countColRange[48] = 1

countColRange[6] = 1
countColRange[7] = 1
countColRange[8] = 1
countColRange[9] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 17
ID = 16
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[17] = 1
countColRange[18] = 1
countColRange[19] = 1
countColRange[20] = 1

countColRange[26] = 1
countColRange[27] = 1
countColRange[28] = 1
countColRange[29] = 1

countColRange[36] = 1
countColRange[37] = 1
countColRange[38] = 1
countColRange[39] = 1

countColRange[46] = 1
countColRange[47] = 1
countColRange[48] = 1
countColRange[49] = 1

countColRange[7] = 1
countColRange[8] = 1
countColRange[9] = 1
countColRange[10] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 18
ID = 17
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[18] = 1
countColRange[19] = 1
countColRange[20] = 1
countColRange[21] = 1

countColRange[27] = 1
countColRange[28] = 1
countColRange[29] = 1
countColRange[30] = 1

countColRange[37] = 1
countColRange[38] = 1
countColRange[39] = 1
countColRange[40] = 1

countColRange[47] = 1
countColRange[48] = 1
countColRange[49] = 1
countColRange[1] = 1

countColRange[8] = 1
countColRange[9] = 1
countColRange[10] = 1
countColRange[11] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 19
ID = 18
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[19] = 1
countColRange[20] = 1
countColRange[21] = 1
countColRange[22] = 1

countColRange[28] = 1
countColRange[29] = 1
countColRange[30] = 1
countColRange[31] = 1

countColRange[38] = 1
countColRange[39] = 1
countColRange[40] = 1
countColRange[41] = 1

countColRange[48] = 1
countColRange[49] = 1
countColRange[1] = 1
countColRange[2] = 1

countColRange[9] = 1
countColRange[10] = 1
countColRange[11] = 1
countColRange[12] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 20
ID = 19
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[20] = 1
countColRange[21] = 1
countColRange[22] = 1
countColRange[23] = 1

countColRange[29] = 1
countColRange[30] = 1
countColRange[31] = 1
countColRange[32] = 1

countColRange[39] = 1
countColRange[40] = 1
countColRange[41] = 1
countColRange[42] = 1

countColRange[49] = 1
countColRange[1] = 1
countColRange[2] = 1
countColRange[3] = 1

countColRange[10] = 1
countColRange[11] = 1
countColRange[12] = 1
countColRange[13] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 21
ID = 20
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[21] = 1
countColRange[22] = 1
countColRange[23] = 1
countColRange[24] = 1

countColRange[30] = 1
countColRange[31] = 1
countColRange[32] = 1
countColRange[33] = 1

countColRange[40] = 1
countColRange[41] = 1
countColRange[42] = 1
countColRange[43] = 1

countColRange[1] = 1
countColRange[2] = 1
countColRange[3] = 1
countColRange[4] = 1

countColRange[11] = 1
countColRange[12] = 1
countColRange[13] = 1
countColRange[14] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 22
ID = 21
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[22] = 1
countColRange[23] = 1
countColRange[24] = 1
countColRange[25] = 1

countColRange[31] = 1
countColRange[32] = 1
countColRange[33] = 1
countColRange[34] = 1

countColRange[41] = 1
countColRange[42] = 1
countColRange[43] = 1
countColRange[44] = 1

countColRange[2] = 1
countColRange[3] = 1
countColRange[4] = 1
countColRange[5] = 1

countColRange[12] = 1
countColRange[13] = 1
countColRange[14] = 1
countColRange[15] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 23
ID = 22
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[23] = 1
countColRange[24] = 1
countColRange[25] = 1
countColRange[26] = 1

countColRange[32] = 1
countColRange[33] = 1
countColRange[34] = 1
countColRange[35] = 1

countColRange[42] = 1
countColRange[43] = 1
countColRange[44] = 1
countColRange[45] = 1

countColRange[3] = 1
countColRange[4] = 1
countColRange[5] = 1
countColRange[6] = 1

countColRange[13] = 1
countColRange[14] = 1
countColRange[15] = 1
countColRange[16] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 24
ID = 23
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[24] = 1
countColRange[25] = 1
countColRange[26] = 1
countColRange[27] = 1

countColRange[33] = 1
countColRange[34] = 1
countColRange[35] = 1
countColRange[36] = 1

countColRange[43] = 1
countColRange[44] = 1
countColRange[45] = 1
countColRange[46] = 1

countColRange[4] = 1
countColRange[5] = 1
countColRange[6] = 1
countColRange[7] = 1

countColRange[14] = 1
countColRange[15] = 1
countColRange[16] = 1
countColRange[17] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 25
ID = 24
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[25] = 1
countColRange[26] = 1
countColRange[27] = 1
countColRange[28] = 1

countColRange[34] = 1
countColRange[35] = 1
countColRange[36] = 1
countColRange[37] = 1

countColRange[44] = 1
countColRange[45] = 1
countColRange[46] = 1
countColRange[47] = 1

countColRange[5] = 1
countColRange[6] = 1
countColRange[7] = 1
countColRange[8] = 1

countColRange[15] = 1
countColRange[16] = 1
countColRange[17] = 1
countColRange[18] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 26
ID = 25
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[26] = 1
countColRange[27] = 1
countColRange[28] = 1
countColRange[29] = 1

countColRange[35] = 1
countColRange[36] = 1
countColRange[37] = 1
countColRange[38] = 1

countColRange[45] = 1
countColRange[46] = 1
countColRange[47] = 1
countColRange[48] = 1

countColRange[6] = 1
countColRange[7] = 1
countColRange[8] = 1
countColRange[9] = 1

countColRange[16] = 1
countColRange[17] = 1
countColRange[18] = 1
countColRange[19] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 27
ID = 26
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[27] = 1
countColRange[28] = 1
countColRange[29] = 1
countColRange[30] = 1

countColRange[36] = 1
countColRange[37] = 1
countColRange[38] = 1
countColRange[39] = 1

countColRange[46] = 1
countColRange[47] = 1
countColRange[48] = 1
countColRange[49] = 1

countColRange[7] = 1
countColRange[8] = 1
countColRange[9] = 1
countColRange[10] = 1

countColRange[17] = 1
countColRange[18] = 1
countColRange[19] = 1
countColRange[20] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 28
ID = 27
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[28] = 1
countColRange[29] = 1
countColRange[30] = 1
countColRange[31] = 1

countColRange[37] = 1
countColRange[38] = 1
countColRange[39] = 1
countColRange[40] = 1

countColRange[47] = 1
countColRange[48] = 1
countColRange[49] = 1
countColRange[1] = 1

countColRange[8] = 1
countColRange[9] = 1
countColRange[10] = 1
countColRange[11] = 1

countColRange[18] = 1
countColRange[19] = 1
countColRange[20] = 1
countColRange[21] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 29
ID = 28
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[29] = 1
countColRange[30] = 1
countColRange[31] = 1
countColRange[32] = 1

countColRange[38] = 1
countColRange[39] = 1
countColRange[40] = 1
countColRange[41] = 1

countColRange[48] = 1
countColRange[49] = 1
countColRange[1] = 1
countColRange[2] = 1

countColRange[9] = 1
countColRange[10] = 1
countColRange[11] = 1
countColRange[12] = 1

countColRange[19] = 1
countColRange[20] = 1
countColRange[21] = 1
countColRange[22] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 30
ID = 29
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[30] = 1
countColRange[31] = 1
countColRange[32] = 1
countColRange[33] = 1

countColRange[39] = 1
countColRange[40] = 1
countColRange[41] = 1
countColRange[42] = 1

countColRange[49] = 1
countColRange[1] = 1
countColRange[2] = 1
countColRange[3] = 1

countColRange[10] = 1
countColRange[11] = 1
countColRange[12] = 1
countColRange[13] = 1

countColRange[20] = 1
countColRange[21] = 1
countColRange[22] = 1
countColRange[23] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 31
ID = 30
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[31] = 1
countColRange[32] = 1
countColRange[33] = 1
countColRange[34] = 1

countColRange[40] = 1
countColRange[41] = 1
countColRange[42] = 1
countColRange[43] = 1

countColRange[1] = 1
countColRange[2] = 1
countColRange[3] = 1
countColRange[4] = 1

countColRange[11] = 1
countColRange[12] = 1
countColRange[13] = 1
countColRange[14] = 1

countColRange[21] = 1
countColRange[22] = 1
countColRange[23] = 1
countColRange[24] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 32
ID = 31
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[32] = 1
countColRange[33] = 1
countColRange[34] = 1
countColRange[35] = 1

countColRange[41] = 1
countColRange[42] = 1
countColRange[43] = 1
countColRange[44] = 1

countColRange[2] = 1
countColRange[3] = 1
countColRange[4] = 1
countColRange[5] = 1

countColRange[12] = 1
countColRange[13] = 1
countColRange[14] = 1
countColRange[15] = 1

countColRange[22] = 1
countColRange[23] = 1
countColRange[24] = 1
countColRange[25] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 33
ID = 32
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[33] = 1
countColRange[34] = 1
countColRange[35] = 1
countColRange[36] = 1

countColRange[42] = 1
countColRange[43] = 1
countColRange[44] = 1
countColRange[45] = 1

countColRange[3] = 1
countColRange[4] = 1
countColRange[5] = 1
countColRange[6] = 1

countColRange[13] = 1
countColRange[14] = 1
countColRange[15] = 1
countColRange[16] = 1

countColRange[23] = 1
countColRange[24] = 1
countColRange[25] = 1
countColRange[26] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 34
ID = 33
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[34] = 1
countColRange[35] = 1
countColRange[36] = 1
countColRange[37] = 1

countColRange[43] = 1
countColRange[44] = 1
countColRange[45] = 1
countColRange[46] = 1

countColRange[4] = 1
countColRange[5] = 1
countColRange[6] = 1
countColRange[7] = 1

countColRange[14] = 1
countColRange[15] = 1
countColRange[16] = 1
countColRange[17] = 1

countColRange[24] = 1
countColRange[25] = 1
countColRange[26] = 1
countColRange[27] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 35
ID = 34
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[35] = 1
countColRange[36] = 1
countColRange[37] = 1
countColRange[38] = 1

countColRange[44] = 1
countColRange[45] = 1
countColRange[46] = 1
countColRange[47] = 1

countColRange[5] = 1
countColRange[6] = 1
countColRange[7] = 1
countColRange[8] = 1

countColRange[15] = 1
countColRange[16] = 1
countColRange[17] = 1
countColRange[18] = 1

countColRange[25] = 1
countColRange[26] = 1
countColRange[27] = 1
countColRange[28] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 36
ID = 35
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[36] = 1
countColRange[37] = 1
countColRange[38] = 1
countColRange[39] = 1

countColRange[45] = 1
countColRange[46] = 1
countColRange[47] = 1
countColRange[48] = 1

countColRange[6] = 1
countColRange[7] = 1
countColRange[8] = 1
countColRange[9] = 1

countColRange[16] = 1
countColRange[17] = 1
countColRange[18] = 1
countColRange[19] = 1

countColRange[26] = 1
countColRange[27] = 1
countColRange[28] = 1
countColRange[29] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 37
ID = 36
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[37] = 1
countColRange[38] = 1
countColRange[39] = 1
countColRange[40] = 1

countColRange[46] = 1
countColRange[47] = 1
countColRange[48] = 1
countColRange[49] = 1

countColRange[7] = 1
countColRange[8] = 1
countColRange[9] = 1
countColRange[10] = 1

countColRange[17] = 1
countColRange[18] = 1
countColRange[19] = 1
countColRange[20] = 1

countColRange[27] = 1
countColRange[28] = 1
countColRange[29] = 1
countColRange[30] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 38
ID = 37
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[38] = 1
countColRange[39] = 1
countColRange[40] = 1
countColRange[41] = 1

countColRange[47] = 1
countColRange[48] = 1
countColRange[49] = 1
countColRange[1] = 1

countColRange[8] = 1
countColRange[9] = 1
countColRange[10] = 1
countColRange[11] = 1

countColRange[18] = 1
countColRange[19] = 1
countColRange[20] = 1
countColRange[21] = 1

countColRange[28] = 1
countColRange[29] = 1
countColRange[30] = 1
countColRange[31] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 39
ID = 38
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[39] = 1
countColRange[40] = 1
countColRange[41] = 1
countColRange[42] = 1

countColRange[48] = 1
countColRange[49] = 1
countColRange[1] = 1
countColRange[2] = 1

countColRange[9] = 1
countColRange[10] = 1
countColRange[11] = 1
countColRange[12] = 1

countColRange[19] = 1
countColRange[20] = 1
countColRange[21] = 1
countColRange[22] = 1

countColRange[29] = 1
countColRange[30] = 1
countColRange[31] = 1
countColRange[32] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 40
ID = 39
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[40] = 1
countColRange[41] = 1
countColRange[42] = 1
countColRange[43] = 1

countColRange[49] = 1
countColRange[1] = 1
countColRange[2] = 1
countColRange[3] = 1

countColRange[10] = 1
countColRange[11] = 1
countColRange[12] = 1
countColRange[13] = 1

countColRange[20] = 1
countColRange[21] = 1
countColRange[22] = 1
countColRange[23] = 1

countColRange[30] = 1
countColRange[31] = 1
countColRange[32] = 1
countColRange[33] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 41
ID = 40
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[41] = 1
countColRange[42] = 1
countColRange[43] = 1
countColRange[44] = 1

countColRange[1] = 1
countColRange[2] = 1
countColRange[3] = 1
countColRange[4] = 1

countColRange[11] = 1
countColRange[12] = 1
countColRange[13] = 1
countColRange[14] = 1

countColRange[21] = 1
countColRange[22] = 1
countColRange[23] = 1
countColRange[24] = 1

countColRange[31] = 1
countColRange[32] = 1
countColRange[33] = 1
countColRange[34] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 42
ID = 41
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[42] = 1
countColRange[43] = 1
countColRange[44] = 1
countColRange[45] = 1

countColRange[2] = 1
countColRange[3] = 1
countColRange[4] = 1
countColRange[5] = 1

countColRange[12] = 1
countColRange[13] = 1
countColRange[14] = 1
countColRange[15] = 1

countColRange[22] = 1
countColRange[23] = 1
countColRange[24] = 1
countColRange[25] = 1

countColRange[32] = 1
countColRange[33] = 1
countColRange[34] = 1
countColRange[35] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 43
ID = 42
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[43] = 1
countColRange[44] = 1
countColRange[45] = 1
countColRange[46] = 1

countColRange[3] = 1
countColRange[4] = 1
countColRange[5] = 1
countColRange[6] = 1

countColRange[13] = 1
countColRange[14] = 1
countColRange[15] = 1
countColRange[16] = 1

countColRange[23] = 1
countColRange[24] = 1
countColRange[25] = 1
countColRange[26] = 1

countColRange[33] = 1
countColRange[34] = 1
countColRange[35] = 1
countColRange[36] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 44
ID = 43
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[44] = 1
countColRange[45] = 1
countColRange[46] = 1
countColRange[47] = 1

countColRange[4] = 1
countColRange[5] = 1
countColRange[6] = 1
countColRange[7] = 1

countColRange[14] = 1
countColRange[15] = 1
countColRange[16] = 1
countColRange[17] = 1

countColRange[24] = 1
countColRange[25] = 1
countColRange[26] = 1
countColRange[27] = 1

countColRange[34] = 1
countColRange[35] = 1
countColRange[36] = 1
countColRange[37] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 45
ID = 44
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[45] = 1
countColRange[46] = 1
countColRange[47] = 1
countColRange[48] = 1

countColRange[5] = 1
countColRange[6] = 1
countColRange[7] = 1
countColRange[8] = 1

countColRange[15] = 1
countColRange[16] = 1
countColRange[17] = 1
countColRange[18] = 1

countColRange[25] = 1
countColRange[26] = 1
countColRange[27] = 1
countColRange[28] = 1

countColRange[35] = 1
countColRange[36] = 1
countColRange[37] = 1
countColRange[38] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 46
ID = 45
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[46] = 1
countColRange[47] = 1
countColRange[48] = 1
countColRange[49] = 1

countColRange[6] = 1
countColRange[7] = 1
countColRange[8] = 1
countColRange[9] = 1

countColRange[16] = 1
countColRange[17] = 1
countColRange[18] = 1
countColRange[19] = 1

countColRange[26] = 1
countColRange[27] = 1
countColRange[28] = 1
countColRange[29] = 1

countColRange[36] = 1
countColRange[37] = 1
countColRange[38] = 1
countColRange[39] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 47
ID = 46
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[47] = 1
countColRange[48] = 1
countColRange[49] = 1
countColRange[1] = 1

countColRange[7] = 1
countColRange[8] = 1
countColRange[9] = 1
countColRange[10] = 1

countColRange[17] = 1
countColRange[18] = 1
countColRange[19] = 1
countColRange[20] = 1

countColRange[27] = 1
countColRange[28] = 1
countColRange[29] = 1
countColRange[30] = 1

countColRange[37] = 1
countColRange[38] = 1
countColRange[39] = 1
countColRange[40] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 48
ID = 47
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[48] = 1
countColRange[49] = 1
countColRange[1] = 1
countColRange[2] = 1

countColRange[8] = 1
countColRange[9] = 1
countColRange[10] = 1
countColRange[11] = 1

countColRange[18] = 1
countColRange[19] = 1
countColRange[20] = 1
countColRange[21] = 1

countColRange[28] = 1
countColRange[29] = 1
countColRange[30] = 1
countColRange[31] = 1

countColRange[38] = 1
countColRange[39] = 1
countColRange[40] = 1
countColRange[41] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 49
ID = 48
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[49] = 1
countColRange[1] = 1
countColRange[2] = 1
countColRange[3] = 1

countColRange[9] = 1
countColRange[10] = 1
countColRange[11] = 1
countColRange[12] = 1

countColRange[19] = 1
countColRange[20] = 1
countColRange[21] = 1
countColRange[22] = 1

countColRange[29] = 1
countColRange[30] = 1
countColRange[31] = 1
countColRange[32] = 1

countColRange[39] = 1
countColRange[40] = 1
countColRange[41] = 1
countColRange[42] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ====== �W�C ==================================================
# 50
ID = 49
# �w�q��� countColRange ���w�n�έp����� ===========================
#- countColRange = np.zeros(50, dtype='i8')
countColRange = np.zeros(50, dtype='i8')
countColRange[49] = 1
countColRange[1] = 1
countColRange[2] = 1
countColRange[3] = 1

countColRange[9] = 1
countColRange[10] = 1
countColRange[11] = 1
countColRange[12] = 1

countColRange[19] = 1
countColRange[20] = 1
countColRange[21] = 1
countColRange[22] = 1

countColRange[29] = 1
countColRange[30] = 1
countColRange[31] = 1
countColRange[32] = 1

countColRange[39] = 1
countColRange[40] = 1
countColRange[41] = 1
countColRange[42] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

# �w�q�ĴX�� ========================================================
# 51
ID = 50
# �w�q��� countColRange ���w�n�έp����� ===========================
countColRange = np.zeros(50, dtype='i8')
countColRange[49] = 1
countColRange[1] = 1
countColRange[2] = 1
countColRange[3] = 1

countColRange[9] = 1
countColRange[10] = 1
countColRange[11] = 1
countColRange[12] = 1

countColRange[19] = 1
countColRange[20] = 1
countColRange[21] = 1
countColRange[22] = 1

countColRange[29] = 1
countColRange[30] = 1
countColRange[31] = 1
countColRange[32] = 1

countColRange[39] = 1
countColRange[40] = 1
countColRange[41] = 1
countColRange[42] = 1

res = weighting_function(jump, countColRange, target_Dw_x_y_z)
countdata[ID][0] = res[0]
countdata[ID][1] = res[1]

#-----------------------------
#print countdata[ID][0]
#print countdata[ID][1]

#print countdata
## �A1 ���� ##############################################################################

## �A2 �}�l #### ( ������� )  ###########################################################

# 01 �ݥk R_0105 (�s��_�Ұ�)

# ���� DIST_V1_01_R_0105_factor = 0 (1�B2�B3....)
Total = 1
div = div_R0105
div1= div1_R0105

if div == 0:
    DIST_V1_01_R_0105_factor = 0
else:
    DIST_V1_01_R_0105_factor = 1.0 /div

if div1 == 0:
    DIST_V1_01_R_0105_factor = 0
else:
    DIST_V1_01_R_0105_factor = DIST_V1_01_R_0105_factor * div1

dumpline = 'DIST_V1_01_R_0105_factor = ' + str(DIST_V1_01_R_0105_factor) + ' (' + str(Total) + '/' + str(div) + '*' + str(div1) + ') '
print dumpline

# �w�q��� countColRange ���w�n�έp����� ==================================
#- countColRange = np.zeros(50, dtype='i8')    ## ID = 48
countColRange = np.zeros(50, dtype='i8')    ## ID = 48
# �s�� -- [���] = �ƶq
countColRange[1] = 1
countColRange[2] = 1
countColRange[3] = 1
countColRange[4] = 1
countColRange[5] = 1

DIST_V1_01_R_0105 = weighting_function(jump, countColRange, target_Dw_x_y_z)
# �C�L �Ĥ����ܼƪ� ���X�B��ơC
# DIST_V1_01_R_0105_factor = 0 (��J 1�B2�B3....����s���ϼƾ�)
#print DIST_V1_01_R_0105[0]
#print DIST_V1_01_R_0105[1]

##= ���ϦC�L ===================================================================

## �o�@�q�O "�ù�" ��X -------------------------------------------
# print("DIST_V1_01_R_0105[0]", DIST_V1_01_R_0105[0])
# print("DIST_V1_01_R_0105[1]", DIST_V1_01_R_0105[1])

## �o�@�q�O "�ɮ�" ��X -------------------------------------------
# flag = 1 ��ܿ�X�ɮ� ��L�Ʀr(-1, 0, 2, 3, 4..) �h����X
flag=flag_dist_R0105
if flag==1:
    dumpfile = open('dist_V1_01_R_0105_Order.txt', mode='wt')
    textline = ''
    for index in range(50):
        # '\t' tab
        textline = textline + str(DIST_V1_01_R_0105[0][index]) + '\t'
    # '\n' new line
    textline =  textline +  '\n'
    dumpfile.write(textline)
    dumpfile.close()

    dumpfile = open('dist_V1_01_R_0105_Statics.txt', mode='wt')
    textline = ''

    for index in range(50):
        # '\t' tab
        textline = textline + str(DIST_V1_01_R_0105[1][index]) + '\t'
    # '\n' new line
    textline =  textline + '\n'
    dumpfile.write(textline)
    dumpfile.close()
## �o�@�q�O�ɮ׿�X���� ==========================================
# 02 �ݥ� 4049 (�s��_�Ұ�)

# ���� DIST_V1_01_L_4549_factor = 0 (1�B2�B3....)
Total = 1
div = div_L4549
div1 = div1_L4549

if div == 0:
    DIST_V1_01_L_4549_factor = 0
else:
    DIST_V1_01_L_4549_factor = 1.0 /div

if div1 == 0:
    DIST_V1_01_L_4549_factor = 0
else:
    DIST_V1_01_L_4549_factor  =  DIST_V1_01_L_4549_factor*div1

dumpline = 'DIST_V1_01_L_4549_factor = ' + str(DIST_V1_01_L_4549_factor) + ' (' + str(Total) + '/' + str(div) + '*' + str(div1) + ') '
print dumpline

# �w�q��� countColRange ���w�n�έp����� ==================================
#- countColRange = np.zeros(50, dtype='i8')    ## ID = 48
countColRange = np.zeros(50, dtype='i8')
# �s�� --- [���] = �ƶq
countColRange[45] = 1
countColRange[46] = 1
countColRange[47] = 1
countColRange[48] = 1
countColRange[49] = 1

DIST_V1_01_L_4549 = weighting_function(jump, countColRange, target_Dw_x_y_z)
#print DIST_V1_01_L_4549[0]
#print DIST_V1_01_L_4549[1]

##= ���ϦC�L ================================================================

## �o�@�q�O "�ù�" ��X -------------------------------------------
# print("DIST_V1_01_L_4549[0]", DIST_V1_01_L_4549[0])
# print("DIST_V1_01_L_4549[1]", DIST_V1_01_L_4549[1])

## �o�@�q�O "�ɮ�" ��X -------------------------------------------
# flag = 1 ��ܿ�X�ɮ� ��L�Ʀr(-1, 0, 2, 3, 4..) �h����X
flag=flag_dist_L4549
if flag==1:
    dumpfile = open('dist_V1_01_L_4549_Order.txt', mode='wt')
    textline = ''
    for index in range(50):
        # '\t' tab
        textline = textline + str(DIST_V1_01_L_4549[0][index]) + '\t'
    # '\n' new line
    textline =  textline +  '\n'
    dumpfile.write(textline)
    dumpfile.close()

    dumpfile = open('dist_V1_01_L_4549_Statics.txt', mode='wt')
    textline = ''

    for index in range(50):
        # '\t' tab
        textline = textline + str(DIST_V1_01_L_4549[1][index]) + '\t'
    #  '\n' new line
    textline =  textline + '\n'
    dumpfile.write(textline)
    dumpfile.close()

##==========================================================================
# 03 �ݥk 0102 (�s��_�Ұ�)

# ���� DIST_V1_R_0102_factor = 0 (1�B2�B3....)
Total = 1
div = div_R0102
div1 = div1_R0102

if div == 0:
    DIST_V1_01_R_0102_factor = 0
else:
    DIST_V1_01_R_0102_factor = 1.0 /div

if div1 == 0:
    DIST_V1_01_R_0102_factor = 0
else:
    DIST_V1_01_R_0102_factor = DIST_V1_01_R_0102_factor*div1

dumpline = 'DIST_V1_01_R_0102_factor = ' + str(DIST_V1_01_R_0102_factor) + ' (' + str(Total) + '/' + str(div) + '*' + str(div1) + ') '
print dumpline

# �w�q��� countColRange ���w�n�έp����� ==================================
countColRange = np.zeros(50, dtype='i8')
countColRange[1]  = 2
countColRange[2]  = 2

DIST_V1_01_R_0102 = weighting_function(jump, countColRange, target_Dw_x_y_z)
#print DIST_V1_01_R_0102[0]
#print DIST_V1_01_R_0102[1]

##= ���ϦC�L ================================================================

## �o�@�q�O "�ù�" ��X -------------------------------------------
# print("DIST_V1_01_R_0102[0]", DIST_V1_01_R_0102[0])
# print("DIST_V1_01_R_0102[1]", DIST_V1_01_R_0102[1])

## �o�@�q�O "�ɮ�" ��X -------------------------------------------
# flag = 1 ��ܿ�X�ɮ� ��L�Ʀr(-1, 0, 2, 3, 4..) �h����X
flag=flag_dist_R0102
if flag==1:
    dumpfile = open('dist_V1_01_R_0102_order.txt', mode='wt')
    textline = ''
    for index in range(50):
        # '\t' tab
        textline = textline + str(DIST_V1_01_R_0102[0][index]) + '\t'
    # '\n' new line
    textline =  textline +  '\n'
    dumpfile.write(textline)
    dumpfile.close()

    dumpfile = open('dist_V1_01_R_0102_statics.txt', mode='wt')
    textline = ''

    for index in range(50):
        # '\t' tab
        textline = textline + str(DIST_V1_01_R_0102[1][index]) + '\t'
    # '\n' new line
    textline =  textline + '\n'
    dumpfile.write(textline)
    dumpfile.close()

##==========================================================================
# 04 �ݥ� 4849

# ���� DIST_V1_01_L_4849_factor = 0 (1�B2�B3....)
Total = 1
div = div_L4849
div1 = div1_L4849

if div == 0:
    DIST_V1_01_L_4849_factor = 0
else:
    DIST_V1_01_L_4849_factor = 1.0/div

if div == 0:
    DIST_V1_01_L_4849_factor = 0
else:
    DIST_V1_01_L_4849_factor =  DIST_V1_01_L_4849_factor* div1

dumpline = 'DIST_V1_01_L_4849_factor = ' + str(DIST_V1_01_L_4849_factor) + ' (' + str(Total) + '/' + str(div) + '*' + str(div1) + ') '
print dumpline

# �w�q��� countColRange ���w�n�έp����� ==================================
countColRange = np.zeros(50, dtype='i8')
countColRange[48] = 2
countColRange[49] = 2

DIST_V1_01_L_4849 = weighting_function(jump, countColRange, target_Dw_x_y_z)
#print DIST_V1_01_L_4849[0]
#print DIST_V1_01_L_4849[1]

##= ���ϦC�L ================================================================

## �o�@�q�O "�ù�" ��X -------------------------------------------
# print("DIST_V1_01_L_4849[0]", DIST_V1_01_L_4849[0])
# print("DIST_V1_01_L_4849[1]", DIST_V1_01_L_4849[1])

## �o�@�q�O "�ɮ�" ��X -------------------------------------------
# flag = 1 ��ܿ�X�ɮ� ��L�Ʀr(-1, 0, 2, 3, 4..) �h����X
flag=flag_dist_L4849
if flag==1:
    dumpfile = open('dist_V1_01_L_4849_order.txt', mode='wt')
    textline = ''
    for index in range(50):
        # '\t' tab
        textline = textline + str(DIST_V1_01_L_4849[0][index]) + '\t'
    # '\n' new line
    textline =  textline +  '\n'
    dumpfile.write(textline)
    dumpfile.close()

    dumpfile = open('dist_V1_01_L_4849_statics.txt', mode='wt')
    textline = ''

    for index in range(50):
        # '\t' tab
        textline = textline + str(DIST_V1_01_L_4849[1][index]) + '\t'
    # '\n' new line
    textline =  textline + '\n'
    dumpfile.write(textline)
    dumpfile.close()

##==========================================================================
# 05 �k R_0103 (�s��_�Ұ�)

# ���� DIST_V1_01_R_0103_factor = 0 (1�B2�B3....)
Total = 1
div = div_R0103
div1 = div1_R0103

if div == 0:
    DIST_V1_01_R_0103_factor = 0
else:
    DIST_V1_01_R_0103_factor = 1.0/div

if div1 == 0:
    DIST_V1_01_R_0103_factor = 0
else:
    DIST_V1_01_R_0103_factor = DIST_V1_01_R_0103_factor*div1

dumpline = 'DIST_V1_01_R_0103_factor = ' + str(DIST_V1_01_R_0103_factor) + ' (' + str(Total) + '/' + str(div) +'*' + str(div1) + ') '
print dumpline

# �w�q��� countColRange ���w�n�έp����� ==================================
countColRange = np.zeros(50, dtype='i8')
countColRange[1]  = 2
countColRange[2]  = 1
countColRange[3]  = 1

DIST_V1_01_R_0103 = weighting_function(jump, countColRange, target_Dw_x_y_z)
#print DIST_V1_01_R_0103[0]
#print DIST_V1_01_R_0103[1]

##= ���ϦC�L ================================================================

## �o�@�q�O "�ù�" ��X -------------------------------------------
# print("DIST_V1_01_R_0103[0]", DIST_V1_01_R_0103[0])
# print("DIST_V1_01_R_0103[1]", DIST_V1_01_R_0103[1])

## �o�@�q�O "�ɮ�" ��X -------------------------------------------
# flag = 1 ��ܿ�X�ɮ� ��L�Ʀr(-1, 0, 2, 3, 4..) �h����X
flag=flag_dist_R0103
if flag==1:
    dumpfile = open('dist_V1_01_R_0103_order.txt', mode='wt')
    textline = ''
    for index in range(50):
        # '\t' tab
        textline = textline + str(DIST_V1_01_R_0103[0][index]) + '\t'
    # '\n' new line
    textline =  textline +  '\n'
    dumpfile.write(textline)
    dumpfile.close()

    dumpfile = open('dist_V1_01_R_0103_statics.txt', mode='wt')
    textline = ''

    for index in range(50):
        # '\t' tab
        textline = textline + str(DIST_V1_01_R_0103[1][index]) + '\t'
    # '\n' new line
    textline =  textline + '\n'
    dumpfile.write(textline)
    dumpfile.close()

##==========================================================================
# 06 �� L_4749 (�s��_�Ұ�)

# ���� DIST_V1_01_L_4749_factor = 0 (1�B2�B3....)
Total = 1
div = div_L4749
div1 = div1_L4749

if div == 0:
    DIST_V1_01_L_4749_factor = 0
else:
    DIST_V1_01_L_4749_factor = 1.0 /div

if div1 == 0:
    DIST_V1_01_L_4749_factor = 0
else:
    DIST_V1_01_L_4749_factor  = DIST_V1_01_L_4749_factor *div1

dumpline = 'DIST_V1_01_L_4749_factor = ' + str(DIST_V1_01_L_4749_factor) + ' (' + str(Total) + '/' + str(div) +'*' + str(div1) + ') '
print dumpline

# �w�q��� countColRange ���w�n�έp����� ==================================
countColRange = np.zeros(50, dtype='i8')
countColRange[47] = 1
countColRange[48] = 1
countColRange[49] = 2

DIST_V1_01_L_4749 = weighting_function(jump, countColRange, target_Dw_x_y_z)

#print DIST_V1_01_L_4749[0]
#print DIST_V1_01_L_4749[1]

##= ���ϦC�L ================================================================

## �o�@�q�O "�ù�" ��X -------------------------------------------
# print("DIST_V1_01_L_4749[0]", DIST_V1_01_L_4749[0])
# print("DIST_V1_01_L_4749[1]", DIST_V1_01_L_4749[1])

## �o�@�q�O "�ɮ�" ��X -------------------------------------------
# flag = 1 ��ܿ�X�ɮ� ��L�Ʀr(-1, 0, 2, 3, 4..) �h����X
flag=flag_dist_L4749
if flag==1:
    dumpfile = open('dist_V1_01_L_4749_order.txt', mode='wt')
    textline = ''
    for index in range(50):
        # '\t' tab
        textline = textline + str(DIST_V1_01_L_4749[0][index]) + '\t'
    # '\n' new line
    textline =  textline +  '\n'
    dumpfile.write(textline)
    dumpfile.close()

    dumpfile = open('dist_V1_01_L_4749_statics.txt', mode='wt')
    textline = ''

    for index in range(50):
        # '\t' tab
        textline = textline + str(DIST_V1_01_L_4749[1][index]) + '\t'
    # '\n' new line
    textline =  textline + '\n'
    dumpfile.write(textline)
    dumpfile.close()
#------------------------------------------------------------------------------------------------------------

##= ���ϦC�L ================================================================

## �o�@�q�O "�ù�" ��X -------------------------------------------
# print("DIST_V1_01_L_4749[0]", DIST_V1_01_L_4749[0])
# print("DIST_V1_01_L_4749[1]", DIST_V1_01_L_4749[1])

## �o�@�q�O "�ɮ�" ��X -------------------------------------------
# flag = 1 ��ܿ�X�ɮ� ��L�Ʀr(-1, 0, 2, 3, 4..) �h����X
flag=flag_dist_L4749
if flag==1:
    dumpfile = open('dist_V1_01_L_4749_order.txt', mode='wt')
    textline = ''
    for index in range(50):
        # '\t' tab
        textline = textline + str(DIST_V1_01_L_4749[0][index]) + '\t'
    # '\n' new line
    textline =  textline +  '\n'
    dumpfile.write(textline)
    dumpfile.close()

    dumpfile = open('dist_V1_01_L_4749_statics.txt', mode='wt')
    textline = ''

    for index in range(50):
        # '\t' tab
        textline = textline + str(DIST_V1_01_L_4749[1][index]) + '\t'
    # '\n' new line
    textline =  textline + '\n'
    dumpfile.write(textline)
    dumpfile.close()

#------------------------------------------------------------------------------------------------------------
## �A2 ���� ###############################################################################################################

## �A3 �}�l ##### (DIST_V1_(01�B02�B03...) #####################################################################################################################################################

# �p�� (����)
#- L_coef = np.zeros(50)   ##ID = 48
L_coef = np.zeros(52)
for index in range(1, 50):
##-----------------------------  2 --------------------------  2 ------------------------ 4 --------------------------- 4 ------------------------ 6 -------------------------  6 ----------
    L_coef[index] = DIST_V1_01_L_4549_factor * DIST_V1_01_L_4549[1][index] + DIST_V1_01_L_4849_factor * DIST_V1_01_L_4849[1][index] * + DIST_V1_01_L_4749_factor * DIST_V1_01_L_4749[1][index]

# �p�� (�k��)
#- R_coef = np.zeros(50)   ##ID = 48
R_coef = np.zeros(52)
for index in range(1, 50):
##------------------------------ 1 --------------------------- 1 ------------------------ 3 --------------------------- 3 ------------------------ 5 -------------------------- 5 -----------
    R_coef[index] =  DIST_V1_01_R_0105_factor * DIST_V1_01_R_0105[1][index] + DIST_V1_01_R_0102_factor * DIST_V1_01_R_0102[1][index] +  DIST_V1_01_R_0103_factor * DIST_V1_01_R_0103[1][index]
print R_coef

## �A3 ���� ###################################################################################################################################################################################


## �A4 �}�l ##########################################################################

#- left_countdata = np.zeros(49 * 2 * 50, dtype='i8')   ## "ID = 48"
#- left_countdata = left_countdata.reshape(49, 2, 50)   ## "ID = 48"
left_countdata = np.zeros(51 * 2 * 50, dtype='i8')
left_countdata = left_countdata.reshape(51, 2, 50)

#- for line in range(49):   ## "ID = 48"
for line in range(51):
    for col in range(1, 50):
        left_countdata[line][1][col] = countdata[line][1][col] + L_coef[col]
    left_countdata[line][0] = np.argsort(-left_countdata[line][1])
#------------------------------------------------------------------------------
#- right_countdata = np.zeros(49 * 2 * 50, dtype='i8')    ## "ID = 48"
#- right_countdata = right_countdata.reshape(49, 2, 50)   ## "ID = 48"
right_countdata = np.zeros(51 * 2 * 50, dtype='i8')
right_countdata = right_countdata.reshape(51, 2, 50)


#- for line in range(49):   ## "ID = 48"
for line in range(51):
    for col in range(1, 50):
        right_countdata[line][1][col] = countdata[line][1][50-col] + R_coef[col]
        # �ݸ�
        # print right_countdata[line][1][col], countdata[line][1][50-col],  R_coef[col]
    right_countdata[line][0] = np.argsort(-right_countdata[line][1])

## hcy1
## ��X [�A4 (����)���� �C�L "���X" ] == " V1_01_target_D1_2_3_4 " �� " D1_2_3_5 " ----------
# flag = 1 ��ܿ�X�ɮ� ��L�Ʀr(-1, 0, 2, 3, 4..) �h����X
flag =1
if flag==1:
    #left_out_file = open('Left_output_Order_V1_01_D' + str(targer_w) + '_' + str(targer_x) + '_' + str(targer_y) + '_' + str(targer_z) + '.txt', mode='w')
    #right_out_file = open('Right_output_Order_V1_01_D' + str(targer_w) + '_' + str(targer_x) + '_' + str(targer_y) + '_' + str(targer_z) + '.txt', mode='w')
    left_out_file = open('Left_output_Order_V1_01_D' + '.txt', mode='w')
    right_out_file = open('Right_output_Order_V1_01_D' + '.txt', mode='w')
    outstring = '\t'
    for col in range(1, 50):
        outstring = outstring + str(col) + '\t'
    outstring = outstring + '\n'
    left_out_file.write(outstring)

    #- for line in range(49):   ## "ID = 48" �BLeft_output_Order_V1_01_D1_2_3_4 "ID ��"
    for line in range(51):
        outstring = ''
        outstring = outstring + str(line+1) + '\t'
        for col in range( 49):
            outstring = outstring + str(left_countdata[line][0][col]) + '\t'
        outstring = outstring + '\n'
        left_out_file.write(outstring)

    outstring = '\t'
    for col in range(49, 0, -1):

        outstring = outstring + str(col) + '\t'
    outstring = outstring + '\n'
    right_out_file.write(outstring)

    #- for line in range(49):   ## "ID = 48"
    for line in range(51):
        outstring = ''
        outstring = outstring + str(line+1) + '\t'
        #for col in range(48, -1, -1):
        for col in range( 49):
            outstring = outstring + str(right_countdata[line][0][col]) + '\t'
        outstring = outstring + '\n'
        right_out_file.write(outstring)
    left_out_file.close()
    right_out_file.close()

# hcy1
## ��X == [�A4 (��)�ϧ��� �C�L "�ƶq" ] == " V1_01_target_Dw_x_y_z " �� " D1_2_3_5 "======

# flag = 1 ��ܿ�X�ɮסB��L�Ʀr(-1, 0, 2, 3, 4..) �h����X
flag =1
if flag==1:
    #left_out_file = open('Left_output_Statics_V1_01_D' + str(targer_w) + '_' + str(targer_x) + '_' + str(targer_y) + '_' + str(targer_z) + '.txt', mode='w')
    #right_out_file = open('Right_output_Statics_V1_01_D' + str(targer_w) + '_' + str(targer_x) + '_' + str(targer_y) + '_' + str(targer_z) + '.txt', mode='w')
    left_out_file = open('Left_output_Statics_V1_01_D' + '.txt', mode='w')
    right_out_file = open('Right_output_Statics_V1_01_D' + '.txt', mode='w')
    outstring = '\t'
    for col in range(1, 50):
        outstring = outstring + str(col) + '\t'
    outstring = outstring + '\n'
    left_out_file.write(outstring)

    #- for line in range(49):   ## "ID = 48"
    for line in range(51):

        outstring = ''
        outstring = outstring + str(line+1) + '\t'
        for col in range( 1, 50):
            outstring = outstring + str(left_countdata[line][1][col]) + '\t'
        outstring = outstring + '\n'
        left_out_file.write(outstring)

    outstring = '\t'
    for col in range(49, 0, -1):   ## " Right_output_Statics_V1_01_D1_2_3_4 �Ĥ@�C "
        outstring = outstring + str(col) + '\t'
    outstring = outstring + '\n'
    right_out_file.write(outstring)

    #- for line in range(49):    ##  "ID = 48"�B Right_output_Statics_V1_01_D1_2_3_4   "ID ��"
    for line in range(51):
        outstring = ''
        outstring = outstring + str(line+1) + '\t'
        #for col in range(49, 0, -1):
        for col in range( 1, 50):
            outstring = outstring + str(right_countdata[line][1][col]) + '\t'
        outstring = outstring + '\n'
        right_out_file.write(outstring)
    left_out_file.close()
    right_out_file.close()

## �A4 ���� ############################################################################
