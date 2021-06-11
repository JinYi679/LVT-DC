import math
import random
import Distance
import numpy as np
import matplotlib.pyplot as plt
# 12.4674,41.9187


def initTestData():
    data = []
    with open('testData1.txt', 'r') as f:
        for s in f.readlines():
            x = s.split()
            x[1] = x[1].strip()
            data.append([float(x[0]), float(x[1]),1000])
    return data


def initData():
    data1 = []
    data2 = []
    with open('testData3.txt','r') as f:
        for s in f.readlines():
            x = s.split(';')
            x[1] = x[1].strip()
            data1.append([float(x[0]), float(x[1]),1000])
    with open('testData2.txt','r') as f:
        for s in f.readlines():
            x = s.split(';')
            x[1] = x[1].strip()
            data2.append([float(x[0]), float(x[1]),1000])
    return data1, data2


def evaluate(ways, maps):
    sum = 0
    for i in range(1, len(ways)):
        sum += maps[ways[i]][ways[i - 1]]
    sum += maps[ways[len(ways)-1]][0]
    return sum



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

# N为每次降温迭代步长
# T为降温次数
# a为降温系数
# t0为初始温度
def findMinWay(data, N = 80, T = 2000, a=0.98, t0=550):
    num = len(data)
    maps = [[] for i in range(len(data))]
    for i in range(len(data)):
        maps[i] = [0 for j in range(len(data))]
    for i in range(len(maps)):
        for j in range(len(maps[i])):
            maps[i][j]=Distance.distance(data[i][0],data[i][1],data[j][0],data[j][1])

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
            if tempevaluation < GhhEvaluation or math.exp((GhhEvaluation - tempevaluation) / t) < r:
                ghhsecond = tempGhh
                GhhEvaluation = tempevaluation
            n += 1
        t = a * t
        k += 1
    ways = []
    for i in range(len(ghh)):
        ways.append([data[ghh[i]][0], data[ghh[i]][1],data[ghh[i]][2],data[ghh[i]][3]])
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


def opt2(ways, data2,w1=0.4,w2=0.3, w3=0.3, a=1.15, q=0.9):
    num = len(data2)
    times = [0 for i in range(len(ways))]
    vis = [0 for i in range(num)]
    index = 0
    stop = True
    vis_id=[]
    for i1,i2,i3,i4 in ways:
        vis_id.append(i4)
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
                if nvi==0 and nv==0:
                    nvi=1
                    nv=1
                if nv==0:
                    nv=1
                fi[index][i] =w1*(nvi-nv)/nv+ w2 * (nci - nc) / nc - w3 * (lensi - lens) / lens
        maxm = 0;
        maxindex1 = -1
        maxindex2 = -1
        for i in range(waysnum):
            for j in range(num):
                if vis[j] == 1:
                    continue
                if maxm < fi[i][j]:
                    maxm = fi[i][j]
                    maxindex1 = i
                    maxindex2 = j
        if maxindex1 == -1 or maxindex2 == -1:
            stop = False

        else:
            ways.insert(maxindex1 + 1, [data2[maxindex2][0], data2[maxindex2][1], data2[maxindex2][2]])
            times.insert(maxindex1 + 1, times[maxindex1] + 1)
            times[maxindex1] += 1
            vis_id.append(data2[maxindex2][3])
            print(maxindex2)
            vis[maxindex2] = 1
    return vis_id


def countCost(line_x,line_y):
    sum = 0
    for num in range(len(line_x)):
        for i in range(1, len(line_x[num])):
            sum += Distance.distance(line_x[num][i], line_y[num][i], line_x[num][i-1], line_y[num][i-1])
    return sum


def draw(center_x, center_y, base_x, base_y, basesensor_x, basesensor_y, noreachsensor_x, noreachsensor_y, line_x, line_y, between_x, between_y, xticks, yticks):
    plt.figure(figsize=(15, 15))
    plt.xticks(xticks)
    plt.yticks(yticks)
    plt.scatter(base_x, base_y, s=0.01, c='#B3B3B5', alpha=0.5)
    plt.scatter(basesensor_x, basesensor_y, s=5, c='#7FFFAA', alpha=1)
    plt.scatter(noreachsensor_x, noreachsensor_y, s=5, c='#CD5C5C', alpha=1)
    for i in range(len(line_x)):
        plt.plot(line_x[i], line_y[i], c='b')
    plt.scatter(between_x, between_y, s=5, c='b', alpha=1)
    r = 0.051
    for i in range(len(center_x)):
        plt.scatter(center_x[i], center_y[i], s=10, c='k', marker='*', alpha=1)
        x = np.arange(center_x[i] - r, center_x[i] + r, 0.00001)
        y = center_y[i] + np.sqrt(r ** 2 - (x - center_x[i]) ** 2)
        y1 = center_y[i] - np.sqrt(r ** 2 - (x - center_x[i]) ** 2)
        plt.plot(x, y, color='k')
        plt.plot(x, y1, color='k')
    plt.savefig('fullpath.png')
    plt.show()


def readCarData():
    Data_X = []
    Data_Y = []
    for i in range(1, 91):
        with open('data/'+str(i)+'.txt', 'r') as f:
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
    sensor_X = []
    sensor_Y = []
    with open('sensor_location.txt', ) as f:
        while f.readable():
            s = f.readline()
            if len(s) <= 0:
                break
            x = s.split(';')
            x[1] = x[1].strip()
            sensor_X.append(float(x[0]))
            sensor_Y.append(float(x[1]))
    return sensor_X, sensor_Y


def readFindData(id):
    sensor_id = []
    sensor_num = []
    with open('Find Data/'+str(id)+'.txt', 'r') as f:
        while f.readable():
            s = f.readline()
            if len(s) <= 0:
                break
            x = s.split(';')
            sensor_id.append(int(x[0]))
            sensor_num.append(int(x[1]))
    return sensor_id, sensor_num


# 第二次优化的函数是opt2，将其注释掉就行
def fullData(centralData_X, centralData_Y,id=1):
    Data_x, Data_y = readCarData()
    sensor_X, sensor_Y = readSensorData()
    sensor_id, sensor_num = readFindData(id)
    path_x = []
    path_y = []
    touch_x = []
    touch_y = []
    for i in range(len(centralData_X)):
        uns_x = []
        uns_y = []
        s_x = []
        s_y = []
        s_num = []
        s_id=[]
        uns_num = []
        uns_id=[]
        X = centralData_X[i]
        Y = centralData_Y[i]
        for j in range(1000):
            if  Distance.distance(sensor_X[sensor_id[j]],sensor_Y[sensor_id[j]],X,Y)<3000: # 核心传感器的半径
                if len(s_x) < 2:  # 初始选择的点数
                    s_x.append(sensor_X[sensor_id[j]])
                    s_y.append(sensor_Y[sensor_id[j]])
                    s_num.append(sensor_num[sensor_id[j]])
                    s_id.append(sensor_id[j])
                else:
                    uns_x.append(sensor_X[sensor_id[j]])
                    uns_y.append(sensor_Y[sensor_id[j]])
                    uns_num.append(sensor_num[sensor_id[j]])
                    uns_id.append(sensor_id[j])
        s_x = [X] + s_x
        s_y = [Y] + s_y
        s_num = [0] + s_num
        s_id = [-1]+ s_id
        data1 = []
        for i in range(len(s_x)):
            data1.append([s_x[i], s_y[i], s_num[i],s_id[i]])
        data2=[]
        for i in range(len(uns_y)):
            data2.append([uns_x[i], uns_y[i], uns_num[i],uns_id[i]])
        score, path = findMinWay(data1)
        vis_id=opt2(path, data2)
        p_x = []
        p_y = []
        for i in range(len(path)):
            p_x.append(path[i][0])
            p_y.append(path[i][1])
        p_x.append(path[0][0])
        p_y.append(path[0][1])
        path_x.append(p_x)
        path_y.append(p_y)
        touch_x = touch_x + p_x
        touch_y = touch_y + p_y
        X2, Y2 = GetOnLine(path, data2)
        touch_x = touch_x + X2
        touch_y = touch_y + Y2
        print(touch_x)
    noreach_x = []
    noreach_y = []
    for i in range(1000):
        if sensor_num[i] == 0:
            noreach_x.append(sensor_X[sensor_id[i]])
            noreach_y.append(sensor_Y[sensor_id[i]])
    xticks = np.arange(12.20661, 12.80629, 0.05)
    yticks = np.arange(41.41129, 42.01097, 0.05)
    draw(centralData_X, centralData_Y, Data_x, Data_y, sensor_X, sensor_Y, noreach_x, noreach_y, path_x, path_y, touch_x, touch_y, xticks, yticks)



def fullData2(centralData_X, centralData_Y,id,sensor_vis):
    sensor_X, sensor_Y = readSensorData()
    sensor_id, sensor_num = readFindData(id)
    path_x = []
    path_y = []
    touch_x = []
    touch_y = []
    vis_id = []
    for i in range(len(centralData_X)):
        uns_x = []
        uns_y = []
        s_x = []
        s_y = []
        s_num = []
        s_id=[]
        uns_num = []
        uns_id=[]
        X = centralData_X[i]
        Y = centralData_Y[i]
        for j in range(1000):
            if sensor_vis[sensor_id[j]]==0 and Distance.distance(sensor_X[sensor_id[j]],sensor_Y[sensor_id[j]],X,Y)<3000: # 核心传感器的半径
                if len(s_x) < 2:  # 初始选择的点数
                    s_x.append(sensor_X[sensor_id[j]])
                    s_y.append(sensor_Y[sensor_id[j]])
                    s_num.append(sensor_num[sensor_id[j]])
                    s_id.append(sensor_id[j])
                else:
                    uns_x.append(sensor_X[sensor_id[j]])
                    uns_y.append(sensor_Y[sensor_id[j]])
                    uns_num.append(sensor_num[sensor_id[j]])
                    uns_id.append(sensor_id[j])
        s_x = [X] + s_x
        s_y = [Y] + s_y
        s_num = [0] + s_num
        s_id = [-1]+s_id
        data1 = []
        for i1 in range(len(s_x)):
            data1.append([s_x[i1], s_y[i1], s_num[i1], s_id[i1]])
        data2 = []
        for i2 in range(len(uns_y)):
            data2.append([uns_x[i2], uns_y[i2], uns_num[i2], uns_id[i2]])
        if len(data1) <= 2:
            continue
        score, path = findMinWay(data1)

        v_id = opt2(path, data2)
        vis_id = vis_id+v_id
        p_x = []
        p_y = []
        for i3 in range(len(path)):
            p_x.append(path[i3][0])
            p_y.append(path[i3][1])
        p_x.append(path[0][0])
        p_y.append(path[0][1])
        path_x.append(p_x)
        path_y.append(p_y)
    for i4 in vis_id:
        if i4 != -1:
            sensor_vis[i4] += 10
    return countCost(path_x, path_y)
def solve():
    vis=[0 for i in range(1000)]
    result=[]
    for i in range(1,41):
        value=fullData2([12.4674], [41.9187],i,vis)
        result.append(value)
        print('第',i,'次成本:', value)
        print(vis)
        for j in range(1000):
            if vis[j] != 0:
                vis[j]-=1
    return result
def test1():
    data1, data2 = initData()
    x=[]
    y=[]
    for i in range(len(data2)):
        x.append(data2[i][0]);
        y.append(data2[i][1]);
    plt.figure(figsize=(7, 5))
    plt.xticks(np.arange(12.30661, 12.60629, 0.05))
    plt.yticks(np.arange(41.91129, 42.01097, 0.05))
    plt.scatter(x,y,c='k',s=10)
    plt.show()
if __name__ == '__main__':
    # data=initTestData()
    # data1, data2 = initData()
    # data1 = [[12.4674, 41.9187,1000]] + data1
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
    # fullData([12.4674], [41.9187])
    solve()

