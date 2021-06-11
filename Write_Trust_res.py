import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from Distance import distance 
from matplotlib.pyplot import MultipleLocator
from matplotlib.legend_handler import HandlerPathCollection

def Res_Write(filepath, msg):
    f = open(filepath, 'a')
    f.write(msg)
    f.close()

def Write_T_com_result1(T_com, cycle):#第一个方法的
    for i in T_com:
        filepath = "F:/Tcom1/" + str(cycle) + ".txt"
        msg = str(i) + "\n"
        Res_Write(filepath, msg)

def Write_T_com_result2(T_com, cycle): #第二个方法的
    for i in T_com:
        filepath = "F:/Tcom2/" + str(cycle) + ".txt"
        msg = str(i) + "\n"
        Res_Write(filepath, msg)

def Write_Diff_para(diff, cycle):
    for i in diff:
        filepath = 'F:/Diff part/' + str(cycle) + '.txt'
        msg = str(i) + '\n'
        Res_Write(filepath, msg)

def Write_T_com1(T1, T2, T3):
    for i in range(len(T1)):
        filepath = 'F:/TC1/1.txt'
        msg = str(T1[i]) + ';' + str(T2[i]) + ';' + str(T3[i]) + '\n'
        Res_Write(filepath, msg)    

def Write_T_com2(T1, T2, T3):
    for i in range(len(T1)):
        filepath = 'F:/TC2/1.txt'
        msg = str(T1[i]) + ';' + str(T2[i]) + ';' + str(T3[i]) + '\n'
        Res_Write(filepath, msg)

def Save(T1, T2, T3):
    for i in range(len(T1)):
        filepath = 'F:/Git/tmp.txt'
        msg = str(T1[i]) + ';' + str(T2[i]) + ';' + str(T3[i]) + '\n'
        Res_Write(filepath, msg)

def W_vis(vis, cycle):
    for i in range(len(vis)):
        filepath = 'F:/vis/' + str(cycle) +'.txt'
        msg = str(vis[i]) + '\n'
        Res_Write(filepath, msg)

