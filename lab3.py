import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from datetime import datetime
import datetime

def Read_map():
    dic = {}
    file_path = '/Users/guojiawei/Desktop/Git/maps.txt'
    rd = pd.read_csv(file_path, sep = ';')
    for index, row in rd.iterrows():
        a = str(row['a'])
        b = str(row['b'])
        dic[a] = b
    return dic

def Judge_point(x, y):
    x = float(x)
    y = float(y)
    if x >= 41.72532 and x <= 42.01097 and y >= 12.20661 and y <= 12.80629:
        return True
    else:
        return False
#读取文件 
def Read_file():
    file1 = '/Users/guojiawei/Downloads/taxi_february.txt'
    #file2 = '/Users/guojiawei/Desktop/Git/t.txt'
    df = pd.read_csv(file1, sep = ';')
    #print(df)
    return df

#处理文件中的字符串并且转换为坐标
def Solve_file(df): 
    mp = Read_map()
    start_date = datetime.datetime.strptime('2014-02-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    f_id = '1'
    for index,row in df.iterrows():   
        p = row['p']
        x_str = ''
        y_str = ''
        for i in range(len(p)):
            if(p[i] == '('):
                i += 1
                while(p[i] != ' '):
                    x_str = x_str + p[i]
                    i += 1
                i += 1
                while(p[i] != ')'):
                    y_str = y_str + p[i]
                    i += 1           
        if Judge_point(x_str, y_str) == False:
            continue
        
        d = row['d']
        d_str = ''
        for i in range(len(d)):
            if(d[i] == '.' or d[i] == '+'):
                break
            d_str = d_str + d[i]
        now_date = datetime.datetime.strptime(d_str, '%Y-%m-%d %H:%M:%S')
        diff_date = (now_date - start_date).total_seconds()
        
        car_preid = str(row['i'])
        car_id = str(mp[car_preid])
        if(diff_date <= 28800.0):
            msg = car_id + ';' + y_str + ';' + x_str
            f_name = f_id + '.txt'
            text_save(f_name, msg)
        else:
            start_date =  (start_date + datetime.timedelta(seconds=28800.0)).strftime("%Y-%m-%d %H:%M:%S")
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
            msg = car_id + ';' + y_str + ';' + x_str
            f_id = str(int(f_id) + 1)
            f_name = f_id + '.txt'
            text_save(f_name, msg)
            print("保存第" + f_id + "个文件成功")

def text_save(filename, msg):#filename为写入CSV文件的路径，data为要写入数据列表.
    file_path = '/Users/guojiawei/Desktop/Lab Data/' + filename
    file = open(file_path, 'a')
    file.write(msg + '\n')
    file.close()
    #print("保存文件成功")

def main():
    df = Read_file()
    Solve_file(df)

if __name__ == '__main__':
    main()