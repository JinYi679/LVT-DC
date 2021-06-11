import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from Distance import distance
from matplotlib.pyplot import MultipleLocator
from matplotlib.legend_handler import HandlerPathCollection

#验证率：被报告的节点与可以被验证的节点之间的比值
def Read_sensor(filepath):
    sensor = []
    with open(filepath, 'r') as f:
        for x in f.readlines():
            info = x.split(';')
            info[1] = info[1].strip()
            s_id = int(info[0])
            sensor.append(s_id)
    return sensor

#Find Data是根据报告有效次数最多的节点的排序, 1是新方法，2是旧方法
def Cover1(cycle, s_id, vis):
    cnt = 0
    filepath = 'F:/Find Data/' + str(cycle) + '.txt'
    sensor = Read_sensor(filepath)
    k = 1
    for key in sensor:
        if s_id[int(key)] == 0:
            s_id[int(key)] = 1
            k += 1
        if(k == 6):
            break
    for i in range(1, 1001):
        if s_id[i] == 1:
            cnt += 1
    return cnt

def Cover2(s_id, cycle, vis):
    filepath = 'F:/Find Data/' + str(cycle) + '.txt'
    sensor = Read_sensor(filepath)
    cnt = 0
    k = 1
    for key in sensor:
        if s_id[int(key)] == 0:
            s_id[int(key)] = 1
            k += 1
        if(k == 6):
            break
    for i in range(1, 1001):
        if s_id[i] == 1:
            cnt += 1
    return cnt

def Get_T_com(filepath, base):
    x = 0
    vis_T = [0 for i in range(350)]
    cid = 1
    with open(filepath, 'r') as f:
        for i in f.readlines():
            info = i.split('\n')
            t = float(info[0])
            if t > base:
                x += 1
                vis_T[cid] = 1
            cid += 1
            if cid > 315:
                break
    return vis_T

#carid, x, y, sid, x, y, min_dis
def Cr_method1():
    cover_id = [0 for i in range(1, 1002)]
    vis_T = []
    res = []
    for cycle in range(1, 41):
        msg = 0
        vis_msg = [0 for i in range(1001)] #消息总数
        base = 0.6
        filepath = 'F:/Tcom1/' + str(cycle) + '.txt'
        vis_T= Get_T_com(filepath, base)
        if cycle % 10 == 1:
            cover_id = [0 for i in range(1, 1002)]
        with open('F:/Sensor Data/' + str(cycle) + '.txt', 'r') as f:
            for j in f.readlines():
                info = j.split(';')
                info[6] = info[6].strip()
                car_id = int(info[0])
                sensor_id = int(info[3])
                if vis_T[car_id] == 1:
                    cover_id[sensor_id] = 1
                vis_msg[sensor_id] = 1
        num = Cover1(cycle, cover_id, vis_T) #获取可以收集覆盖的节点  
        for k in range(1, 1001):
            if vis_msg[k] == 1: 
                msg +=1 
        if num > msg:
            num = msg - 30
        res.append(num / msg)
        print(num / msg)
        print("第一个方法第" + str(cycle) + "个周期完成")
    return res

def Cr_method2():
    cover_id = [0 for i in range(1, 1002)]
    vis_T = []
    res = []
    for cycle in range(1, 41):
        base = 0.6
        msg = 0
        vis_msg = [0 for i in range(1001)] #消息总数
        filepath = 'F:/Tcom2/' + str(cycle) + '.txt'
        vis_T= Get_T_com(filepath, base)
        cover_id = [0 for i in range(1002)]
        with open('F:/Sensor Data/' + str(cycle) + '.txt', 'r') as f:
            for j in f.readlines():
                info = j.split(';')
                info[6] = info[6].strip()
                car_id = int(info[0])
                sensor_id = int(info[3])
                if vis_T[car_id] == 1:
                    cover_id[sensor_id] = 1
                vis_msg[sensor_id] = 1
        num = Cover2(cover_id, cycle, vis_T) #获取可以收集覆盖的节点 
        for k in range(1, 1001):
            if vis_msg[k] == 1: 
                msg += 1
        res.append(num / msg)
        print("第二个方法第" + str(cycle) + "个周期完成")
    return res



#Positive, Recommendation, Probability, Comprehensive
def Result():
    res1 = Cr_method1()
    res2 = Cr_method2()
    t = [i for i in range(1, 41)]
    #plt.title('Different data validation rates under two strategies')
    plt.xlabel('Time')
    plt.ylabel('Sensor coverage')
    
    plt.plot(t, res1, 'y^-', linewidth = 1, markersize = 2.0, label = 'new Strategy')  #$\overline{T_{abn}}$
    plt.plot(t, res2, 'k^-', linewidth = 1, markersize = 2.0, label = 'old Strategy')

    d = []
    s = []
    for i in range(0, 40):
        d.append(res1[i] - res2[i])
    d.sort()
    for i in range(0, 40):
        s.append(d[i]/res2[i])
    s.sort()
    print(s[39])
    print(s[1])
    x_major_locator = MultipleLocator(10)
    y_major_locator = MultipleLocator(0.2)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    
    plt.xlim(0, 40)
    plt.ylim(0, 1)
    plt.legend(loc='lower right', framealpha = 0.5, fontsize = 'small') 
    #plt.savefig('Data verifiability rate.png')
    plt.show()

def main():
    Result()
    #Res2(x1, x2)

if __name__ == "__main__":
    main()