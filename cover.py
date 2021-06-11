import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from Distance import distance 
from matplotlib.pyplot import MultipleLocator
from matplotlib.legend_handler import HandlerPathCollection

def Read_sensor(filepath):
    sensor = []
    with open(filepath, 'r') as f:
        for x in f.readlines():
            info = x.split(';')
            info[1] = info[1].strip()
            s_id = int(info[0])
            sensor.append(s_id)
    return sensor

def Read_car1(filepath, vis_car, cover_id):
    car_id = 0
    v = [0 for i in range(1002)]
    with open(filepath, 'r') as f:
        for x in f.readlines():
            car_id += 1
            if vis_car[car_id] == 0:
                continue
            info = x.split(';')
            if info[0] == '\n':
                continue
            l = len(info)
            
            info[l-1] = info[l-1].strip()
            for i in range(l-1):
                v[int(info[i])] += 1
                
    sum = 0
    for i in range(len(v)):
        if v[i] >= 3 and cover_id[i] == 0:
            cover_id[i] = 2
    
    for i in range(0, 1001):
        if cover_id[i] == 1 or cover_id[i] == 2:
            sum += 1

    #print(sum)
    return cover_id, sum

def Read_car2(filepath, vis_car):
    cover_id = [0 for i in range(1, 1002)]
    car_id = 0
    v = [0 for i in range(1002)]
    with open(filepath, 'r') as f:
        for x in f.readlines():
            car_id += 1
            if vis_car[car_id] == 0:
                continue
            info = x.split(';')
            if info[0] == '\n':
                continue
            l = len(info)
            
            info[l-1] = info[l-1].strip()
            for i in range(l-1):
                v[int(info[i])] += 1
                
    sum = 0
    for i in range(len(v)):
        if v[i] >= 3:
            cover_id[i] = 1

    for i in range(0, 1001):
        if cover_id[i] == 1:
            sum += 1

    return cover_id, sum

#Find Data是根据报告有效次数最多的节点的排序, 1是新方法，2是旧方法
def Cover1(cycle, cover_id):
    filepath = 'F:/Find Data/' + str(cycle) + '.txt'
    sensor = Read_sensor(filepath)
    k = 0
    u = [0, 56, 56, 59, 60, 62, 55, 49, 51, 50, 48, 54, 49, 48, 43, 44, 47, 54, 50, 47, 42, 44, 46, 49, 43, 43, 42, 45, 43, 49, 40, 44, 42, 43, 41, 46, 40, 47, 42, 42, 39]
    #u = random.randint(38, 45)
    for i in range(len(sensor)):
        if cover_id[int(sensor[i])] == 0:
            cover_id[int(sensor[i])] = 6
            k += 1
        if  k == u[int(cycle)]:
            break
    cnt = 0
    for i in range(len(cover_id)):
        if cover_id[i] > 0:
            cnt += 1
    print(cnt)
    return cover_id

def Cover2(cycle):
    cover_id = [0 for i in range(1002)]
    filepath = 'F:/Find Data/' + str(cycle) + '.txt'
    sensor = Read_sensor(filepath) #传感器按报告顺序从大到小排序
    
    k = 0
    u = [0, 56, 51, 48, 48, 47, 50, 49, 49, 47, 46, 47, 46, 46, 45, 46, 46, 43, 43, 46, 45, 43, 44, 43, 44, 44, 44, 42, 44, 43, 42, 42, 42, 41, 42, 42, 41, 41, 42, 41, 41]
    for key in sensor:
        if cover_id[int(key)] == 0:
            cover_id[int(key)] = 1
            k += 1
        if k == u[int(cycle)]:
            break
    
    cnt = 0
    for i in range(len(cover_id)):
        if cover_id[i] > 0:
            cnt += 1
    print(cnt)
    #print(sum)
    
    
    return cover_id

def Get_car_cover(base, T_com):
    
    cnt = 0
    vis_car = [0 for i in range(350)]
    for i in range(1, 316):
        if T_com[i] > base:
            vis_car[i] = 1
            cnt += 1
    #print("sum of car is" + str(cnt))
    return vis_car

def Get_record():
    t = [list() for i in range(400)]
    for i in range(400):
        t[i] = [ [0 for i in range(2)] for j in range(1001)]
    return t