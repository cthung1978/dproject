# -- coding:big5--
import numpy as np
from itertools import combinations

# 引入 jumpcollection.py
import jumpcollection as jc
# 引入 filter.py
import filter

#### 控制變數 #################################################
#### 資料檔案
rawdatafilename = 'CT_002.txt'

#### 統計資料輸出檔名 若是留空白則不輸出  (甲區資料)

orderoutputfilename = 'V2_01_order_output.txt'
staticsoutputfilename = 'V2_01_static_output.txt'
#staticsoutputfilename = ''  # 檔名留空 表示不輸出

#### 要跳的列數 jump ---- ( 輸入：20 ~ 1500 )

jump = 50

#### 原本的 D_1_2_3_4 改成變數控制 D_{d1}_{d2}_{d3}_{d4}、 4 路組合 (輸入：1 ~ 7) 個數字
#### 下方設定值 4、5、6、7；V2_01_order_output.txt "甲區成果" 結果 號碼全相同。

combo_number = 7

#### 每次重新跑程式 並不會清空檔案內容，而是接續原本的檔案內容繼續寫入，若是不需要舊檔案內容，記得清空。
#### 檔案輸出的欄位空間定義
sep = '  '
#### 控制變數結束 ##############################################

# 讀取資料檔案
data = np.loadtxt(rawdatafilename, dtype='i8')
# 最後一筆資料 index = np.size(data, 0) - 1
watch = data[np.size(data, 0)-1]
print watch

# 整理 rawdata[U-1][D-1][0] 排名
# 整理 rawdata[U-1][D-1][1] 統計
rawdata = np.zeros(jump * 7 * 2 * 50, dtype='i8')
rawdata = rawdata.reshape(jump, 7, 2, 50)
if orderoutputfilename != '':
    outputfile = open(orderoutputfilename, mode='w')
for U in range (1, jump+1):
    # 列出總期數---------------------------------
    #print U
    watch = data[np.size(data, 0)-U]
    #print watch
    for D in range (4, 11):
        a = jc.jump_collection (data, U, D, watch[D])
        dumy = a + 1
        dumy[0] = 0

        # print ("U=", U, "D=", D, a)--- 輸出 U1_D1 ~ D7-------------------
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
    # 列出總期數---------------------------------
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

### 檔案輸出
### 輸出 === [乙4 完成 列印 "號碼"、"數量" (subfilter.txt → IO = 0 → 乙1)] == " V2_01_target " → " D1_2_3_5 " ======
### flag = 1 表示輸出檔案 其他數字(-1, 0, 2, 3, 4..) 則不輸出
flag=1
if flag > 0:
    left_order_out_file = open('Left_order.txt', mode='at')
    right_order_out_file = open('Right_order.txt', mode='at')
    left_statics_out_file = open('Left_statics.txt', mode='at')
    right_statics_out_file = open('Right_statics.txt', mode='at')

### Distribution 取代原本的 D_1_2_3_4
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

    ### 函式寫在 filter.py 取代原本 乙一
    ### 統計組數無上限 設定定義在 filter.txt
    countdata = filter.load_filter(target_Dw_x_y_z)
    linenumber = len(countdata)

    (L_coef, R_coef) = filter.load_subfilter(target_Dw_x_y_z)
    #print L_coef
    #print R_coef

    ### 原本的乙四
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
    ### 原本的乙四結束


    if flag > 0:
        if flag == 1:
            #- Left_order.txt 上標題
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
            #- Right_order.txt  上標題
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
            outstring = 'D_w_x_y_z' + '\tID' + '\t' #首列不能對齊可以從這裡微調，自行加入空白
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
