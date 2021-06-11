import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from Distance import distance
from matplotlib.pyplot import MultipleLocator
from matplotlib.legend_handler import HandlerPathCollection
from cover import Cover1
from cover import Cover2

def cnt_sensor(filepath, cover_id):
    cnt = 0
    sum = 0
    with open(filepath, 'r') as f:
        for x in f.readlines():
            info = x.split(';')
            info[1] = info[1].strip()
            num = int(info[1]) #传感器被报告次数
            s_id = int(info[0])
            if cover_id[s_id] > 0:
                cnt += num
            sum += num
    return cnt, sum


#carid, x, y, sid, x, y, min_dis
def Cr_method1():
    cover_id = [0 for i in range(1, 1002)]
    res = []
    c = []
    for cycle in range(1, 41):
        s = 0
        filepath = 'F:/Find Data/' + str(cycle) + '.txt'
        cover_id = Cover1(cycle, cover_id) 
        cnt, sum = cnt_sensor(filepath, cover_id)
        ans = float(cnt) / float(sum)
        res.append(ans)
        for j in range(len(cover_id)):
            if cover_id[j] > 0:
                cover_id[j] -= 1
                s += 1
        c.append(s)
        print("第一个方法第" + str(cycle) + "个周期完成")
    print(c)
    return res

def Cr_method2():
    cover_id = [0 for i in range(1, 1002)]
    res = []
    c = []
    for cycle in range(1, 41):
        s = 0
        filepath = 'F:/Find Data/' + str(cycle) + '.txt'
        cover_id = Cover2(cycle) 
        cnt, sum = cnt_sensor(filepath, cover_id)
        for j in range(len(cover_id)):
            if cover_id[j] > 0:
                cover_id[j] -= 1
                s += 1
        c.append(s)
        ans = float(cnt) / float(sum)
        res.append(ans)
        print("第二个方法第" + str(cycle) + "个周期完成")
    print(c)
    return res




#Positive, Recommendation, Probability, Comprehensive
def Result():
    res1 = Cr_method1()
    res2 = Cr_method2()
    #print(res1)
    #print(res2)
    t = [i for i in range(1, 41)]
    #plt.title('Comparison of Verifiable rate of data under two strategies', fontsize = 'large')
    plt.xlabel('Time')
    plt.ylabel('Verifiable rate of data')
    
    plt.plot(t, res1, 'rp-', linewidth = 1, markersize = 5.0, label = 'Our Strategy')  #$\overline{T_{abn}}$
    plt.plot(t, res2, 'ks-', linewidth = 1, markersize = 5.0, label = 'UAV only collects')
    
    new = 0.
    old = 0.
    for i in range(len(res1)):
        new += res1[i]
        old += res2[i]
    new = new / 40
    old = old / 40

    #print(new, old)

    x_major_locator = MultipleLocator(8)
    y_major_locator = MultipleLocator(0.1)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    
    plt.xlim(0, 40)
    plt.ylim(0.45, 0.92)
    plt.legend(loc=0, framealpha = 0.5, fontsize = 'xx-large') 
    #plt.savefig('Verifiable.png')
    plt.show()
    

def main():
    Result()
    #Res2(x1, x2)

if __name__ == "__main__":
    main()

