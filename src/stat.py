# -- coding:big5--
import numpy as np
from itertools import combinations

# �ޤJ jumpcollection.py
import jumpcollection as jc
# �ޤJ filter.py
import filter

#### �����ܼ� #################################################
#### ����ɮ�
rawdatafilename = 'CT_002.txt'

#### �έp��ƿ�X�ɦW �Y�O�d�ťիh����X  (�Ұϸ��)

orderoutputfilename = 'V2_01_order_output.txt'
staticsoutputfilename = 'V2_01_static_output.txt'
#staticsoutputfilename = ''  # �ɦW�d�� ��ܤ���X

#### �n�����C�� jump ---- ( ��J�G20 ~ 1500 )

jump = 50

#### �쥻�� D_1_2_3_4 �令�ܼƱ��� D_{d1}_{d2}_{d3}_{d4}�B 4 ���զX (��J�G1 ~ 7) �ӼƦr
#### �U��]�w�� 4�B5�B6�B7�FV2_01_order_output.txt "�ҰϦ��G" ���G ���X���ۦP�C

combo_number = 7

#### �C�����s�]�{�� �ä��|�M���ɮפ��e�A�ӬO����쥻���ɮפ��e�~��g�J�A�Y�O���ݭn���ɮפ��e�A�O�o�M�šC
#### �ɮ׿�X�����Ŷ��w�q
sep = '  '
#### �����ܼƵ��� ##############################################

# Ū������ɮ�
data = np.loadtxt(rawdatafilename, dtype='i8')
# �̫�@����� index = np.size(data, 0) - 1
watch = data[np.size(data, 0)-1]
print watch

# ��z rawdata[U-1][D-1][0] �ƦW
# ��z rawdata[U-1][D-1][1] �έp
rawdata = np.zeros(jump * 7 * 2 * 50, dtype='i8')
rawdata = rawdata.reshape(jump, 7, 2, 50)
if orderoutputfilename != '':
    outputfile = open(orderoutputfilename, mode='w')
for U in range (1, jump+1):
    # �C�X�`����---------------------------------
    #print U
    watch = data[np.size(data, 0)-U]
    #print watch
    for D in range (4, 11):
        a = jc.jump_collection (data, U, D, watch[D])
        dumy = a + 1
        dumy[0] = 0

        # print ("U=", U, "D=", D, a)--- ��X U1_D1 ~ D7-------------------
        # print ("U=", U, "D=", D-3, a)
        sortdata = np.argsort(-dumy)

        #print ("Sort U=", U, "D=", D, sortdata)
        # print ("Sort U=", U, "D=", D-3, sortdata)

        outstring = str(U) + sep + str(D-3) + '\t'
        rawdata[U-1][D-4][0] = sortdata
        rawdata[U-1][D-4][1] = a

        for i in range(np.size(sortdata)):
            outstring = outstring + str(sortdata[i]) + '\t'
        outstring = outstring + '\n'
        if orderoutputfilename != '':
            outputfile.write(outstring)
if orderoutputfilename != '':
    outputfile.close()

if staticsoutputfilename != '':
    outputfile = open(staticsoutputfilename, mode='w')
for U in range (1, jump+1):
    # �C�X�`����---------------------------------
    #print U
    watch = data[np.size(data, 0)-U]
    #print watch
    for D in range (4, 11):
        outstring = str(U) + sep + str(D-3) + '\t'

        for i in range(np.size(sortdata)):
            outstring = outstring + str(rawdata[U-1][D-4][1][i]) + '\t'
        outstring = outstring + '\n'
        if staticsoutputfilename != '':
            outputfile.write(outstring)
if staticsoutputfilename != '':
    outputfile.close()

### �ɮ׿�X
### ��X === [�A4 ���� �C�L "���X"�B"�ƶq" (subfilter.txt �� IO = 0 �� �A1)] == " V2_01_target " �� " D1_2_3_5 " ======
### flag = 1 ��ܿ�X�ɮ� ��L�Ʀr(-1, 0, 2, 3, 4..) �h����X
flag=1
if flag > 0:
    left_order_out_file = open('Left_order.txt', mode='at')
    right_order_out_file = open('Right_order.txt', mode='at')
    left_statics_out_file = open('Left_statics.txt', mode='at')
    right_statics_out_file = open('Right_statics.txt', mode='at')

### Distribution ���N�쥻�� D_1_2_3_4
for d in combinations([1, 2, 3, 4, 5, 6, 7], combo_number):
    print "Combo: ", d
    dumpline = 'D'
    for dumpindex in range(0, combo_number):
        dumpline = dumpline + '_' + str(d[dumpindex])
    print dumpline
    # targetDwxyz is the sort number list from the sum(static number) of UnDx + UnDy + UnDz + ....  
    target_Dw_x_y_z = filter.Distribution(rawdata, jump, d)
    # print "target size ", np.size(target_Dw_x_y_z.distribution)
    # print target_Dw_x_y_z.distribution
    # print target_Dw_x_y_z.distribution

    ### �禡�g�b filter.py ���N�쥻 �A�@
    ### �έp�ռƵL�W�� �]�w�w�q�b filter.txt
    countdata = filter.load_filter(target_Dw_x_y_z)
    linenumber = len(countdata)

    (L_coef, R_coef) = filter.load_subfilter(target_Dw_x_y_z)
    #print L_coef
    #print R_coef

    ### �쥻���A�|
    left_countdata = np.zeros(linenumber * 2 * 50, dtype='i8')
    left_countdata = left_countdata.reshape(linenumber, 2, 50)
    for line in range(linenumber):
        for col in range(1, 50):
            left_countdata[line][1][col] = countdata[line][1][col] + L_coef[col]
        left_countdata[line][0] = np.argsort(-left_countdata[line][1])

    right_countdata = np.zeros(linenumber * 2 * 50, dtype='i8')
    right_countdata = right_countdata.reshape(linenumber, 2, 50)

    for line in range(linenumber):
        for col in range(1, 50):
            right_countdata[line][1][col] = countdata[line][1][50-col] + R_coef[col]
        right_countdata[line][0] = np.argsort(-right_countdata[line][1])
    ### �쥻���A�|����


    if flag > 0:
        if flag == 1:
            #- Left_order.txt �W���D
            outstring = 'D_w_x_y_z' + sep + '    ID' + sep
            for col in range(1, 50):
                outstring = outstring + "{0:<2d}".format(col) + sep
            outstring = outstring + '\n'
            left_order_out_file.write(outstring)

        for line in range(linenumber):
            outstring = 'D'
            for stringindex in target_Dw_x_y_z.n:
                outstring = outstring + '_' +  str(stringindex)
            outstring = outstring + sep
            outstring = outstring + "{0:>6d}".format(line+1) + sep
            for col in range( 49):
                outstring = outstring + "{0:<2d}".format(left_countdata[line][0][col]) + sep
            outstring = outstring + '\n'
            left_order_out_file.write(outstring)

        if flag == 1:
            #- Right_order.txt  �W���D
            outstring = 'D_w_x_y_z' + sep + '    ID' + sep
            for col in range(49, 0, -1):
                outstring = outstring + "{0:<2d}".format(col) + sep
            outstring = outstring + '\n'
            right_order_out_file.write(outstring)

        for line in range(linenumber):
            outstring = 'D'
            for stringindex in target_Dw_x_y_z.n:
                outstring = outstring + '_' +  str(stringindex)
            outstring = outstring + sep
            outstring = outstring + "{0:>6d}".format(line+1) + sep
            for col in range( 49):
                outstring = outstring + "{0:<2d}".format(right_countdata[line][0][col]) + sep
            outstring = outstring + '\n'
            right_order_out_file.write(outstring)

    if flag > 0:

        if flag == 1:
            outstring = 'D_w_x_y_z' + '\tID' + '\t' #���C�������i�H�q�o�̷L�աA�ۦ�[�J�ť�
            for col in range(1, 50):
                outstring = outstring + str(col) + '\t'
            outstring = outstring + '\n'
            left_statics_out_file.write(outstring)

        for line in range(linenumber):
            outstring = 'D'
            for stringindex in target_Dw_x_y_z.n:
                outstring = outstring + '_' +  str(stringindex)
            outstring = outstring + '\t'
            outstring = outstring + str(line+1) + '\t'
            for col in range( 1, 50):
                outstring = outstring + str(left_countdata[line][1][col]) + '\t'
            outstring = outstring + '\n'
            left_statics_out_file.write(outstring)

        if flag == 1:
            flag = 2
            outstring = 'D_w_x_y_z' + '\tID'  + '\t'
            for col in range(49, 0, -1):
                outstring = outstring + str(col) + '\t'
            outstring = outstring + '\n'
            right_statics_out_file.write(outstring)

        for line in range(linenumber):
            outstring = 'D'
            for stringindex in target_Dw_x_y_z.n:
                outstring = outstring + '_' +  str(stringindex)
            outstring = outstring + '\t'
            outstring = outstring + str(line+1) + '\t'
            #for col in range(49, 0, -1):
            for col in range( 1, 50):
                outstring = outstring + str(right_countdata[line][1][col]) + '\t'
            outstring = outstring + '\n'
            right_statics_out_file.write(outstring)


if flag > 0:
    left_order_out_file.close()
    right_order_out_file.close()
    left_statics_out_file.close()
    right_statics_out_file.close()
