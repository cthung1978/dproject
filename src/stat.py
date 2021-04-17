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
#### 統計資料輸出檔名 若是留空白則不輸出
#staticsoutputfilename = 'V4_01_order_output.txt'
staticsoutputfilename = ''  # 檔名留空 表示不輸出
#### 要跳的列數 jump ---- ( 輸入：600 ~ 1500 )
jump = 3
#### 原本的 D_1_2_3_4 改成變數控制 D_{d1}_{d2}_{d3}_{d4} 一共 4 個數字
combo_number = 4
#### 最後輸出檔案是 left_order.txt right_order.txt left_statics.txt right_statics.txt
#### 每次重新跑程式 並不會清空檔案內容，而是接續原本的檔案內容繼續寫入，若是不需要舊檔案內容，記得清空
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
if staticsoutputfilename != '':
    outputfile = open(staticsoutputfilename, mode='w')
rawdata = np.zeros(jump * 7 * 2 * 50, dtype='i8')
rawdata = rawdata.reshape(jump, 7, 2, 50)
for U in range (1, jump+1):
    # 列出總期數---------------------------------
    #print U
    watch = data[np.size(data, 0)-U]
    #print watch
    for D in range (4, 11):
        a = jc.jump_collection (data, U, D, watch[D])
        dumy = a + 1
        dumy[0] = 0

        # print ("U=", U, "D=", D, a)--- 輸出 U1_D1-D7-------------------
        #print ("U=", U, "D=", D-3, a)
        sortdata = np.argsort(-dumy)

        #print ("Sort U=", U, "D=", D, sortdata)--- ## 偵錯  ##-----------
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


### 檔案輸出
## 輸出 === [乙4 完成 列印 "號碼" ] == " V4_01_target" → " D1_2_3_5 " ======
# flag = 1 表示輸出檔案 其他數字(-1, 0, 2, 3, 4..) 則不輸出
flag=1
if flag > 0:
    left_order_out_file = open('left_order.txt', mode='at')
    right_order_out_file = open('right_order.txt', mode='at')
    left_statics_out_file = open('left_statics.txt', mode='at')
    right_statics_out_file = open('right_statics.txt', mode='at')

### Distribution 取代原本的 D_1_2_3_4
for d in combinations([1, 2, 3, 4, 5, 6, 7], combo_number):
    # print d
    dumpline = 'D_' + str(d[0]) + '_' + str(d[1]) + '_' + str(d[2]) + '_' + str(d[3])
    print dumpline
    target_Dw_x_y_z = filter.Distribution(rawdata, jump, d)
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
