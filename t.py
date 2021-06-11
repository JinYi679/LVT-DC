from datetime import datetime
import datetime
from lab3 import Read_map
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import os
from matplotlib.pyplot import MultipleLocator
from matplotlib.legend_handler import HandlerPathCollection
from cover import Cover1

s = '2018-05-01 11:58:24'
s1 = '2018-06-02 09:13:33'
a = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S') #datetime库和datetime类不是一个东西
b = datetime.datetime.strptime(s1, '%Y-%m-%d %H:%M:%S')
    
c = (a + datetime.timedelta(seconds=28800.0)).strftime("%Y-%m-%d %H:%M:%S")
#print(type(c))
c = datetime.datetime.strptime(c, '%Y-%m-%d %H:%M:%S')
#print(c)

#plt.scatter(x, s = 1., color = (10., 10., 10.), alpha = 0.5)

def Get_T_com(filepath, base):
    vis_T = [0 for i in range(350)]
    cid = 0
    with open(filepath, 'r') as f:
        for i in f.readlines():
            info = i.split('\n')
            t = float(info[0])
            if t > base:
                vis_T[cid] = 1
            cid += 1
            if cid > 316:
                break
    return vis_T


def Res_Write(filepath, msg):
    f = open(filepath, 'a')
    f.write(msg)
    f.close()

def draw():
    fig = plt.figure(figsize=(3.5, 2.5), dpi = 300)
    x = [1, 2, 3, 4, 5]
    y = [1, 2, 3, 4, 5]
    sx = [1, 2, 3, 4, 5]
    sy = [1, 2, 3, 4, 5]
    #plt.figure(figsize=(5, 3.1))
    #plt.title('Simulation diagram', Fontsize = 'x-large')

    plt.xticks(np.arange(12.20661, 13.0, 0.15))
    plt.yticks(np.arange(41.72532, 42.2, 0.08)) #8:5
 
#dpi是设置清晰度的，大于300就很清晰了，但是保存下来的图片很大 
    #plt.savefig(‘result.png', dpi=300)

    plt.scatter(x, y, s = 0.01, c = '#B3B3B5', alpha = 0.5)
    plt.scatter(sx, sy, s = 7, c = 'r', alpha = 1)
    pic = plt.legend(('MVs trajectory', 'Sensor deployment'),loc = 'upper right',fontsize = 'medium')#'medium')
    #调整图例散点的大小
    pic.legendHandles[0]._sizes = [30]
    pic.legendHandles[1]._sizes = [30]
    #plt.savefig('hah.png', bbox_inches='tight', dpi = 600, pad_inches = 0.0)
    print("success!")
    plt.show()


def xlsx_to_csv_pd():
    data_xls = pd.read_excel('E:/GXH/FF_Factors.xls', index_col=0)
    data_xls.to_csv('E:/GXH/2.csv', encoding='utf-8')

def Solve():
    file = 'F:/884-1121.csv'
    df = pd.read_csv(file)
    arr = df.iloc[883:1121,2]
    ans = arr.tolist()
    std = np.std(ans)
    print(std)
Solve()


