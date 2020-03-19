
from copy import deepcopy
from utl import generate
from utl import nInfected
from utl import each_round_of_infection
from utl import PMAX
from cls import Result
import os
import operator

saves=[]

#寻找0号病人
def findZeroInf(n,true_each_round_of_infection): #n表示迭代次数，
    from utl import INIT_STATE_DATA
    global INIT_STATE_DATA
    maxx =len(INIT_STATE_DATA)
    saves.clear()
    for i in range(0,maxx):
        monteCarloOnce(n,i)
        compareAndSave(i,true_each_round_of_infection)
        os.system("cls")
        print('#'*i+'-'*(maxx-i) + "%d/%d"%(i,maxx))
    return saves

#使用蒙特卡洛算法进行一次溯源
def monteCarloOnce(n,k):
    generate(-1,-1,True,k)
    for i in range(0,n):
        nInfected()
    
#比较并保存结果
def compareAndSave(k,true_each_round_of_infection):
    sorce = 0;
    for i in range(0,len(each_round_of_infection)):
        for j in range(0,PMAX):
            if each_round_of_infection[i][j].state==true_each_round_of_infection[i][j].state:
                sorce+=1;
    p = INIT_STATE_DATA[k].point
    saves.append(Result(p[0],p[1],sorce))

#过滤结果
def passResult(res):
    rig = len(res)
    sum=0
    for i in range(0,rig):
        sum += res[i].sorce
    avg = sum/rig
    new_res=list()
    for i in range(0,rig):
        if res[i].sorce>avg:
            res[i].sorce-=avg
            new_res.append(res[i])
    new_res = sorted(new_res,key=operator.attrgetter('sorce'),reverse=True)
    return new_res
