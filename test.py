#from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import lab2

#读取文件 
def Read_file():
    file1 = '/Users/guojiawei/Downloads/taxi_february.txt'
    file2 = '/Users/guojiawei/Desktop/Git/t.txt'
    df = pd.read_csv(f_name, header = None, sep = ';')
    #print(df)
    return df

#处理文件中的字符串并且转换为坐标
def Solve_file(df):
    array = df.iloc[:,2]
    x = []
    y = []
    cnt = 0
    for arr in array:
        length = len(arr)
        x_str = ''
        y_str = ''
        for i in range(0,length):
            if(arr[i] == '('):
                i += 1
                while(arr[i] != ' '):
                    x_str = x_str + arr[i]
                    i += 1
                i += 1
                while(arr[i] != ')'):
                    y_str = y_str + arr[i]
                    i += 1
        #x_num = float(x_str)
        #y_num = float(y_str)
        x.append(x_str)
        y.append(y_str)
        cnt += 1
        if(cnt > 5000):
            break
    file_x = '/Users/guojiawei/Desktop/Git/x_point.txt'
    file_y = '/Users/guojiawei/Desktop/Git/y_point.txt'
    text_save(file_x, x)
    text_save(file_y, y)


def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename, 'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存文件成功")

def text_read(filename):
    file = open(filename)
    l = []
    for arr in file:
        num = float(arr)
        l.append(num)
    return l

#绘制散点图
def Draw_result(x, y):
    plt.figure(figsize=(7, 5))
    plt.scatter(x, y, s = 0.1, c = 'k', alpha = 0.5)
    plt.show()

def main():
    file_x = '/Users/guojiawei/Desktop/Git/x_point.txt'
    file_y = '/Users/guojiawei/Desktop/Git/y_point.txt'
    x = text_read(file_x)
    y = text_read(file_y)
    Draw_result(x, y)
    #Solve_file(Read_file())

if __name__ == '__main__':
    main()




        