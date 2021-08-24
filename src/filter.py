# -- coding:big5--
import numpy as np

# Dwxyz 資料結構定義
class distribution_structure:
    def __init__(self, _jump):
        self.n = []
        self.jump = _jump
        self.distribution = np.zeros(self.jump * 50, dtype='i8')
        self.distribution = self.distribution.reshape(self.jump, 50)

# 改寫原本的 D_1_2_3_4
def Distribution(therawdata, thejump, n):
    dist = distribution_structure(thejump)
    for i in n:
        dist.n.append(i)
    dist.jump = thejump
    for U in range(dist.jump):
        tmpdata = np.zeros(50, dtype='i8')
        for col in range(1, 50):
            for i in n:
                tmpdata[col] = tmpdata[col] + therawdata[U][i-1][1][col]
        dist.distribution[U] = np.argsort(-tmpdata)
        # print "U = ", U
        # print tmpdata
        # print dist.distribution[U]
    return dist

### 權重函數
def weighting_function(weight, data):
    thecountdata = np.zeros(2 * 50, dtype='i8')
    thecountdata = thecountdata.reshape(2, 50)
    for U in range(data.jump):
        for num in range(1, 50):
            for r in range(1, 50):
                if data.distribution[U][r-1] == num:
                    # print num, r, data.distribution[U][r-1]
                    thecountdata[1][num] = thecountdata[1][num] + weight[r];
    thecountdata[0] = np.argsort(-thecountdata[1])
    return thecountdata

## 代替原本的乙一 欄位改成由檔案 filter.txt 讀入 組數無上限
def load_filter(targetDwxyz):
    filterdata = np.loadtxt('filter.txt', comments="#", dtype='i8')
    linenumber = np.size(filterdata, 0)
    print 'Total filter rules = ', linenumber
    thecountdata = np.zeros(linenumber * 2 * 50)
    thecountdata = thecountdata.reshape(linenumber, 2, 50)
    for i in range(linenumber):
        print '\tDealing with rule ', i
        res = weighting_function(filterdata[i], targetDwxyz)
        thecountdata[i][0] = res[0]
        thecountdata[i][1] = res[1]
    return thecountdata


def load_subfilter(targetDwxyz):
    subfilterdata = np.loadtxt('subfilter.txt', comments="#", dtype={'names':('Name', 'div', 'div2', 'IO', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49'), 'formats':('|S10', np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int, np.int)})
    linenumber = np.size(subfilterdata, 0)
    # print subfilterdata
    L_index = 0
    R_index = 0
    L_linenumber = 0
    R_linenumber = 0
    for i in range(linenumber):
        if subfilterdata[i][0][0] == 'L':
            L_linenumber = L_linenumber + 1
        elif subfilterdata[i][0][0] == 'R':
            R_linenumber = R_linenumber + 1
    print 'Total subfilter rules = ', linenumber, ' L-rules ', L_linenumber, ' R-rules ', R_linenumber
    L_dist =  np.zeros(L_linenumber * 2 * 50)
    R_dist =  np.zeros(R_linenumber * 2 * 50)
    L_dist = L_dist.reshape(L_linenumber, 2, 50)
    R_dist = R_dist.reshape(R_linenumber, 2, 50)
    filter = np.zeros(50, dtype='i8')

    L_coef = np.zeros(50)
    R_coef = np.zeros(50)
    for i in range(linenumber):
        for j in range(1, 50):
            filter[j] = subfilterdata[i][j+3]
        print '\tDealing with rule ', subfilterdata[i][0]
        res = weighting_function(filter, targetDwxyz)
        if subfilterdata[i][0][0] == 'L':
            L_dist[L_index][0] = res[0]
            L_dist[L_index][1] = res[1]
            L_index = L_index + 1
        elif subfilterdata[i][0][0] == 'R':
            R_dist[R_index][0] = res[0]
            R_dist[R_index][1] = res[1]
            R_index = R_index + 1

    L_index = 0
    R_index = 0
    for i in range(linenumber):
        factor = 0.0
        if subfilterdata[i][1] == 0:
            factor = 0.0
        else:
            factor = 1.0 / subfilterdata[i][1]
        if subfilterdata[i][2] == 0:
            factor = 0.0
        else:
            factor = factor*subfilterdata[i][2]

        if subfilterdata[i][0][0] == 'L':
            for j in range(1, 50):
                L_coef[j] = L_coef[j] + factor * L_dist[L_index][1][j]
            L_index = L_index + 1
        elif subfilterdata[i][0][0] == 'R':
            for j in range(1, 50):
                R_coef[j] = R_coef[j] + factor * R_dist[R_index][1][j]
            R_index = R_index + 1
    # print L_coef
    # print R_coef

    # 檔案輸出
    L_index = 0
    R_index = 0
    for i in range(linenumber):
        outputfilename = subfilterdata[i][0] + '_order.txt'
        # print outputfilename
        if subfilterdata[i][3] == 1: # IO 輸出
            outputfile = open(outputfilename, mode='at')

            outstring = '## \t\t'
            for col in range(1, 50):
                outstring = outstring + str(col) + '\t'
            outstring = outstring + '\n'
            outputfile.write(outstring)

            dumpstring = 'D'
            for j in targetDwxyz.n:
                dumpstring = dumpstring + '_' + str(j)
            dumpstring = dumpstring + '\t'
            if subfilterdata[i][0][0] == 'L':
                for index in range(50):
                    dumpstring = dumpstring + '{:.0f}'.format(L_dist[L_index][0][index]) + '\t'
                dumpstring = dumpstring + '\n'
                outputfile.write(dumpstring)
            if subfilterdata[i][0][0] == 'R':
                for index in range(50):
                    dumpstring = dumpstring + '{:.0f}'.format(R_dist[R_index][0][index]) + '\t'
                dumpstring = dumpstring + '\n'
                outputfile.write(dumpstring)
            # print dumpstring
            outputfile.close()

        outputfilename = subfilterdata[i][0] + '_statics.txt'
        # print outputfilename
        if subfilterdata[i][3] == 1: # IO 輸出
            outputfile = open(outputfilename, mode='at')

            outstring = '## \t\t'
            for col in range(1, 50):
                outstring = outstring + str(col) + '\t'
            outstring = outstring + '\n'
            outputfile.write(outstring)

            dumpstring = 'D'
            for j in targetDwxyz.n:
                dumpstring = dumpstring + '_' + str(j)
            dumpstring = dumpstring + '\t'
            if subfilterdata[i][0][0] == 'L':
                for index in range(50):
                    dumpstring = dumpstring + '{:.0f}'.format(L_dist[L_index][1][index]) + '\t'
                dumpstring = dumpstring + '\n'
                outputfile.write(dumpstring)
            if subfilterdata[i][0][0] == 'R':
                for index in range(50):
                    dumpstring = dumpstring + '{:.0f}'.format(R_dist[R_index][1][index]) + '\t'
                dumpstring = dumpstring + '\n'
                outputfile.write(dumpstring)
            # print dumpstring
            outputfile.close()

        if subfilterdata[i][0][0] == 'L':
            L_index = L_index + 1
        elif subfilterdata[i][0][0] == 'R':
            R_index = R_index + 1

    return (L_coef, R_coef)
