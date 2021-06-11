import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from Distance import distance
from lab4 import Cover_sensor_1
from lab4 import Cover_sensor_2
from lab4 import Get_record
from matplotlib.pyplot import MultipleLocator
from matplotlib.legend_handler import HandlerPathCollection
from Write_Trust_result import Write_Diff_para

def Get_file(filepath, sum_id, flag):
    l = []
    if flag == 0:
        with open(filepath, 'r') as f:
            for i in f.readlines():
                x = i.strip()
                sum_id[int(x)] = 0
                l.append(int(x))
    else:
        with open(filepath, 'r') as f:
            for i in f.readlines():
                x = i.strip()
                sum_id[int(x)] = 1
                l.append(int(x))
    return sum_id, l

#0是好, 1是坏
def Get_car_id():
    sum_id = [-1 for i in range(0, 316)]
    good = []
    bad = []
    filepath = 'F:/Git/abnormal_id.txt'
    sum_id, good = Get_file(filepath, sum_id, 0)
    
    filepath = 'F:/Git/normal_id.txt'
    sum_id, bad = Get_file(filepath, sum_id, 1)

    return sum_id, good, bad

#id_n是车子标号
def Calc_trust(id_n, id_q): #id_q就是好车子坏车子的编号
    t_sum = 0.0
    l = len(id_q)
    for i in id_q:
        t_sum += id_n[int(i)]
    t = t_sum / l
    return float(t)

#0是成功, 1是失败 创建字典
def Get_cnt_car():
    x = [i for i in range(1, 316)]
    t = dict((key, [0, 0]) for key in x)
    return t

def Res_check(filepath, msg):
    f = open('res.txt', 'w')
    f.write(msg + '\n')
    f.close()

#传感器编号是0-999
#carid, x, y, sid, x, y, min_dis
def Solve(a, b, c):
    sum_id, normal_id, abnormal_id = Get_car_id()
    T_ab_aver = [0.5]
    T_nor_aver = [0.5]
    Diff = [0]
    need_dis = 60.0
    cnt_car = Get_cnt_car()
    
    cover_id = [0 for i in range(0, 1001)]
    T_act = [0.5 for i in range(316)]
    T_rec = [0.5 for i in range(316)]
    T_pro = [0.5 for i in range(316)]
    T_com = [0.5 for i in range(316)]
    car_record = Get_record() #获取车子报告节点成功与失败的次数
    
    for i in range(1, 41):
        cover_id = Cover_sensor_1(i, cover_id) #获取可以收集覆盖的节点
        with open('F:/Sensor Data/' + str(i) + '.txt', 'r') as f:
            for j in f.readlines():
                info = j.split(';')
                info[6] = info[6].strip()
                
                car_id = int(info[0])
                sensor_id = int(info[3])
                dis = float(info[6])

                if dis > need_dis:
                    continue
                
                if cover_id[car_id] == 1:
                    if sum_id[car_id] == 0:
                        set_prob = random.uniform(0.001, 0.003)
                        prob = random.random()
                        if prob <= set_prob:
                            cnt_car[car_id][1] += 1 #失败次数+1 
                            car_record[car_id][sensor_id][1] += 1     
                        else:
                            cnt_car[car_id][0] += 1 #成功次数+1
                            car_record[car_id][sensor_id][0] += 1  
                    
                    elif sum_id[car_id] == 1:
                        set_prob = random.uniform(0.7, 0.8)
                        prob = random.random()
                        if prob <= set_prob:
                            cnt_car[car_id][1] += 1 #失败次数+1
                            car_record[car_id][sensor_id][1] += 1  
                        else:
                            cnt_car[car_id][0] += 1 #成功次数+1
                            car_record[car_id][sensor_id][0] += 1  

        T_act = Act_trust(cnt_car, T_act)
        T_pro = Pro_trust(car_record, T_pro)
        T_rec = Rec_trust(car_record, T_com, T_rec)                
        T_com = Sum_trust(T_act, T_rec, T_pro, T_com, a, b, c)

        t_abnormal_aver = Calc_trust(T_com, abnormal_id)
        t_normal_aver = Calc_trust(T_com, normal_id)
        diff = t_normal_aver - t_abnormal_aver

        print("第2个办法第" + str(i) + '个周期成功')
       
        T_ab_aver.append(t_abnormal_aver)
        T_nor_aver.append(t_normal_aver)
        Diff.append(diff)
        
    return T_ab_aver, T_nor_aver, Diff

def Calc_Aver_T_com(T_com):
    sum = 0.0
    for i in T_com:
        sum += i
    l = len(T_com)
    res =sum / l
    return res

#Positive, Recommendation, Probability, Comprehensive
def Result():
    line_style = ['y^-', 'g^-', 'b^-', 'm^-', 'c^-', 'k^-']
    for i in range(6):
        if i == 0:
            a = 0.7
            b = 0.2
            c = 0.1
        elif i == 1:
            a = 0.7
            b = 0.1
            c = 0.2
        elif i == 2:
            a = 0.2
            b = 0.7
            c = 0.1
        elif i == 3:
            a = 0.2
            b = 0.1
            c = 0.7
        elif i == 4:
            a = 0.1
            b = 0.7
            c = 0.2
        elif i == 5:
            a = 0.1
            b = 0.2
            c = 0.7
        x1, x2, x3 = Solve(a, b, c)
        t = [i for i in range(41)]
        
        Write_Diff_para(x3, i)
        ida = str(a)
        idb = str(b)
        idc = str(c)
        #plt.plot(t, x3, line_style[i], linewidth = 1, markersize = 2.0, label = '$\overline{Tru_{com}}$=' + pid)
        plt.plot(t, x3, line_style[i], linewidth = 1, markersize = 2.0, label = '$\overline{W_{1}}$=' + ida + ' ' + '$\overline{W_{2}}$=' + idb + ' ' + '$\overline{W_{3}}$=' + idc)
        #plt.plot(t, x3, 'r*-', linewidth = 1, markersize = 2.0)     
        
    plt.title('Comprehensive trust difference')
    plt.xlabel('Time')
    plt.ylabel('The difference of comprehensive trust')

    x_major_locator = MultipleLocator(5)
    #把x轴的刻度间隔设置为1，并存在变量里
    y_major_locator = MultipleLocator(0.13)
    #把y轴的刻度间隔设置为10，并存在变量里
    ax = plt.gca()
    #ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)
    #把x轴的主刻度设置为1的倍数
    ax.yaxis.set_major_locator(y_major_locator)
    #把y轴的主刻度设置为10的倍数
    plt.xlim(0, 40)
    plt.ylim(0, 0.65)
    
    plt.legend(loc='best', framealpha = 0.5, fontsize = 'small') 
    plt.savefig('diff_par1.png')
    #plt.show()

def Sum_trust(T_act, T_rec, T_pro, T_com, a, b, c):
    for i in range(1, 316):
        T_com[i] = (a * T_act[i] + b * T_rec[i] + c * T_pro[i])
    
    return T_com

def Calc_act_trust(cnt_s, cnt_f):
    s = cnt_s / (cnt_s + cnt_f + 1)
    f = 1 / (cnt_s + cnt_f + 1)
    t_act = (2.0 * s + f) / 2.0
    return t_act

def Act_trust(cnt_car, T_act):
    T_act = [0.5 for i in range(316)]
    for i in range(1, 316):
        T_act[i] = Calc_act_trust(cnt_car[i][0], cnt_car[i][1])
    
    return T_act

def Rec_trust(data, T_com, T_rec):
    car_num = 316
    sensor_num = 1001
    good_match = [[] for i in range(car_num)]
    bad_match = [[] for i in range(car_num)]
    z = [[] for i in range(car_num)]
    recom = [[] for i in range(car_num)]
    for i in range(car_num):
        good_match[i] = [0 for j in range(car_num)]
        bad_match[i] = [0 for j in range(car_num)]
        recom[i] = [0 for j in range(car_num)]
        z[i] = [0 for j in range(car_num)]
    for i in range(car_num):
        for j in range(i + 1, car_num):
            good = 0
            bad = 0
            for k in range(sensor_num):
                si = data[i][k][0]
                sj = data[j][k][0]
                fi = data[i][k][1]
                fj = data[j][k][1]
                good += si * sj + fi * fj
                bad += si * fj + fi * sj
            good_match[i][j] = good_match[j][i] = good
            bad_match[i][j] = bad_match[j][i] = bad
            b = good / (good + bad + 1)
            u = 1 / (good + bad + 1)
            recom[i][j] = recom[j][i] = (2 * b + u) / 2
            if(good != 0 or bad != 0):
                z[i][j] = z[j][i] = 1
    #T_rec = [0.5 for i in range(316)]
    for i in range(car_num):
        sum1 = 0
        sum2 = 0
        for j in range(car_num):
            sum1 += z[i][j] * recom[i][j] * recom[i][j] #* T_com[j]
            sum2 += z[i][j] * recom[i][j]
        if(sum2 != 0):
            T_rec[i] = sum1 / sum2

    return T_rec

def Pro_trust(car_record, T_pro):
    for i in range(1, 316):
        cnt = 0.0
        sum_pro = 0.0
        for j in range(1, 1001):
            pro = 0.0
            if car_record[i][j][0] > 0 or car_record[i][j][1] > 0:
                cnt += 1
                alpha = car_record[i][j][0] + 1
                beta = car_record[i][j][1] + 1
                pro = (alpha/ (alpha + beta))
                sum_pro += pro
        if cnt == 0:
            cnt += 1
        T_pro[i] = sum_pro / cnt
        if T_pro[i] == 0:
            T_pro[i] = 0.5
    
    return T_pro

Result()