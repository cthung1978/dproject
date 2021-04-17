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
#### �έp��ƿ�X�ɦW �Y�O�d�ťիh����X
#staticsoutputfilename = 'V4_01_order_output.txt'
staticsoutputfilename = ''  # �ɦW�d�� ��ܤ���X
#### �n�����C�� jump ---- ( ��J�G600 ~ 1500 )
jump = 3
#### �쥻�� D_1_2_3_4 �令�ܼƱ��� D_{d1}_{d2}_{d3}_{d4} �@�@ 4 �ӼƦr
combo_number = 4
#### �̫��X�ɮ׬O left_order.txt right_order.txt left_statics.txt right_statics.txt
#### �C�����s�]�{�� �ä��|�M���ɮפ��e�A�ӬO����쥻���ɮפ��e�~��g�J�A�Y�O���ݭn���ɮפ��e�A�O�o�M��
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
if staticsoutputfilename != '':
    outputfile = open(staticsoutputfilename, mode='w')
rawdata = np.zeros(jump * 7 * 2 * 50, dtype='i8')
rawdata = rawdata.reshape(jump, 7, 2, 50)
for U in range (1, jump+1):
    # �C�X�`����---------------------------------
    #print U
    watch = data[np.size(data, 0)-U]
    #print watch
    for D in range (4, 11):
        a = jc.jump_collection (data, U, D, watch[D])
        dumy = a + 1
        dumy[0] = 0

        # print ("U=", U, "D=", D, a)--- ��X U1_D1-D7-------------------
        #print ("U=", U, "D=", D-3, a)
        sortdata = np.argsort(-dumy)

        #print ("Sort U=", U, "D=", D, sortdata)--- ## ����  ##-----------
        #print ("Sort U=", U, "D=", D-3, sortdata)

        outstring = str(U) + sep + str(D-3) + '\t'
        rawdata[U-1][D-4][0] = sortdata
        rawdata[U-1][D-4][1] = a

        for i in range(np.size(sortdata)):
            outstring = outstring + str(sortdata[i]) + '\t'
        outstring = outstring + '\n'
        if staticsoutputfilename != '':
            outputfile.write(outstring)
if staticsoutputfilename != '':
    outputfile.close()


### �ɮ׿�X
## ��X === [�A4 ���� �C�L "���X" ] == " V4_01_target" �� " D1_2_3_5 " ======
# flag = 1 ��ܿ�X�ɮ� ��L�Ʀr(-1, 0, 2, 3, 4..) �h����X
flag=1
if flag > 0:
    left_order_out_file = open('left_order.txt', mode='at')
    right_order_out_file = open('right_order.txt', mode='at')
    left_statics_out_file = open('left_statics.txt', mode='at')
    right_statics_out_file = open('right_statics.txt', mode='at')

### Distribution ���N�쥻�� D_1_2_3_4
for d in combinations([1, 2, 3, 4, 5, 6, 7], combo_number):
    # print d
    dumpline = 'D_' + str(d[0]) + '_' + str(d[1]) + '_' + str(d[2]) + '_' + str(d[3])
    print dumpline
    target_Dw_x_y_z = filter.Distribution(rawdata, jump, d)
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
            outstring = 'D_w_x_y_z' + sep + sep
            for col in range(1, 50):
                outstring = outstring + "{0:>2d}".format(col) + sep
            outstring = outstring + '\n'
            left_order_out_file.write(outstring)

        for line in range(linenumber):
            outstring = 'D_' + str(target_Dw_x_y_z.n[0]) + '_' + str(target_Dw_x_y_z.n[1]) + '_' + str(target_Dw_x_y_z.n[2]) + '_' + str(target_Dw_x_y_z.n[3]) + sep
            outstring = outstring + "{0:>2d}".format(line+1) + sep
            for col in range( 49):
                outstring = outstring + "{0:>2d}".format(left_countdata[line][0][col]) + sep
            outstring = outstring + '\n'
            left_order_out_file.write(outstring)

        if flag == 1:
            outstring = 'D_w_x_y_z' + sep + sep
            for col in range(49, 0, -1):
                outstring = outstring + "{0:>2d}".format(col) + sep
            outstring = outstring + '\n'
            right_order_out_file.write(outstring)

        for line in range(linenumber):
            outstring = 'D_' + str(target_Dw_x_y_z.n[0]) + '_' + str(target_Dw_x_y_z.n[1]) + '_' + str(target_Dw_x_y_z.n[2]) + '_' + str(target_Dw_x_y_z.n[3]) + sep
            outstring = outstring + "{0:>2d}".format(line+1) + sep
            for col in range( 49):
                outstring = outstring + "{0:>2d}".format(right_countdata[line][0][col]) + sep
            outstring = outstring + '\n'
            right_order_out_file.write(outstring)

    if flag > 0:

        if flag == 1:
            outstring = 'D_w_x_y_z' + sep + sep
            for col in range(1, 50):
                outstring = outstring + "{0:>2d}".format(col) + sep
            outstring = outstring + '\n'
            left_statics_out_file.write(outstring)

        for line in range(linenumber):
            outstring = 'D_' + str(target_Dw_x_y_z.n[0]) + '_' + str(target_Dw_x_y_z.n[1]) + '_' + str(target_Dw_x_y_z.n[2]) + '_' + str(target_Dw_x_y_z.n[3]) + sep
            outstring = outstring + "{0:>2d}".format(line+1) + sep
            for col in range( 1, 50):
                outstring = outstring + "{0:>2d}".format(left_countdata[line][1][col]) + sep
            outstring = outstring + sep
            left_statics_out_file.write(outstring)

        if flag == 1:
            flag = 2
            outstring = 'D_w_x_y_z' + sep + sep
            for col in range(49, 0, -1):
                outstring = outstring + "{0:>2d}".format(col) + sep
            outstring = outstring + '\n'
            right_statics_out_file.write(outstring)

        for line in range(linenumber):
            outstring = 'D_' + str(target_Dw_x_y_z.n[0]) + '_' + str(target_Dw_x_y_z.n[1]) + '_' + str(target_Dw_x_y_z.n[2]) + '_' + str(target_Dw_x_y_z.n[3]) + sep
            outstring = outstring + "{0:>2d}".format(line+1) + sep
            #for col in range(49, 0, -1):
            for col in range( 1, 50):
                outstring = outstring + "{0:>2d}".format(right_countdata[line][1][col]) + sep
            outstring = outstring + '\n'
            right_statics_out_file.write(outstring)


if flag > 0:
    left_order_out_file.close()
    right_order_out_file.close()
    left_statics_out_file.close()
    right_statics_out_file.close()
