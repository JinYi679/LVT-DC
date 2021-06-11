import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import os
from matplotlib.pyplot import MultipleLocator

#12.80629 42.01097

def Read_s():
    x = []
    y = []
    with open('F:/DataCenter_location.txt','r') as f:
        for i in f.readlines():
            info = i.split(';')
            info[1] = info[1].strip()
            a = float(info[0])
            b = float(info[1])
            x.append(a)
            y.append(b)
    return x, y

def draw(sx, sy):
    x, y = Read_s()
    plt.figure(figsize=(10, 7))
    print(1)
    cx = [12.4674,12.5165,12.4718]
    cy = [41.9187,41.8803,41.8216]
    plt.title('Data center distribution', Fontsize = 'x-large')
    plt.xticks(np.arange(12.20661, 13.0, 0.15))
    plt.yticks(np.arange(41.72532, 42.2, 0.08))
    plt.scatter(sx, sy, s = 0.01, c = '#B3B3B5', alpha = 0.5, label = 'MVs trajectory')
    plt.scatter(x, y, s = 7, c = 'b', alpha = 1, label = 'General data center')
    print('!')
    r=0.03
    for i in range(len(cx)):
        x = np.arange(cx[i] - r, cx[i] + r + 0.00001, 0.00001)
        y = cy[i] + np.sqrt(r ** 2 - (x - cx[i]) ** 2)
        y1 = cy[i] - np.sqrt(r ** 2 - (x - cx[i]) ** 2)
        if i == 0:
            plt.scatter(cx[i],cy[i], s=80 ,c='k', marker='*',alpha=1, label = 'Advanced data center')
            plt.plot(x, y, color='k', label = 'Flight range')
        else:
            plt.scatter(cx[i],cy[i], s=80 ,c='k', marker='*',alpha=1)
            plt.plot(x, y, color='k')
        plt.plot(x, y1, color='k')
    #plt.scatter(cx, cy, s = 30 ,c='k', marker='*', alpha=1, label = 'Advanced data center')


    
    pic = plt.legend(loc = 'upper right', fontsize = 'medium')
    #调整图例散点的大小
    pic.legendHandles[0]._sizes = [30]
    pic.legendHandles[1]._sizes = [30]
    pic.legendHandles[2]._sizes = [30]
    pic.legendHandles[3]._sizes = [30]
    plt.savefig('5.2.png')
    plt.show()

def Draw_result(x, y, sx, sy):
    #plt.figure(figsize=(828, 608.4)) #宽/高
    #plt.title('Simulation diagram', Fontsize = 'x-large')
    plt.xticks(np.arange(12.20661, 13.0, 0.15))
    plt.yticks(np.arange(41.72532, 42.2, 0.08)) #8:5

    plt.scatter(x, y, s = 0.01, c = '#B3B3B5', alpha = 0.5)
    plt.scatter(sx, sy, s = 7, c = 'r', alpha = 1)
    pic = plt.legend(('MVs trajectory', 'Sensor deployment'),loc = 'upper right',fontsize = 'medium')
    #调整图例散点的大小
    pic.legendHandles[0]._sizes = [30]
    pic.legendHandles[1]._sizes = [30]
    plt.savefig('5.1.eps', format = 'eps', bbox_inches='tight', dpi = 600, pad_inches = 0.0)
    print("success!")
    plt.show()

def Set_sensor(maxlon=12.80629,maxlat=42.01097,minlon=12.20661,minlat=41.72532,lonsize=500,latsize=500,sensorNum=1000):
    lonblocksize=(maxlon-minlon)/lonsize
    latblocksize=(maxlat-minlat)/latsize
    maps=[list() for i in range(lonsize)]
    for i in range(lonsize):
        maps[i]=[list() for k in range(latsize)]
    times,X,Y=readfile(lonblocksize,latblocksize,minlon,minlat,maps)
    sensorX=[]
    sensorY=[]
    for i in range(1000):
        r=random.random()
        index=0
        indey=0
        for k in range(lonsize):
            if(r<=0):
                break
            for j in range(latsize):
                r-=float(len(maps[k][j]))/float(times)
                if (r <= 0):
                    index=k
                    indey=j
                    times-=len(maps[k][j])
                    maps[k][j]=[]
                    break
        sensorX.append(random.uniform(index*lonblocksize+minlon,(index+1)*lonblocksize+minlon))
        sensorY.append(random.uniform(indey*latblocksize+minlat,(indey+1)*latblocksize+minlat))
    return sensorX,sensorY,X,Y

def readfile(lonblocksize,latblocksize,minlon,minlat,maps):
    times=0
    X=[]
    Y=[]
    for i in range(1,91):
        print("读取第",i,"个文件")
        with open('F:/Lab Data/' + str(i) + '.txt','r') as f:
            for s in f.readlines():
                x=s.split(';')
                x[2]=x[2].strip()
                index_x=(float(x[1])-minlon)/lonblocksize
                index_y=(float(x[2])-minlat)/latblocksize
                index_x=int(index_x)
                index_y=int(index_y)
                maps[index_x][index_y].append((x[1],x[2]))
                X.append(float(x[1]))
                Y.append(float(x[2]))
                times+=1
    return times,X,Y

def r():
    X = []
    Y = []
    for i in range(1,91):
        print("读取第",i,"个文件")
        with open('F:/Lab Data/' + str(i) + '.txt','r') as f:
            for s in f.readlines():
                x=s.split(';')
                x[2]=x[2].strip()
                X.append(float(x[1]))
                Y.append(float(x[2]))
    return X,Y

if __name__=='__main__':
    sensorX = []
    sensorY = []
    x, y = r()
    print('开始画图')
    
    f = open("sensor_location.txt", 'r')
    for i in f.readlines():
        a = i.split(';')
        a[1] = a[1].strip()
        sensorX.append(float(a[0]))
        sensorY.append(float(a[1]))
    f.close()
    
    Draw_result(x, y, sensorX, sensorY)
    #draw(x, y)