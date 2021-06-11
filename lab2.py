import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from Distance import distance 

def Read_file():
    file1 = '/Users/guojiawei/Desktop/Lab Data/sensor_location.txt'
    #file2 = '/Users/guojiawei/Desktop/Git/t.txt'
    df = pd.read_csv(file1, sep = ';')
    #print(df)
    return df

def Get_file(filepath):
    l = []
    with open(filepath, 'r') as f:
        for i in f.readlines():
            x = i.strip()
            l.append(x)
    return l

def Get_car_id():
    ab_id = []
    n_id = []
    filepath = '/Users/guojiawei/Desktop/Git/abnormal_id.txt'
    ab_id = Get_file(filepath)
    
    filepath = '/Users/guojiawei/Desktop/Git/normal_id.txt'
    n_id = Get_file(filepath)

    return ab_id, n_id

def text_save(filename, msg):#filename为写入CSV文件的路径，data为要写入数据列表.
    file_path = '/Users/guojiawei/Desktop/Sensor Data' + filename
    file = open(file_path, 'a')
    file.write(msg + '\n')
    file.close()
    #print("保存文件成功")

def Is_receive(x, y, sx, sy):
    find = False
    min_dis = 1000000.0
    s_id = 0
    for i in range(len(sx)):
        dis = distance(float(x), float(y), float(sx[i]), float(sy[i]))
        if dis <= 60.0 and dis < min_dis:
            find = True
            min_dis = dis
            s_id = i
        else:
            if dis < min_dis:
                min_dis = dis
                s_id = i
    return find, s_id, min_dis

def Is_exist(car_id, id_set):
    if car_id in id_set:
        return True
    else:
        return False

def Get_sensor():
    table_sensor = Read_file()
    sx = []
    sy = []
    for index, row in table_sensor.iterrows():
        sx.append(row['a'])
        sy.append(row['b'])
    return sx, sy

#id_n是车子标号，另一个是车子品质标号
def Calc_trust(id_n, id_q):
    t_sum = 0.0
    l = len(id_q)
    for i in id_q:
        t_sum += id_n[int(i)]
    t = t_sum / l
    return float(t)

#信任度 +-0.02
def Solve():
    abnormal_id, normal_id = Get_car_id()
    sx, sy = Get_sensor()
    car_trust = [0.5 for i in range(316)]
    T_ab_aver = [0.5]
    T_nor_aver = [0.5]
    Diff = [0]
    for i in range(1, 31):
        #file_id = str(int(f_id) + 1)
        filename = str(i) + '.txt'
        with open('/Users/guojiawei/Desktop/Lab Data/' + str(i) + '.txt', 'r') as f:
            for j in f.readlines():
                info = j.split(';')
                info[2] = info[2].strip()
                car_id = info[0]
                x_p = info[1]
                y_p = info[2]
                find, s_id, min_dis = Is_receive(x_p, y_p, sx, sy)
                
                msg = str(car_id) + ';' + str(x_p) + ';' + str(y_p) + ';' + str(s_id) + ';' + str(sx[int(s_id)]) + ';' + str(sy[int(s_id)]) + ';' + str(min_dis)
                text_save(filename, msg)

                if find == False:
                    continue
                else:
                    if Is_exist(car_id, normal_id) == True:
                        set_prob = random.uniform(0.01, 0.03)
                        prob = random.random()
                        if prob <= set_prob:
                            car_trust[int(car_id)] -= 0.02
                        else:
                            car_trust[int(car_id)] += 0.02
                    elif Is_exist(car_id, abnormal_id) == True:
                        set_prob = random.uniform(0.3, 0.7)
                        prob = random.random()
                        if prob <= set_prob:
                            car_trust[int(car_id)] -= 0.02
                        else:
                            car_trust[int(car_id)] += 0.02
        
        t_abnormal_aver = Calc_trust(car_trust, abnormal_id)
        t_normal_aver = Calc_trust(car_trust, normal_id)
        diff = t_normal_aver - t_abnormal_aver

        print("第" + str(i) + '个周期成功')
        T_ab_aver.append(t_abnormal_aver)
        T_nor_aver.append(t_normal_aver)
        Diff.append(diff)
        
    return T_ab_aver, T_nor_aver, Diff

def Result():
    x1, x2, x3 = Solve()
    t = [i for i in range(31)]
    plt.plot(t, x1)
    plt.plot(t, x2)
    plt.plot(t, x3)
    plt.show()

def Act_trust(car_id, cnt_s, cnt_f):
    s = cnt_s / (cnt_s + cnt_f + 1)
    f = 1 / (cnt_s + cnt_f + 1)
    t_act = (2 * s + f) / 2.0
    return car_id, t_act

def Rec_trust():
    print('test')

def fix_FindDate(id):
    with open('F:/Find Data/'+str(id)+'.txt', 'r') as f:
        while f.readable():
            s = f.readline()
            if len(s) <= 0 or s[0] == '\n':
                break
            x = s.split(';')
            sensor_id = int(x[0])
            sensor_num = int(x[1])
            filepath = 'F:/FD/' + str(id) + '.txt'
            msg = str(sensor_id) + ';' + str(sensor_num) + '\n'
            if int(x[0]) != 1000:
                Res_Write(filepath, msg)
    print(str(id) + 'Finsh!')
    return True

def Res_Write(filepath, msg):
    f = open(filepath, 'a')
    f.write(msg)
    f.close()


def main():
    for i in range(1, 41):
        fix_FindDate(i)

if __name__ == "__main__":
    main()