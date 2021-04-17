# -- coding:big5--
import numpy as np

# 統計 回朔 jump 列 第 col 欄位為 num 時，數字 X 出現幾次
# shift 為統計時 忽略data前面無關的欄位
def jump_collection (data, jump=1, col=4, num=1, shift=4):
    count = np.zeros(50, dtype='i8')

    # 一列一列
    for index in range(jump, np.size(data, 0)) :
        if data[index-jump][col] == num:

            #print data[index]----U1D1.2.3..逐次列出；期次、號碼。---
            #print data[index]
            count[data[index][shift]] = count[data[index][shift]] + 1
            count[data[index][shift+1]] = count[data[index][shift+1]] + 1
            count[data[index][shift+2]] = count[data[index][shift+2]] + 1
            count[data[index][shift+3]] = count[data[index][shift+3]] + 1
            count[data[index][shift+4]] = count[data[index][shift+4]] + 1
            count[data[index][shift+5]] = count[data[index][shift+5]] + 1
    return count
