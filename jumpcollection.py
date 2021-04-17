# -- coding:big5--
import numpy as np

# �έp �^�� jump �C �� col ��쬰 num �ɡA�Ʀr X �X�{�X��
# shift ���έp�� ����data�e���L�������
def jump_collection (data, jump=1, col=4, num=1, shift=4):
    count = np.zeros(50, dtype='i8')

    # �@�C�@�C
    for index in range(jump, np.size(data, 0)) :
        if data[index-jump][col] == num:

            #print data[index]----U1D1.2.3..�v���C�X�F�����B���X�C---
            #print data[index]
            count[data[index][shift]] = count[data[index][shift]] + 1
            count[data[index][shift+1]] = count[data[index][shift+1]] + 1
            count[data[index][shift+2]] = count[data[index][shift+2]] + 1
            count[data[index][shift+3]] = count[data[index][shift+3]] + 1
            count[data[index][shift+4]] = count[data[index][shift+4]] + 1
            count[data[index][shift+5]] = count[data[index][shift+5]] + 1
    return count
