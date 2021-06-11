import math
import random
import Distance
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from matplotlib.legend_handler import HandlerPathCollection
# 12.4674,41.9187

#test
def initTestData():
    data = []
    with open('testData1.txt', 'r') as f:
        for s in f.readlines():
            x = s.split()
            x[1] = x[1].strip()
            data.append([float(x[0]), float(x[1])])
    return data

#test
def initData():
    data1 = []
    data2 = []
    with open('testData3.txt','r') as f:
        for s in f.readlines():
            x = s.split(';')
            x[1] = x[1].strip()
            data1.append([float(x[0]), float(x[1])])
    with open('testData2.txt','r') as f:
        for s in f.readlines():
            x = s.split(';')
            x[1] = x[1].strip()
            data2.append([float(x[0]), float(x[1])])
    return data1, data2


def evaluate(ways, maps):
    sum = 0
    for i in range(1, len(ways)):
        sum += maps[ways[i]][ways[i - 1]]
    sum += maps[ways[len(ways)-1]][0]
    return sum
# N为每次降温迭代步长
# T为降温次数
# a为降温系数
# t0为初始温度

def Linju(ghh,num):
    temp = [i for i in ghh]
    rand1 = random.randint(0, 65535) % (num-1)
    rand1 += 1
    rand2 = random.randint(0, 65535) % (num-1)
    rand2 += 1
    while rand1 == rand2:
        rand1 = random.randint(0, 65535) % (num - 1)
        rand1 += 1
        rand2 = random.randint(0, 65535) % (num - 1)
        rand2 += 1
    t = temp[rand1]
    temp[rand1] = temp[rand2]
    temp[rand2] = t
    return temp

#模拟退火
def findMinWay(data, N = 80, T = 2000, a=0.98, t0=550):
    num = len(data)
    maps = [[] for i in range(len(data))]
    for i in range(len(data)):
        maps[i] = [0 for j in range(len(data))]
    for i in range(len(maps)):
        for j in range(len(maps[i])):
            xd = data[i][0] - data[j][0]
            yd = data[i][1] - data[j][1]
            rij = math.sqrt((xd * xd + yd * yd) / 10.0)
            tij = math.trunc(rij)
            dij = 0
            if tij < rij:
                dij = rij + 1
            else:
                dij = rij
            maps[i][j] = dij
    temp = [i for i in range(1, len(data))]
    random.shuffle(temp)
    ghh = [0] + temp
    bestevaluation = evaluate(ghh, maps)
    GhhEvaluation = bestevaluation
    ghhsecond = [i for i in ghh]
    k = 0
    n = 0
    t = t0
    r = 0
    while k < T:
        n = 0
        while n < N:
            tempGhh = Linju(ghh, num)
            tempevaluation = evaluate(tempGhh, maps)
            if tempevaluation < bestevaluation:
                ghh = tempGhh
                bestevaluation = tempevaluation
            r = random.random()
            if tempevaluation < GhhEvaluation or math.exp((GhhEvaluation - tempevaluation) / t) > r:
                ghhsecond = tempGhh
                GhhEvaluation = tempevaluation
            n += 1
        t = a * t
        k += 1
    ways = []
    for i in range(len(ghh)):
        ways.append([data[ghh[i]][0], data[ghh[i]][1],data[ghh[i]][2]])
    return bestevaluation, ways

def countLineSensorNum(data, leftlon, leftlat, rightlon, rightlat, MDistance=30):
    sum = 0
    num = 0
    for i in range(len(data)):
        a0 = data[i][0]
        b0 = data[i][1]
        a1 = leftlon
        b1 = leftlat
        a2 = rightlon
        b2 = rightlat
        a1a2 = a1-a2
        b1b2 = b1-b2
        if a1a2 == 0 and b1b2 == 0:
            x = a1
            y = b1
        else:
            x = (a0 * a1a2 * a1a2 + b0 * b1b2 * a1a2 - (b2 * a1 - b1 * a2) * b1b2) / (b1b2 * b1b2 + a1a2 * a1a2)
            y = (b0 * b1b2 * b1b2 + a0 * b1b2 * a1a2 + (b2 * a1 - b1 * a2) * a1a2) / (b1b2 * b1b2 + a1a2 * a1a2)

        dist = Distance.distance(x, y, a0, b0)
        dist1 = Distance.distance(x, y, a1, b1)
        dist2 = Distance.distance(x, y, a2, b2)
        dist3 = Distance.distance(a1, b1, a2, b2)
        if dist < MDistance and dist1 + dist2 <= dist3 + 0.5:
            sum += 1
            num += data[i][2]
    return sum,num

def GetOnLine(ways, data, MDistance=60):
    X = []
    Y = []
    waysnum = len(ways)
    datanum = len(data)
    vis = [0 for i in range(datanum)]
    for i in range(waysnum):
        for j in range(datanum):
            if vis[j] == 1:
                continue
            a0 = data[j][0]
            b0 = data[j][1]
            a1 = ways[i][0]
            b1 = ways[i][1]
            a2 = ways[(i + 1) % waysnum][0]
            b2 = ways[(i + 1) % waysnum][1]
            a1a2 = a1 - a2
            b1b2 = b1 - b2
            if a1a2 == 0 and b1b2 == 0:
                x = a1
                y = b1
            else:
                x = (a0 * a1a2 * a1a2 + b0 * b1b2 * a1a2 - (b2 * a1 - b1 * a2) * b1b2) / (b1b2 * b1b2 + a1a2 * a1a2)
                y = (b0 * b1b2 * b1b2 + a0 * b1b2 * a1a2 + (b2 * a1 - b1 * a2) * a1a2) / (b1b2 * b1b2 + a1a2 * a1a2)

            dist = Distance.distance(x, y, a0, b0)
            dist1 = Distance.distance(x, y, a1, b1)
            dist2 = Distance.distance(x, y, a2, b2)
            dist3 = Distance.distance(a1, b1, a2, b2)
            if dist < MDistance:
                print(dist1+dist2, ' ', dist3)
            if dist < MDistance and dist1+dist2<=dist3+0.5 :
                print(data[j][0], ' ', data[j][1], ' ', dist, ' ', i)
                X.append(data[j][0])
                Y.append(data[j][1])
                vis[j] = 1
    return X, Y

#二次优化
def opt2(ways, data2,w1=0.4,w2=0.3, w3=0.3, a=1.15, q=0.9):
    num = len(data2)
    times = [0 for i in range(len(ways))]
    vis = [0 for i in range(num)]
    index = 0
    stop = True
    while stop:
        waysnum = len(ways)
        fi=[[] for i in range(waysnum)]
        for i in range(waysnum):
            fi[i] = [0 for j in range(num)]
        for index in range(waysnum):
            # print(index,' ',(index + 1) % waysnum,' ',len(ways))

            nc,nv = countLineSensorNum(data2, ways[index][0], ways[index][1], ways[(index + 1) % waysnum][0],
                                    ways[(index + 1) % waysnum][1])
            nc += 2
            lens = Distance.distance(ways[index][0], ways[index][1], ways[(index + 1) % waysnum][0],
                                     ways[(index + 1) % waysnum][1])
            nv += ways[index][2] + ways[(index + 1) % waysnum][2]
            for i in range(num):
                if vis[i] == 1:
                    continue

                nci1, nvi1 = countLineSensorNum(data2, ways[index][0], ways[index][1], data2[i][0], data2[i][1])
                nci2 ,nvi2= countLineSensorNum(data2, data2[i][0], data2[i][1], ways[(index + 1) % waysnum][0],
                                          ways[(index + 1) % waysnum][1])
                nci = nci1 + nci2 + 2
                nvi = nvi1 + nvi2
                lensi = Distance.distance(ways[index][0], ways[index][1], data2[i][0], data2[i][1])
                lensi += Distance.distance(data2[i][0], data2[i][1], ways[(index + 1) % waysnum][0],
                                           ways[(index + 1) % waysnum][1])
                qa = math.pow(q, times[index])
                if lensi > qa * a * lens:
                    continue
                # print(nc, ' ',nci,' ',lens,' ',lensi,' ',ways[index][0],' ',ways[index][1],' ',ways[(index+1)%num][0],' ',ways[(index+1)%num][1])
                fi[index][i] =w1*(nvi-nv)/nv+ w2 * (nci - nc) / nc - w3 * (lensi - lens) / lens
        maxm = 0
        maxindex1 = -1
        maxindex2 = -1
        for i in range(waysnum):
            for j in range(num):
                if vis[i] == 1:
                    continue
                if maxm < fi[i][j]:
                    maxm = fi[i][j]
                    maxindex1 = i
                    maxindex2 = j
        if maxindex1 == -1 or maxindex2 == -1:
            stop = False

        else:
            ways.insert(maxindex1 + 1, [data2[maxindex2][0], data2[maxindex2][1],data2[maxindex2][2]])
            times.insert(maxindex1 + 1, times[maxindex1] + 1)
            times[maxindex1] += 1
            print(maxindex2)
            vis[maxindex2] = 1

def draw(center_x,center_y,base_x,base_y,basesensor_x,basesensor_y,noreachsensor_x,noreachsensor_y,line_x,line_y,between_x,between_y,xticks,yticks):
    #plt.figure(figsize=(15, 15))
    r=0.02
    
    x_min = center_x[0] - r - 0.001
    x_max = center_x[0] + r + 0.001
    y_min = center_y[0] - r - 0.001
    y_max = center_y[0] + r + 0.001

    x_major_locator = MultipleLocator(0.01)
    y_major_locator = MultipleLocator(0.01)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    
    plt.xticks(xticks) #xticks
    plt.yticks(yticks) #yticks
    plt.scatter(base_x, base_y, s=0.01, c='#B3B3B5', alpha=0.5)
    plt.scatter(basesensor_x,basesensor_y,s=40,c='w',alpha=1, marker= 'o',edgecolors='g')
    plt.scatter(noreachsensor_x,noreachsensor_y,s=40,c='w',alpha=1, marker= 'o',edgecolors='g')
   
    for i in range(len(line_x)):
        plt.plot(line_x[i],line_y[i],c='b')
        for j in range(len(line_x[i])):
            plt.scatter(line_x[i][j],line_y[i][j],s=40,c='b',alpha=1)
     
    plt.scatter(between_x,between_y,s=40,c='r',alpha=1)
    
    for i in range(len(center_x)):
        plt.scatter(center_x[i],center_y[i], s= 400,c='k', marker='*',alpha=1)
        x = np.arange(center_x[i] - r, center_x[i] + r + 0.00001, 0.00001)
        y = center_y[i] + np.sqrt(r ** 2 - (x - center_x[i]) ** 2)
        y1 = center_y[i] - np.sqrt(r ** 2 - (x - center_x[i]) ** 2)
        plt.plot(x, y, color='k')
        plt.plot(x, y1, color='k')
    #plt.axis('off')
    plt.savefig('path2.png', bbox_inches='tight', dpi = 600, pad_inches = 0.0)
    plt.show()

def readCarData():
    Data_X=[]
    Data_Y=[]
    for i in range(1,91):
        with open('F:/Lab Data/'+str(i)+'.txt','r') as f:
            while f.readable():
                s = f.readline()
                if len(s)==0:
                    break
                x = s.split(';')
                x[2] = x[2].strip()
                Data_X.append(float(x[1]))
                Data_Y.append(float(x[2]))
    return Data_X, Data_Y


def readSensorData():
    sensor_X=[]
    sensor_Y=[]
    with open('sensor_location.txt','r') as f:
        while f.readable():
            s = f.readline()
            if len(s)<=0:
                break
            x = s.split(';')
            x[1]=x[1].strip()
            sensor_X.append(float(x[0]))
            sensor_Y.append(float(x[1]))
    return sensor_X, sensor_Y


def readFindData1():
    sensor_id = []
    sensor_num = []
    with open('F:/Find Data/1.txt', 'r') as f:
        while f.readable():
            s = f.readline()
            if len(s) <= 0:
                break
            x = s.split(';')
            x[1] = x[1].strip()
            sensor_id.append(int(x[0])-1) #优化了读取文件的问题
            sensor_num.append(int(x[1]))
    return sensor_id, sensor_num

def countCost(line_x,line_y):
    sum=0
    for i in range(1,len(line_x)):
        sum+=Distance.distance(line_x[i],line_y[i],line_x[i-1],line_y[i-1])
    return sum

# 优化了-1和999的问题
# 第二次优化的函数是opt2，将其注释掉就行
def fullData(centralData_X, centralData_Y):
    Data_x, Data_y = readCarData()
    sensor_X, sensor_Y = readSensorData()
    sensor_id, sensor_num = readFindData1()
    path_x=[]
    path_y=[]
    touch_x=[]
    touch_y=[]
    for i in range(len(centralData_X)):
        uns_x = []
        uns_y = []
        s_x = []
        s_y = []
        s_num = []
        uns_num = []
        X = centralData_X[i]
        Y = centralData_Y[i]
        for j in range(1000):
            if Distance.distance(sensor_X[sensor_id[j]],sensor_Y[sensor_id[j]],X,Y) < 1200: # 核心传感器的半径
                if len(s_x) < 5: #初始选择的点数
                    s_x.append(sensor_X[sensor_id[j]])
                    s_y.append(sensor_Y[sensor_id[j]])
                    s_num.append(sensor_num[sensor_id[j]])
                else:
                    uns_x.append(sensor_X[sensor_id[j]])
                    uns_y.append(sensor_Y[sensor_id[j]])
                    uns_num.append(sensor_num[sensor_id[j]])
        s_x=[X]+s_x
        s_y=[Y]+s_y
        s_num=[0]+s_num
        data1=[]
        for i in range(len(s_x)):
            data1.append([s_x[i],s_y[i],s_num[i]])
        data2=[]
        for i in range(len(uns_y)):
            data2.append([uns_x[i],uns_y[i],uns_num[i]])
        score, path = findMinWay(data1) #模拟退火
        opt2(path,data2)# 二次优化
        p_x=[]
        p_y=[]
        for i in range(len(path)):
            p_x.append(path[i][0])
            p_y.append(path[i][1])
        p_x.append(path[0][0])
        p_y.append(path[0][1])
        path_x.append(p_x)
        path_y.append(p_y)
        touch_x=touch_x+p_x
        touch_y=touch_y+p_y
        X2, Y2 = GetOnLine(path, data2)
        touch_x = touch_x + X2
        touch_y = touch_y + Y2
        print(touch_x)
    noreach_x=[]
    noreach_y=[]
    for i in range(1000):
        if sensor_num[i] == 0:
            noreach_x.append(sensor_X[sensor_id[i]])
            noreach_y.append(sensor_Y[sensor_id[i]])
    xticks=np.arange(12.20661, 12.80629, 0.05)
    yticks=np.arange(41.41129, 42.01097, 0.05)
    dis_sum = countCost(path_x, path_y)
    draw(centralData_X, centralData_Y,Data_x, Data_y, sensor_X, sensor_Y,noreach_x,noreach_y,path_x,path_y,touch_x,touch_y,xticks,yticks)


if __name__ == '__main__':
    # data=initTestData()
    # data1, data2 = initData()
    # data1 = [[12.4674, 41.9187]] + data1
    # score, ways = findMinWay(data1)
    # X = []
    # Y = []
    # X1 = []
    # Y1 = []
    # opt2(ways, data2)
    # for i in range(len(ways)):
    #     X.append(ways[i][0])
    #     Y.append(ways[i][1])
    # for i in range(len(data2)):
    #     X1.append(data2[i][0])
    #     Y1.append(data2[i][1])
    # X2, Y2 = GetOnLine(ways, data2)
    # X.append(data1[0][0])
    # Y.append(data1[0][1])
    # draw(Y, X, Y1, X1, 41.9187, 12.4674, Y2, X2)
    # print(ways)
    fullData([12.4674], [41.9187])


