import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from Distance import distance
from cover import Cover1
from cover import Cover2
from cover import Get_car_cover
from cover import Get_record

from Write_Trust_res import Write_T_com_result1
from Write_Trust_res import Write_T_com_result2
from matplotlib.pyplot import MultipleLocator
from matplotlib.legend_handler import HandlerPathCollection

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
    filepath = 'F:/Git/normal_id.txt'
    sum_id, good = Get_file(filepath, sum_id, 0)
    
    filepath = 'F:/Git/abnormal_id.txt'
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
def Solve():
    sum_id, normal_id, abnormal_id = Get_car_id()
    T_ab_aver = [0.5]
    T_nor_aver = [0.5]
    Diff = [0]
    need_dis = 10000000.0
    cnt_car = Get_cnt_car()
    cover_id = [0 for i in range(0, 1001)]

    T_act = [0.5 for i in range(316)]
    T_rec = [0.5 for i in range(316)]
    T_com = [0.5 for i in range(316)]
    
    car_record = Get_record() #获取车子报告节点成功与失败的次数
    vis_car = [0 for i in range(316)]

    r1 = []
    r2 = []
    for i in range(1, 41):
        #file_id = str(int(f_id) + 1)
        vis_car = Get_car_cover(0.85, T_com)#获取可以收集覆盖的节点
        #cover_id = [0 for i in range(1001)]
        cover_id = Cover1(i, cover_id, vis_car)
        with open('F:/Sensor Data/' + str(i) + '.txt', 'r') as f:
            for j in f.readlines():
                info = j.split(';')
                info[6] = info[6].strip()
                
                car_id = int(info[0])
                sensor_id = int(info[3])
                dis = float(info[6])

                if dis > need_dis or car_id == 0:
                    continue
                if cover_id[sensor_id] == 1:
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
        
        if i == 1:
            T_rec = Rec_trust(car_record, T_act, T_rec)
        else:
            T_rec = Rec_trust(car_record, T_com, T_rec)                  
        
        T_com = Sum_trust(T_act, T_rec, T_com)
        
        t1 = Calc_trust(T_rec, abnormal_id)
        t2 = Calc_trust(T_rec, normal_id)
        print(t1, t2)
        r1.append(t1)
        r2.append(t2)

        #Write_T_com_result1(T_com, i) #写入结果文件
        t_abnormal_aver = Calc_trust(T_com, abnormal_id)
        t_normal_aver = Calc_trust(T_com, normal_id)
        diff = t_normal_aver - t_abnormal_aver

        print("第1个办法第" + str(i) + '个周期成功')
       
        T_ab_aver.append(t_abnormal_aver)
        T_nor_aver.append(t_normal_aver)
        Diff.append(diff)
        
    return T_ab_aver, T_nor_aver, Diff, r1, r2

#传感器编号是0-999
#carid, x, y, sid, x, y, min_dis
def Solve2():
    sum_id, normal_id, abnormal_id = Get_car_id()
    T_ab_aver = [0.5]
    T_nor_aver = [0.5]
    Diff = [0]
    need_dis = 10000000.0
    cnt_car = Get_cnt_car()
    cover_id = [0 for i in range(0, 1001)]

    T_act = [0.5 for i in range(316)]
    T_rec = [0.5 for i in range(316)]
    T_com = [0.5 for i in range(316)]
    vis_car = [0 for i in range(350)]
    r1 = []
    r2 = []
    car_record = Get_record() #获取车子报告节点成功与失败的次数
    for i in range(1, 41):
        #file_id = str(int(f_id) + 1)
        vis_car = Get_car_cover(0.85, T_com)#获取可以收集覆盖的节点
        cover_id = Cover2(i, vis_car)
        with open('F:/Sensor Data/' + str(i) + '.txt', 'r') as f:
            for j in f.readlines():
                info = j.split(';')
                info[6] = info[6].strip()
                
                car_id = int(info[0])
                sensor_id = int(info[3])
                dis = float(info[6])

                if dis > need_dis or car_id == 0:
                    continue
                
                if cover_id[sensor_id] == 1:
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
        if i == 1:
            T_rec = Rec_trust(car_record, T_act, T_rec)
        else:
            T_rec = Rec_trust(car_record, T_com, T_rec)                 
        T_com = Sum_trust(T_act, T_rec, T_com)
        
        t1 = Calc_trust(T_rec, abnormal_id)
        t2 = Calc_trust(T_rec, normal_id)
        print(t1, t2)
        r1.append(t1)
        r2.append(t2)

        t_abnormal_aver = Calc_trust(T_com, abnormal_id)
        t_normal_aver = Calc_trust(T_com, normal_id)
        diff = t_normal_aver - t_abnormal_aver

        print("第2个办法第" + str(i) + '个周期成功')
        
        #Write_T_com_result2(T_com, i) #写入结果文件
        T_ab_aver.append(t_abnormal_aver)
        T_nor_aver.append(t_normal_aver)
        Diff.append(diff)
        
    return T_ab_aver, T_nor_aver, Diff, r1, r2

#Positive, Recommendation, Probability, Comprehensive
def Result(c):
    x1, x2, x3, r1, r2 = Solve()
    t = [i for i in range(41)]
    #liens = plt.plot(t, x1, t, x2, t, x3)
    #plt.yticks(np.arange(0, 1.2, 0.2))
    
    plt.title('Comparison of Recommendation trust')
    plt.xlabel('Time')
    plt.ylabel('Recommendation Trust')
    
    plt.plot(t, x1, 'y^-', linewidth = 1, markersize = 2.0, label = 'new Strategy $\overline{T_{abn}}$')
    plt.plot(t, x2, 'go-', linewidth = 1, markersize = 2.0, label = 'new Strategy $\overline{T_{nor}}$')
    #plt.plot(t, x3, 'r*-', linewidth = 1, markersize = 2.0)
    print(x1)
    print(x2)
    print(x3)
    print('REC:############')
    print(r1)
    print(r2)
    
    x4, x5, x6, r1, r2 = Solve2()

    print(x4)
    print(x5)
    print(x6)
    print('REC:############')
    print(r1)
    print(r2)

    plt.plot(t, x4, 'k^-', linewidth = 1, markersize = 2.0, label = 'old Strategy $\overline{T_{abn}}$')
    plt.plot(t, x5, 'bo-', linewidth = 1, markersize = 2.0, label = 'old Strategy $\overline{T_{nor}}$')
    #plt.plot(t, x6, 'c*-', linewidth = 1, markersize = 2.0)

    x_major_locator = MultipleLocator(8)
    #把x轴的刻度间隔设置为1，并存在变量里
    y_major_locator = MultipleLocator(0.2)
    #把y轴的刻度间隔设置为10，并存在变量里
    ax = plt.gca()
    #ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)
    #把x轴的主刻度设置为1的倍数
    ax.yaxis.set_major_locator(y_major_locator)
    #把y轴的主刻度设置为10的倍数
    plt.xlim(0, 40)
    plt.ylim(0, 1)
    
    plt.legend(loc=0 , framealpha = 0.5, fontsize = 'small') 
    plt.savefig('new_rec.png')
    plt.show()
    

    return x3, x6

def f(x):
    
    return 4 * (x**2) - 4 * x + 1 


def Sum_trust(T_act, T_rec, T_com):
    for i in range(1, 316):
        T_com[i] = (0.8 * T_act[i] + 0.2 * T_rec[i])
    
    return T_com

def Calc_act_trust(cnt_s, cnt_f):
    s = cnt_s / (cnt_s + cnt_f + 1)
    f = 1 / (cnt_s + cnt_f + 1)
    t_act = (2.0 * s + f) / 2.0
    return t_act

'''
def Calc_act_trust(cnt_s, cnt_f):
    a = cnt_s + 1
    b = cnt_s + cnt_f + 2
    return a/b
'''

def Act_trust(cnt_car, T_act):
    #T_act = [0.5 for i in range(316)]
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
            if T_com[j] < 0.5:
                continue
            for k in range(sensor_num):
                si = data[i][k][0]
                sj = data[j][k][0]
                fi = data[i][k][1]
                fj = data[j][k][1]
                if sj != 0 or fj != 0:
                    good += si 
                    bad +=  fi
                else:
                    continue
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
            sum1 += z[i][j] * recom[i][j] * T_com[j] * f(T_com[j])
            sum2 += z[i][j] * T_com[j]
        if(sum2 != 0):
            T_rec[i] = sum1 / sum2
        else:
            T_rec[i] = 0.5

    return T_rec

def main():
    x1,x2 = Result('T_rec_new')
    #Res2(x1, x2)

if __name__ == "__main__":
    main()