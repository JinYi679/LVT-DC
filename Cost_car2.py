import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from Distance import distance
from matplotlib.pyplot import MultipleLocator
from matplotlib.legend_handler import HandlerPathCollection
import math
import cover

def Get_sensor():
    sx = []
    sy = []
    f = open("sensor_location.txt", 'r')
    for i in f.readlines():
        a = i.split(';')
        a[1] = a[1].strip()
        sx.append(float(a[0]))
        sy.append(float(a[1]))
    f.close()
    return sx, sy

def Get_dis(cycle):
    car_dis = [[] for i in range(316)]
    for i in range(316):
        car_dis[i] = [0 for i in range(1005)]
    with open('F:/Sensor Data/' + str(cycle) + '.txt', 'r') as f:
        for j in f.readlines():
            info = j.split(';')
            info[6] = info[6].strip()        
            car_id = int(info[0])
            sensor_id = int(info[3])
            dis = float(info[6])

            if dis < 60.0:
                car_dis[car_id][sensor_id] = dis

    return car_dis

def Get_val_sensor(cycle):
    filepath = 'F:/Find Data/' + str(cycle) + '.txt'
    val_sensor = [0 for i in range(1002)]
    with open(filepath, 'r') as f:
        for x in f.readlines():
            info = x.split(';')
            info[1] = info[1].strip()
            s_id = int(info[0])
            cnt = float(info[1])
            if cnt != 0:
                if math.log(float(cnt)) != 0:
                    val_sensor[s_id] = 1.0 / math.log(float(cnt))
                else:
                    val_sensor[s_id] = 0
            else:
                val_sensor[s_id] = 0
    return val_sensor

def Get_T_com(cycle):
    T_com = []
    filepath = 'F:/Tcom1/' + str(cycle) + '.txt'
    with open(filepath, 'r') as f:
        for x in f.readlines():
            info = x.split(';') #分隔符出现在最后会多出一个空格
            info[0] = info[0].strip()
            T_com.append(float(info[0]))
    return T_com

def Cover1(cycle, rem_id, vis_car):
    filepath = 'F:/Find Data/' + str(cycle) + '.txt'
    sensor = cover.Read_sensor(filepath)
    k = 0
    for key in sensor:
        if rem_id[int(key)] == 0:
            rem_id[int(key)] = 1
            k += 1
        if k == 15:
            break
    return rem_id

def Get_cover(cycle, rem_id):
    base = 0.6
    T_com = Get_T_com(cycle) #获取车辆在每个周期的综合信任
    vis_car = cover.Get_car_cover(base, T_com) #获取基础车辆
    Cover1(cycle, rem_id, vis_car)
    
    return  rem_id, vis_car, T_com

def Get_carval(cycle, sx, sy, vis_car, need_dis, rem_id):
    filepath = 'F:/Cover Data/' + str(cycle) + '.txt'
    car_id = 0
    car_val = [0 for i in range(316)]
    car_dis = [0 for i in range(316)]
    sensor_val = Get_val_sensor(cycle)
    cover = [0 for i in range(1002)]
    rep = [[] for i in range(316)]
    with open(filepath, 'r') as f:
        for x in f.readlines():
            car_id += 1
            if vis_car[car_id] == 0:
                continue
            info = x.split(';')
            if info[0] == '\n':
                continue
            
            sid = int(info[0])
            prex = sx[sid] #保存前一个点的传感器坐标
            prey = sy[sid]
            
            l = len(info)
            info[l-1] = info[l-1].strip()
            for i in range(l-1):
                s_id = int(info[i])
                if rem_id[s_id] == 1:
                    car_val[int(car_id)] += 0
                    cover[s_id] = 0
                else:
                    car_val[int(car_id)] += sensor_val[s_id]
                    cover[s_id] = 1
                car_dis[int(car_id)] += distance(sx[s_id], sy[s_id], prex, prey)
                prex = sx[s_id]
                prey = sy[s_id]
                #car_val[int(car_id)] += sensor_val[s_id]
                rep[int(car_id)].append(s_id)
    return car_val, car_dis, cover, rep

def Calc_sum():
    sx, sy = Get_sensor()
    rem_id = [0 for i in range(1005)] 
    res = []
    for t in range(1, 41):
        #if t % 10 == 1:
        rem_id = [0 for i in range(1005)] 
        cost = [0 for i in range(316)]
        v = [0 for i in range(316)]
        cc = [0 for i in range(316)]
        cv = [0 for i in range(316)] 
        rem_id, vis_car, T_com = Get_cover(t, rem_id) #
        need_dis = Get_dis(t)
        car_val, car_dis, cover, rep = Get_carval(t, sx, sy, vis_car, need_dis, rem_id)

        for i in range(1002):
            if rem_id[i] == 1:
                cover[i] = 0
        #在所有车辆成本中挑取价值率最高的
        a1 = 0.8
        a2 = 0.1
        a3 = 0.1
        #print(car_dis)
        for i in range(1, 316): #8*70 min(200.0 / 560.0 * float(car_dis[i]), 200)
            v[i] = car_val[i]
            #cost[i] = a1 * min(float(car_val[i]), 80.0) + a2 * 80 * float(car_dis[i]) / 4800.0 + a3 * 80 * float(T_com[i])
            #cost[i] = 70 * float(car_dis[i]) / 4800.0
            cost[i] = a1 * min(float(car_val[i]), 50.0) + a2 * min(80.0 * (float(car_dis[i]) / 4800.0), 50) + a3 * 150 * float(T_com[i])
        x1 = max(cost)
        x2 = max(v)
        for i in range(1, 316):
            cc[i] = 1.0 - (cost[i] / x1)
            cv[i] = cost[i] / x2
        w1 = 0.5
        w2 = 0.5
        sum = 0.0
        vis = [0 for i in range(316)]
        cnt = 0
        while any(cover) == True:
            p = -1
            maxc = -1
            for i in range(316):
                if w1 * cv[i] + w2 * cc[i] > maxc and vis[i] == 0 and vis_car[i] == 1:
                    p = i
                    maxc = w1 * cv[i] + w2 * cc[i]
            sum += cost[p]
            vis[p] = 1
            l = len(rep[p])
            for i in range(l):
                s_id = rep[p][i]
                cover[s_id] = 0
            cnt += 1
        res.append(sum)
        #print(cnt)
    return res

print(Calc_sum())