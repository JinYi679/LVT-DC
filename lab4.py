import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from Distance import distance 
from matplotlib.pyplot import MultipleLocator
from matplotlib.legend_handler import HandlerPathCollection

def Is_exist(car_id, id_set):
    if car_id in id_set:
        return True
    else:
        return False

#id_n是车子标号，另一个是车子品质标号
def Calc_trust(id_n, id_q):
    t_sum = 0.0
    l = len(id_q)
    for i in id_q:
        t_sum += id_n[int(i)]
    t = t_sum / l
    return float(t)

def Get_dic():
    x = [i for i in range(0, 1000)]
    t = dict((key, 0) for key in x)
    return t

def Res_Write(filepath, msg):
    f = open(filepath, 'a')
    f.write(msg)
    f.close()

#carid, x, y, sid, x, y, min_dis
def Solve():
    sensor = Get_dic()
    #sort_sensor = []
    for i in range(2, 3):
        filename = str(i) + '.txt'
        with open('F:/Sensor Data/' + str(i) + '.txt', 'r') as f:
            for j in f.readlines():
                info = j.split(';')
                info[6] = info[6].strip()
                
                sensor_id = int(info[3])
                dis = float(info[6])

                if dis <= 60.0:
                    sensor[sensor_id] += 1    
                    
                sort_sensor = sorted(sensor.items(), key = lambda x:x[1], reverse= True)

        print("第" + str(i) + '个周期成功')
        
        msg = ''
        for i in range(0, 1000):
            s_id = sort_sensor[i][0]
            s_cnt = sort_sensor[i][1]
            msg = msg + str(s_id) + ';' + str(s_cnt) + '\n'
        
        filepath = 'F:/Find Data/' + filename
        Res_Write(filepath, msg)

def New_sensordata():
    #sort_sensor = []
    for i in range(1, 91):
        msg = ''
        filename = str(i) + '.txt'
        with open('/Users/guojiawei/Desktop/Sensor Data/' + str(i) + '.txt', 'r') as f:
            for j in f.readlines():
                info = j.split(';')
                info[6] = info[6].strip()
                
                car_id = int(info[0])
                sensor_id = int(info[3])
                dis = float(info[6])

                if dis > 60.0:   
                    continue

                msg += str(sensor_id) + ';' + str(car_id) + '\n'

        print("第" + str(i) + '个周期成功')
        
        filepath = '/Users/guojiawei/Desktop/nSensor Data/' + filename
        Res_Write(filepath, msg)

def Read_sensor(filepath):
    sensor = {}
    with open(filepath, 'r') as f:
        for x in f.readlines():
            info = x.split(';')
            info[1] = info[1].strip()
            s_id = int(info[0])
            s_cnt = int(info[1])
            d = {s_id: s_cnt}
            sensor.update(d)
    return sensor

#Find Data是根据报告有效次数最多的节点的排序, 1是新方法，2是旧方法
def Cover_sensor_2(cycle):
    filepath = 'F:/Find Data/' + str(cycle) + '.txt'
    sensor = Read_sensor(filepath)
    
    cover_id = [0 for i in range(0, 1001)]
    i = 1
    for key, value in sensor.items():
        cover_id[int(key)] = 1
        i += 1
        if(i == 501):
            break
    return cover_id

def Cover_sensor_1(cycle, s_id):
    filepath = 'F:/Find Data/' + str(cycle) + '.txt'
    sensor = Read_sensor(filepath)
    i = 1
    for key, value in sensor.items():
        if s_id[int(key)] == 0:
            s_id[int(key)] = 1
            i += 1
        if(i == 501):
            break
    return s_id

def Get_record():
    t = [list() for i in range(320)]
    for i in range(320):
        t[i] = [ [0 for i in range(2)] for j in range(1001)]
    return t

def Res2(x3, x6):
    print('Start: Res2')
    t = [i for i in range(41)]

    MAX = -1
    MIN = 1

    max_v = -1
    min_v = 1
    sx = []
    for i in range(1, 41):
        d = x3[i] - x6[i]
        s = x3[i]/x6[i]
        sx.append(s)
        if d > 0 and d < MIN:
            MIN = d
        if d > MAX:
            MAX = d
        if s > max_v:
            max_v = s
        if s < min_v and s > 1:
            min_v = s

    sx.sort()
    for i in range(0, 10):
        print(sx[i])
    print(sx[39])
    print("综合信任的最大差值是：" + str(MAX))
    print("综合信任的最小差值是：" + str(MIN))
    
    print("综合信任的最大提升是：" + str(max_v))
    print("综合信任的最小提升是：" + str(min_v))

    #plt.yticks(np.arange(0, 1.2, 0.2))
    plt.title('Comparison of Trust difference')
    plt.xlabel('Time')
    plt.ylabel('Trust difference')
    
    plt.plot(t, x3, 'y^-', linewidth = 1, markersize = 2.0, label = 'new Strategy $\overline{T_{diff}}$')
    plt.plot(t, x6, 'k^-', linewidth = 1, markersize = 2.0, label = 'old Strategy $\overline{T_{diff}}$')

    x_major_locator = MultipleLocator(8)
    y_major_locator = MultipleLocator(0.2)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.xlim(0, 40)
    plt.ylim(0, 1)
    
    plt.legend(loc='lower right', framealpha = 0.5, fontsize = 'small') 
    plt.savefig('diff_Rec.png')
    print('Diff job done!')

def Res3(x1, x2): #速度的比较
    tx = [i for i in range(1,41)]
    t = 1
    sum1 = 0.0
    sum2 = 0.0
    v1 = []
    v2 = []
    v = []
    maxx = -1
    minn = 1
    p1 = 0
    p2 = 0
    for i in range(1, 41):
        a = x1[i] - x2[i]
        if a > maxx:
            maxx = a
            p1 = i
        if a < minn and a > 0:
            minn = a
            p2 = i
        sum1 = x1[i] - x1[i - 1]
        sum2 = x2[i] - x2[i - 1]
        v1.append(sum1 / t)
        v2.append(sum2 / t)
        v.append((sum1/t) - (sum2/t))
    
    print(maxx)
    print(minn)
    print(x1[p1]/x2[p1] -1)
    print(x1[p2]/x2[p2] -1)
    plt.title('Verification rate difference')
    plt.xlabel('Time')
    plt.ylabel('Verification rate difference')
        
    plt.plot(tx, v1, 'y^-', linewidth = 1, markersize = 2.0, label = 'new Strategy $\overline{V}$')
    plt.plot(tx, v2, 'k^-', linewidth = 1, markersize = 2.0, label = 'old Strategy $\overline{V}$')
    plt.plot(tx, v, 'g^-', linewidth = 1, markersize = 2.0, label = 'The difference $\overline{V}$')

    x_major_locator = MultipleLocator(8)
    y_major_locator = MultipleLocator(0.1)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.xlim(0, 40)
    plt.ylim(0, 1)
       
    plt.legend(loc='lower right', framealpha = 0.5, fontsize = 'small') 
    plt.savefig('v_com.png')
