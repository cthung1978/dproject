# -- coding:big5--
import numpy as np

def jump_collection (data, jump=1, col=4, num=1):
    count = np.zeros(50, dtype='i8')

    # 一列一列
    for index in range(jump, np.size(data, 0)) :
        if data[index-jump][col] == num:

            #print data[index]   ## U1D1.2.3..逐次列出；期次、號碼。
            count[data[index][4]] = count[data[index][4]] + 1
            count[data[index][5]] = count[data[index][5]] + 1
            count[data[index][6]] = count[data[index][6]] + 1
            count[data[index][7]] = count[data[index][7]] + 1
            count[data[index][8]] = count[data[index][8]] + 1
            count[data[index][9]] = count[data[index][9]] + 1
    return count

### 權重函數
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
# 列印  jump = 1300  資料 ( 打開 print D1_2_3_4[U] )
order_outputfile = open('V1_01_order_output.txt', mode='w')
static_outputfile = open('V1_01_static_output.txt', mode='w')

# 乙2 區段變數
# 變數設定在這裡；輸入 "倍數 div = /、div1 = * " " 上值 = 0 不列計算"。
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

# 檔案是否顯示 (輸入 " = 1 列印 " " = 0 不列印 ")
flag_dist_L4549 = 1
flag_dist_L4849 = 0
flag_dist_L4749 = 0
#-------------------
flag_dist_R0105 = 1
flag_dist_R0102 = 0
flag_dist_R0103 = 0

#-------------------------------------------------------
# numpy 的 size 函數 查詢資料長度 0 表示列
# print np.size(data, 0)
# numpy 的 size 函數 查詢資料長度 1 表示欄
# print np.size(data, 1)
# numpy 的 size 函數 查詢資料總個數
# print np.size(data)

a = jump_collection (data, 1, 6, 20)
#print a

#U = 1
#D = 1

# 最後一筆資料 index = np.size(data, 0) - 1
# "螢幕" 輸出期數、日期、球碼
watch = data[np.size(data, 0)-1]
print watch

# hcy1 -------------------------------------------
# 要跳的列數 jump ---- ( 輸入：50 ~ 1500 )

jump = 100
#-------------------------------------------------
rawdata = np.zeros(jump * 7 * 2 * 50, dtype='i8')
rawdata = rawdata.reshape(jump, 7, 2, 50)
for U in range (1, jump+1):
    # 列出總期數---------------------------------
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
    # 列出總期數---------------------------------
    #print U
    for D in range (4, 11):
        outstring = str(U) + '\t' + str(D-3) + '\t'
        for i in range(np.size(rawdata[U-1][D-4][1])):
            outstring = outstring + str(rawdata[U-1][D-4][1][i]) + '\t'
        outstring = outstring + '\n'
        static_outputfile.write(outstring)
static_outputfile.close()

## UxDy 資料已經輸出到檔案 記憶體有一組 rawdata[U][D][?] 供後續計算
## rawdata[0][0][0][0] 表示 U1D1 開獎號碼第一名
## rawdata[0][0][1][0] 表示 U1D1 開獎號碼出現次數

## 甲 開始  ### 編輯 "七路" 頁面組合 (四合一式、共 35 組) #####################################################################
## 01  定義檔案流水號 在 乙1 開始
D1_2_3_4 = np.zeros(jump * 50, dtype='i8')
D1_2_3_4 = D1_2_3_4.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        # ---------------------- [1] ------------------- [2] ------------------- [3] ------------------- [4] -- (標項數目減 1 )
        tmpdata[col] = rawdata[U][0][1][col] + rawdata[U][1][1][col] + rawdata[U][2][1][col] + rawdata[U][3][1][col]
    D1_2_3_4[U] = np.argsort(-tmpdata)
    # 列印 D1、2 、.... 6、7 。共 1300 列。 輸出檔名：V1_01_order_output -------------
    #print D1_2_3_4[U]

## 02
D1_2_3_5 = np.zeros(jump * 50, dtype='i8')
D1_2_3_5 = D1_2_3_5.reshape(jump, 50)
tmpdata = np.zeros(50, dtype='i8')
for U in range(jump):
    for col in range(1, 50):
        # rawdata[U][D][col]
        # print rawdata[U][0][1][col], rawdata[U][1][1][col], rawdata[U][2][1][col], rawdata[U][3][1][col]
        # ---------------------- [1] ------------------- [2] ------------------- [3] ------------------- [5] -- (標項數目減 1 )
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

## 甲 結束 ####################################################################################################################################################

## 乙1 開始  ##########################################################################################################################################
# 替代變數取代後面所有的  weighting_functio(jump, countColRange, target_Dw_x_y_z)
#target_Dw_x_y_z = D1_2_3_4
target_Dw_x_y_z = D1234567

# 以下定義檔案流水號
targer_w = 1
targer_x = 2
targer_y = 3
targer_z = 4

## 增設 ID 修改
#- countdata = np.zeros(49 * 2 * 50)         ## 原 ID 48
#- countdata = countdata.reshape(49, 2, 50)  ## 原 ID 48
countdata = np.zeros(51 * 2 * 50)
countdata = countdata.reshape(51, 2, 50)

# 定義第幾組 =======================================================
# 乙1 區第一組 [從 0 開始到 48 (計 49 組)]
# 01
ID = 0
# 定義欄位 countColRange 指定要統計的欄位。
#- countColRange = np.zeros(50, dtype='i8')  ## 原 ID 48  "不改"
countColRange = np.zeros(50, dtype='i8')
# 編輯 [欄位 (號碼)] = 數量
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

# 這一段是 "螢幕" 輸出 乙區 第一組的 號碼、支數。
# 未含 乙2 DIST_V1_01_R_0101_factor = 0 (1、2、3....變化值)。
# print countdata[ID][0]
# print countdata[ID][1]

# 定義第幾組 =======================================================
# 02
ID = 1
# 定義欄位 countColRange 指定要統計的欄位 ==========================
countColRange = np.zeros(50, dtype='i8')
# 編輯 -- [欄位] = 數量
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


# 定義第幾組 =======================================================
# 03
ID = 2
# 定義欄位 countColRange 指定要統計的欄位 ==========================
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

# 定義第幾組 =======================================================
# 04
ID = 3
# 定義欄位 countColRange 指定要統計的欄位 ==========================
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

# 定義第幾組 =======================================================
# 05
ID = 4
# 定義欄位 countColRange 指定要統計的欄位 ==========================
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

# 定義第幾組 =========================================================
# 06
ID = 5
# 定義欄位 countColRange 指定要統計的欄位 ============================
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

# 定義第幾組 =======================================================
# 07
ID = 6
# 定義欄位 countColRange 指定要統計的欄位 ==========================
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

# 定義第幾組 ========================================================
# 08
ID = 7
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 09
ID = 8
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 10
ID = 9
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 11
ID = 10
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 12
ID = 11
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 13
ID = 12
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 14
ID = 13
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 15
ID = 14
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 16
ID = 15
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 17
ID = 16
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 18
ID = 17
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 19
ID = 18
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 20
ID = 19
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 21
ID = 20
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 22
ID = 21
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 23
ID = 22
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 24
ID = 23
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 25
ID = 24
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 26
ID = 25
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 27
ID = 26
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 28
ID = 27
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 29
ID = 28
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 30
ID = 29
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 31
ID = 30
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 32
ID = 31
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 33
ID = 32
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 34
ID = 33
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 35
ID = 34
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 36
ID = 35
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 37
ID = 36
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 38
ID = 37
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 39
ID = 38
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 40
ID = 39
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 41
ID = 40
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 42
ID = 41
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 43
ID = 42
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 44
ID = 43
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 45
ID = 44
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 46
ID = 45
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 47
ID = 46
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 48
ID = 47
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 49
ID = 48
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ====== 增列 ==================================================
# 50
ID = 49
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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

# 定義第幾組 ========================================================
# 51
ID = 50
# 定義欄位 countColRange 指定要統計的欄位 ===========================
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
## 乙1 結束 ##############################################################################

## 乙2 開始 #### ( 粹取分布 )  ###########################################################

# 01 端右 R_0105 (編輯于甲區)

# 倍數 DIST_V1_01_R_0105_factor = 0 (1、2、3....)
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

# 定義欄位 countColRange 指定要統計的欄位 ==================================
#- countColRange = np.zeros(50, dtype='i8')    ## ID = 48
countColRange = np.zeros(50, dtype='i8')    ## ID = 48
# 編輯 -- [欄位] = 數量
countColRange[1] = 1
countColRange[2] = 1
countColRange[3] = 1
countColRange[4] = 1
countColRange[5] = 1

DIST_V1_01_R_0105 = weighting_function(jump, countColRange, target_Dw_x_y_z)
# 列印 第六組變數的 號碼、支數。
# DIST_V1_01_R_0105_factor = 0 (輸入 1、2、3....不更新本區數據)
#print DIST_V1_01_R_0105[0]
#print DIST_V1_01_R_0105[1]

##= 本區列印 ===================================================================

## 這一段是 "螢幕" 輸出 -------------------------------------------
# print("DIST_V1_01_R_0105[0]", DIST_V1_01_R_0105[0])
# print("DIST_V1_01_R_0105[1]", DIST_V1_01_R_0105[1])

## 這一段是 "檔案" 輸出 -------------------------------------------
# flag = 1 表示輸出檔案 其他數字(-1, 0, 2, 3, 4..) 則不輸出
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
## 這一段是檔案輸出結束 ==========================================
# 02 端左 4049 (編輯于甲區)

# 倍數 DIST_V1_01_L_4549_factor = 0 (1、2、3....)
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

# 定義欄位 countColRange 指定要統計的欄位 ==================================
#- countColRange = np.zeros(50, dtype='i8')    ## ID = 48
countColRange = np.zeros(50, dtype='i8')
# 編輯 --- [欄位] = 數量
countColRange[45] = 1
countColRange[46] = 1
countColRange[47] = 1
countColRange[48] = 1
countColRange[49] = 1

DIST_V1_01_L_4549 = weighting_function(jump, countColRange, target_Dw_x_y_z)
#print DIST_V1_01_L_4549[0]
#print DIST_V1_01_L_4549[1]

##= 本區列印 ================================================================

## 這一段是 "螢幕" 輸出 -------------------------------------------
# print("DIST_V1_01_L_4549[0]", DIST_V1_01_L_4549[0])
# print("DIST_V1_01_L_4549[1]", DIST_V1_01_L_4549[1])

## 這一段是 "檔案" 輸出 -------------------------------------------
# flag = 1 表示輸出檔案 其他數字(-1, 0, 2, 3, 4..) 則不輸出
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
# 03 端右 0102 (編輯于甲區)

# 倍數 DIST_V1_R_0102_factor = 0 (1、2、3....)
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

# 定義欄位 countColRange 指定要統計的欄位 ==================================
countColRange = np.zeros(50, dtype='i8')
countColRange[1]  = 2
countColRange[2]  = 2

DIST_V1_01_R_0102 = weighting_function(jump, countColRange, target_Dw_x_y_z)
#print DIST_V1_01_R_0102[0]
#print DIST_V1_01_R_0102[1]

##= 本區列印 ================================================================

## 這一段是 "螢幕" 輸出 -------------------------------------------
# print("DIST_V1_01_R_0102[0]", DIST_V1_01_R_0102[0])
# print("DIST_V1_01_R_0102[1]", DIST_V1_01_R_0102[1])

## 這一段是 "檔案" 輸出 -------------------------------------------
# flag = 1 表示輸出檔案 其他數字(-1, 0, 2, 3, 4..) 則不輸出
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
# 04 端左 4849

# 倍數 DIST_V1_01_L_4849_factor = 0 (1、2、3....)
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

# 定義欄位 countColRange 指定要統計的欄位 ==================================
countColRange = np.zeros(50, dtype='i8')
countColRange[48] = 2
countColRange[49] = 2

DIST_V1_01_L_4849 = weighting_function(jump, countColRange, target_Dw_x_y_z)
#print DIST_V1_01_L_4849[0]
#print DIST_V1_01_L_4849[1]

##= 本區列印 ================================================================

## 這一段是 "螢幕" 輸出 -------------------------------------------
# print("DIST_V1_01_L_4849[0]", DIST_V1_01_L_4849[0])
# print("DIST_V1_01_L_4849[1]", DIST_V1_01_L_4849[1])

## 這一段是 "檔案" 輸出 -------------------------------------------
# flag = 1 表示輸出檔案 其他數字(-1, 0, 2, 3, 4..) 則不輸出
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
# 05 右 R_0103 (編輯于甲區)

# 倍數 DIST_V1_01_R_0103_factor = 0 (1、2、3....)
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

# 定義欄位 countColRange 指定要統計的欄位 ==================================
countColRange = np.zeros(50, dtype='i8')
countColRange[1]  = 2
countColRange[2]  = 1
countColRange[3]  = 1

DIST_V1_01_R_0103 = weighting_function(jump, countColRange, target_Dw_x_y_z)
#print DIST_V1_01_R_0103[0]
#print DIST_V1_01_R_0103[1]

##= 本區列印 ================================================================

## 這一段是 "螢幕" 輸出 -------------------------------------------
# print("DIST_V1_01_R_0103[0]", DIST_V1_01_R_0103[0])
# print("DIST_V1_01_R_0103[1]", DIST_V1_01_R_0103[1])

## 這一段是 "檔案" 輸出 -------------------------------------------
# flag = 1 表示輸出檔案 其他數字(-1, 0, 2, 3, 4..) 則不輸出
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
# 06 左 L_4749 (編輯于甲區)

# 倍數 DIST_V1_01_L_4749_factor = 0 (1、2、3....)
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

# 定義欄位 countColRange 指定要統計的欄位 ==================================
countColRange = np.zeros(50, dtype='i8')
countColRange[47] = 1
countColRange[48] = 1
countColRange[49] = 2

DIST_V1_01_L_4749 = weighting_function(jump, countColRange, target_Dw_x_y_z)

#print DIST_V1_01_L_4749[0]
#print DIST_V1_01_L_4749[1]

##= 本區列印 ================================================================

## 這一段是 "螢幕" 輸出 -------------------------------------------
# print("DIST_V1_01_L_4749[0]", DIST_V1_01_L_4749[0])
# print("DIST_V1_01_L_4749[1]", DIST_V1_01_L_4749[1])

## 這一段是 "檔案" 輸出 -------------------------------------------
# flag = 1 表示輸出檔案 其他數字(-1, 0, 2, 3, 4..) 則不輸出
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

##= 本區列印 ================================================================

## 這一段是 "螢幕" 輸出 -------------------------------------------
# print("DIST_V1_01_L_4749[0]", DIST_V1_01_L_4749[0])
# print("DIST_V1_01_L_4749[1]", DIST_V1_01_L_4749[1])

## 這一段是 "檔案" 輸出 -------------------------------------------
# flag = 1 表示輸出檔案 其他數字(-1, 0, 2, 3, 4..) 則不輸出
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
## 乙2 結束 ###############################################################################################################

## 乙3 開始 ##### (DIST_V1_(01、02、03...) #####################################################################################################################################################

# 計算 (左用)
#- L_coef = np.zeros(50)   ##ID = 48
L_coef = np.zeros(52)
for index in range(1, 50):
##-----------------------------  2 --------------------------  2 ------------------------ 4 --------------------------- 4 ------------------------ 6 -------------------------  6 ----------
    L_coef[index] = DIST_V1_01_L_4549_factor * DIST_V1_01_L_4549[1][index] + DIST_V1_01_L_4849_factor * DIST_V1_01_L_4849[1][index] * + DIST_V1_01_L_4749_factor * DIST_V1_01_L_4749[1][index]

# 計算 (右用)
#- R_coef = np.zeros(50)   ##ID = 48
R_coef = np.zeros(52)
for index in range(1, 50):
##------------------------------ 1 --------------------------- 1 ------------------------ 3 --------------------------- 3 ------------------------ 5 -------------------------- 5 -----------
    R_coef[index] =  DIST_V1_01_R_0105_factor * DIST_V1_01_R_0105[1][index] + DIST_V1_01_R_0102_factor * DIST_V1_01_R_0102[1][index] +  DIST_V1_01_R_0103_factor * DIST_V1_01_R_0103[1][index]
print R_coef

## 乙3 結束 ###################################################################################################################################################################################


## 乙4 開始 ##########################################################################

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
        # 待詳
        # print right_countdata[line][1][col], countdata[line][1][50-col],  R_coef[col]
    right_countdata[line][0] = np.argsort(-right_countdata[line][1])

## hcy1
## 輸出 [乙4 (丙區)完成 列印 "號碼" ] == " V1_01_target_D1_2_3_4 " → " D1_2_3_5 " ----------
# flag = 1 表示輸出檔案 其他數字(-1, 0, 2, 3, 4..) 則不輸出
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

    #- for line in range(49):   ## "ID = 48" 、Left_output_Order_V1_01_D1_2_3_4 "ID 數"
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
## 輸出 == [乙4 (丙)區完成 列印 "數量" ] == " V1_01_target_Dw_x_y_z " → " D1_2_3_5 "======

# flag = 1 表示輸出檔案、其他數字(-1, 0, 2, 3, 4..) 則不輸出
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
    for col in range(49, 0, -1):   ## " Right_output_Statics_V1_01_D1_2_3_4 第一列 "
        outstring = outstring + str(col) + '\t'
    outstring = outstring + '\n'
    right_out_file.write(outstring)

    #- for line in range(49):    ##  "ID = 48"、 Right_output_Statics_V1_01_D1_2_3_4   "ID 數"
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

## 乙4 結束 ############################################################################
