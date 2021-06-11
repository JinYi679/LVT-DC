import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import os
from matplotlib.pyplot import MultipleLocator
from cover import Cover1

#12.80629 42.01097

def Get_T_com(filepath, base):
    vis_T = [0 for i in range(350)]
    cid = 0
    with open(filepath, 'r') as f:
        for i in f.readlines():
            info = i.split('\n')
            t = float(info[0])
            if t > base:
                vis_T[cid] = 1
            cid += 1
            if cid > 316:
                break
    return vis_T

def cover_point():
    a = [17, 283, 61, 394, 926, 1, 90, 163, 43, 442, 838, 320, 42, 82, 16, 210, 73, 238, 34, 59, 629, 45, 590, 46, 428, 56, 281, 169, 85, 155, 182, 178, 195, 754, 3, 20, 4, 11, 414, 987, 114, 8, 536, 152, 122, 21, 0, 177, 94, 124, 72, 591]
    b = [0, 1, 2, 4, 5, 8, 11, 12, 14, 16, 20, 21, 24, 27, 28, 30, 33, 36, 39, 43, 44, 45, 46, 49, 52, 54, 57, 59, 60, 67, 68, 69, 70, 71, 72, 74, 77, 82, 83, 85, 87, 90, 91, 93, 94, 100, 101, 102, 103, 104, 114, 115, 119, 120, 121, 
122, 126, 127, 128, 132, 133, 136, 146, 147, 149, 151, 152, 153, 155, 158, 159, 161, 163, 165, 172, 173, 177, 178, 179, 182, 184, 186, 189, 192, 196, 199, 203, 205, 210, 212, 214, 215, 219, 222, 225, 228, 233, 234, 236, 238, 
239, 246, 247, 253, 256, 264, 265, 267, 271, 274, 275, 276, 281, 282, 283, 286, 289, 291, 295, 298, 300, 302, 306, 308, 309, 310, 314, 320, 324, 327, 329, 332, 336, 341, 346, 347, 357, 360, 361, 365, 370, 373, 374, 375, 384, 
385, 394, 399, 402, 403, 409, 414, 418, 420, 423, 424, 427, 428, 430, 432, 433, 437, 439, 440, 443, 446, 448, 452, 454, 459, 467, 473, 476, 485, 487, 488, 490, 492, 494, 497, 498, 500, 509, 511, 512, 514, 516, 517, 521, 523, 
524, 525, 526, 527, 528, 529, 532, 533, 536, 537, 539, 540, 543, 546, 547, 549, 550, 552, 556, 557, 558, 561, 564, 565, 569, 573, 575, 579, 582, 584, 585, 589, 590, 591, 600, 604, 611, 617, 618, 619, 621, 626, 629, 634, 636, 
641, 643, 645, 658, 659, 660, 661, 667, 670, 672, 681, 688, 691, 699, 700, 706, 708, 711, 713, 715, 722, 725, 727, 738, 742, 743, 749, 753, 754, 758, 759, 764, 766, 767, 768, 777, 781, 784, 788, 789, 791, 794, 796, 798, 804, 
809, 812, 814, 816, 817, 819, 823, 826, 829, 833, 834, 838, 841, 843, 845, 848, 850, 859, 863, 868, 874, 877, 883, 884, 885, 888, 890, 893, 894, 896, 897, 900, 908, 910, 913, 916, 918, 920, 923, 925, 926, 927, 928, 931, 937, 
944, 947, 952, 966, 971, 973, 974, 982, 983, 984, 989, 993, 994, 995, 997]
    return a, b

def get_cover():
    cover_id = [0 for i in range(1, 1002)]
    vis_car = []
    for cycle in range(1, 11):
        base = 0.8
        filepath = 'F:/Tcom1/' + str(cycle) + '.txt'
        vis_car = Get_T_com(filepath, base)
        
        if cycle % 10 == 1:
            cover_id = [0 for i in range(1002)]
        
        cover_id = Cover1(cycle, cover_id)
    
    return cover_id

def Read_s():
    x = []
    y = []
    with open('F:/DataCenter_location.txt','r') as f:
        for i in f.readlines():
            info = i.split(';')
            info[1] = info[1].strip()
            a = float(info[0])
            b = float(info[1])
            x.append(a)
            y.append(b)
    return x, y

def draw(sx, sy, senx, seny):
    
    #b = get_cover()
    #plt.figure(figsize=(10, 7))
    a, b = cover_point()

    x = []
    y = []
    '''
    for i in range(len(b)):
            x.append(senx[i])
            y.append(seny[i])
    '''
    for i in range(len(a)):
        x.append(senx[a[i]])
        y.append(seny[a[i]])

    #plt.figure(figsize=(10, 7))
    print(1)
    print(len(a))
    

    plt.xticks(np.arange(12.20661, 13.0, 0.15))
    plt.yticks(np.arange(41.72532, 42.2, 0.08)) #8:5
    #7FFFAA
    plt.scatter(sx, sy, s = 0.01, c = '#B3B3B5', alpha = 0.5)
    plt.scatter(senx, seny,s = 7,c = 'r', alpha = 1)
    plt.scatter(x, y, s = 8, c = 'b', alpha = 1) #Include digital watermark
    pic = plt.legend(('MVs trajectory', 'Sensor deployment', 'Include verification code'),loc = 'upper right',fontsize = 'medium')
    #pic = plt.legend(loc = 'upper right', fontsize = 'medium')
    #调整图例散点的大小
    pic.legendHandles[0]._sizes = [30]
    pic.legendHandles[1]._sizes = [30]
    pic.legendHandles[2]._sizes = [30]
    #pic.legendHandles[3]._sizes = [30]
    
    plt.savefig('cyc=1.png', bbox_inches='tight', dpi = 360, pad_inches = 0.0)
    plt.show()

def Draw_result(x, y, sx, sy):
    plt.figure(figsize=(10, 7))
    plt.title('Simulation diagram', Fontsize = 'x-large')
    plt.xticks(np.arange(12.20661, 13.0, 0.15))
    plt.yticks(np.arange(41.72532, 42.2, 0.08))

    plt.scatter(x, y, s = 0.01, c = '#B3B3B5', alpha = 0.5)
    plt.scatter(sx, sy, s = 7, c = 'r', alpha = 1)
    pic = plt.legend(('Vehicle trajectory', 'Sensor deployment'),loc = 'upper right',fontsize = 'medium')
    #调整图例散点的大小
    pic.legendHandles[0]._sizes = [30]
    pic.legendHandles[1]._sizes = [30]
    plt.savefig('5.1.png')
    print("success!")
    plt.show()

def r(): #运动轨迹
    X = []
    Y = []
    for i in range(1,91):
        print("读取第",i,"个文件")
        with open('F:/Lab Data/' + str(i) + '.txt','r') as f:
            for s in f.readlines():
                x=s.split(';')
                x[2]=x[2].strip()
                X.append(float(x[1]))
                Y.append(float(x[2]))
    return X,Y

if __name__=='__main__':
    sensorX = []
    sensorY = []
    x, y = r()
    print('开始画图')
    
    f = open("sensor_location.txt", 'r')
    for i in f.readlines():
        a = i.split(';')
        a[1] = a[1].strip()
        sensorX.append(float(a[0]))
        sensorY.append(float(a[1]))
    f.close()
    
    draw(x, y, sensorX, sensorY)