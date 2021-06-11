import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from Distance import distance
from cover import Cover1
from cover import Cover2
from cover import Get_record
from lab4 import Res2
from lab4 import Res3
from Write_Trust_res import Write_T_com_result1
from Write_Trust_res import Write_T_com_result2
from matplotlib.pyplot import MultipleLocator
from matplotlib.legend_handler import HandlerPathCollection
import Write_Trust_res

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
    sum_id = [-1 for i in range(0, 380)]
    sum_id[0] = 0
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
    x = [i for i in range(0, 380)]
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
    need_dis = 120.0
    
    cnt_car = Get_cnt_car()
    
    cover_id = [0 for i in range(0, 1001)]
    T_act = [0.5 for i in range(380)]
    T_rec = [0.5 for i in range(380)]
    T_com = [0.5 for i in range(380)]
    r1 = []
    r2 = []
    car_record = Get_record() #获取车子报告节点成功与失败的次数
    good_match = [[] for i in range(380)] #推荐信任的次数的存储
    bad_match = [[] for i in range(380)]
    for i in range(1, 41):
        #c = [0 for i in range(317)]
        #file_id = str(int(f_id) + 1)
        cover_id = Cover1(i, cover_id) #获取可以收集覆盖的节点
        with open('F:/Sensor Data/' + str(i) + '.txt', 'r') as f:
            for j in f.readlines():
                info = j.split(';')
                info[6] = info[6].strip()
                
                car_id = int(info[0])
                sensor_id = int(info[3])
                dis = float(info[6])

                if dis > need_dis:
                    continue
                
                car_id += 1
               
                if cover_id[sensor_id] > 0:
                    if sum_id[car_id] == 0:
                        
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
            T_rec = Rec_trust(car_record, T_act, T_rec, good_match, bad_match)
        else:
            T_rec = Rec_trust(car_record, T_com, T_rec, good_match, bad_match)   
            
        T_com = Sum_trust(T_act, T_rec, T_com)
        
        for j in range(len(cover_id)):
            if cover_id[j] > 0:
                cover_id[j] -= 1
        
        #Write_T_com_result1(T_com, i) #写入结果文件
        t_abnormal_aver = Calc_trust(T_com, abnormal_id)
        t_normal_aver = Calc_trust(T_com, normal_id)
        diff = t_normal_aver - t_abnormal_aver
        
        t1 = Calc_trust(T_rec, abnormal_id)
        t2 = Calc_trust(T_rec, normal_id)
        print(t1, t2)
        r1.append(t1)
        r2.append(t2)
        
        

        print("第1个办法第" + str(i) + '个周期成功')
       
        T_ab_aver.append(t_abnormal_aver)
        T_nor_aver.append(t_normal_aver)
        Diff.append(diff)
    print(r1)
    print(r2)
    return T_ab_aver, T_nor_aver, Diff

#传感器编号是0-999
#carid, x, y, sid, x, y, min_dis
def Solve2():
    sum_id, normal_id, abnormal_id = Get_car_id()
    T_ab_aver = [0.5]
    T_nor_aver = [0.5]
    Diff = [0]
    need_dis = 120.0
    
    cnt_car = Get_cnt_car()
    cover_id = [0 for i in range(0, 1001)]
    
    r1 = []
    r2 = []
    T_act = [0.5 for i in range(380)]
    T_rec = [0.5 for i in range(380)]
    T_com = [0.5 for i in range(380)]
    car_record = Get_record() #获取车子报告节点成功与失败的次数
    good_match = [[] for i in range(380)] #推荐信任的次数的存储
    bad_match = [[] for i in range(380)]
    
    for i in range(1, 41):
        #file_id = str(int(f_id) + 1)
        cover_id = Cover2(i) #获取可以收集覆盖的节点
        with open('F:/Sensor Data/' + str(i) + '.txt', 'r') as f:
            for j in f.readlines():
                info = j.split(';')
                info[6] = info[6].strip()
                
                car_id = int(info[0])
                sensor_id = int(info[3])
                dis = float(info[6])

                if dis > need_dis:
                    continue

                car_id += 1
                
                if cover_id[sensor_id] > 0:
                    if sum_id[car_id] == 0:
                        
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
            T_rec = Rec_trust(car_record, T_act, T_rec, good_match, bad_match) #引用传递
        else:
            T_rec = Rec_trust(car_record, T_com, T_rec, good_match, bad_match)   
                 
        T_com = Sum_trust(T_act, T_rec, T_com)
        
        t_abnormal_aver = Calc_trust(T_com, abnormal_id)
        t_normal_aver = Calc_trust(T_com, normal_id)
        diff = t_normal_aver - t_abnormal_aver

        print("第2个办法第" + str(i) + '个周期成功')
        
        
        t1 = Calc_trust(T_rec, abnormal_id)
        t2 = Calc_trust(T_rec, normal_id)
        print(t1, t2)
        r1.append(t1)
        r2.append(t2)
        
        
        #Write_T_com_result2(T_com, i) #写入结果文件
        T_ab_aver.append(t_abnormal_aver)
        T_nor_aver.append(t_normal_aver)
        Diff.append(diff)
    print(r1)
    print(r2)
    return T_ab_aver, T_nor_aver, Diff

#Positive, Recommendation, Probability, Comprehensive
def Result(c):
    x1, x2, x3 = Solve()
    t = [i for i in range(41)]
    #Write_Trust_result.Write_T_com1(x1, x2, x3)
    #liens = plt.plot(t, x1, t, x2, t, x3)
    #plt.yticks(np.arange(0, 1.2, 0.2))
    plt.title('Comparison of Recommendation trust')
    plt.xlabel('Time')
    plt.ylabel('Recommendation Trust')
    
    plt.plot(t, x1, 'y^-', linewidth = 1, markersize = 2.0, label = 'Our Strategy $\overline{T_{abn}}$')
    plt.plot(t, x2, 'go-', linewidth = 1, markersize = 2.0, label = 'Our Strategy $\overline{T_{nor}}$')
    #plt.plot(t, x3, 'r*-', linewidth = 1, markersize = 2.0)
    
    x4, x5, x6 = Solve2()
    #Write_Trust_result.Write_T_com2(x4, x5, x6)
    
    print(x1)
    print(x4)
    print('#########')
    print(x3)
    print(x6)
    print("##")
    print(x2)
    print(x5)
    
    
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
    plt.ylim(0., 1)
    
    plt.legend(loc=0 , framealpha = 0.5, fontsize = 'xx-large') 
    #plt.savefig(c + '.png')
    plt.show()


    return x3, x6

def Sum_trust(T_act, T_rec, T_com):
    for i in range(1, 380):
        T_com[i] = (0.8 * T_act[i] + 0.2 * T_rec[i])
    
    return T_com

def Calc_act_trust(cnt_s, cnt_f):

    a = cnt_s + 1
    b = cnt_s + 1.5 * cnt_f + 2
    t_act = a / b
    return t_act

def Act_trust(cnt_car, T_act):
    #T_act = [0.5 for i in range(380)]
    
    for i in range(1, 380):
        T_act[i] = Calc_act_trust(cnt_car[i][0], cnt_car[i][1]) #引用传递，直接修改
    
    return T_act

def Rec_trust(data, T_com, T_rec, good_match, bad_match):
    car_num = 380
    sensor_num = 1001
    #good_match = [[] for i in range(car_num)]
    #bad_match = [[] for i in range(car_num)]
    z = [[] for i in range(car_num)]
    recom = [[] for i in range(car_num)]
    for i in range(car_num):
        good_match[i] = [0 for j in range(car_num)]
        bad_match[i] = [0 for j in range(car_num)]
        recom[i] = [0 for j in range(car_num)]
        z[i] = [0 for j in range(car_num)]
    for i in range(car_num):
        for j in range(1, car_num):
            good = 0
            bad = 0
            if T_com[j] <= T_com[i] or i == j or T_com[j] < 0.5:
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
            #b = good / (good + bad + 1)
            #u = 1 / (good + bad + 1)
            b = good + 1.0
            u = good + bad + 2.0
            #recom[i][j] = recom[j][i] = (2 * b + u) / 2
            recom[i][j] = recom[j][i] = float(b) / float(u)
            if(good != 0 or bad != 0):
                z[i][j] = z[j][i] = 1
    #T_rec = [0.5 for i in range(380)]
    for i in range(car_num):
        sum1 = 0
        sum2 = 0
        for j in range(car_num):
            sum1 += z[i][j] * recom[i][j] * (T_com[j]**2)
            sum2 += z[i][j] * T_com[j]
        if(sum2 != 0):
            T_rec[i] = sum1 / sum2
        else:
            continue

    return T_rec

x1, x2 = Result('T_rec_new')
#Res2(x1, x2)
