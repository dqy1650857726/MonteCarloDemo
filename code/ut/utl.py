from cls import People
from random import randint
from copy import copy
from copy import deepcopy
from out import saveNow
from out import cleanAllPng
import matplotlib.pyplot as towplt
from out import cleanAllFile

#----------------运行前先看参数，可以调参--------
PMAX = 88 #人数                               |
WMAX = 200 #                                 |
HMAX = 200 #地图大小                         |
POINTSIZE = 2 #可视化点的大小                |
U=33 #感染概率 1-100                        |
N=6#允许感染最近的n人                       |
MAX_INF=100 #最大感染距离(x+y)              |
#------------------------------------------

was_n_inf=0 #记录感染轮数
infn=0  #记录每轮的新增感染者
flag = True #缓存开启
isF = False #是否完成模拟感染
once = 0;
#data:
infected_person=[]
un_infected_person=[]
res_cache = {}

INIT_STATE_DATA = [] #最初的人群图，此图不会改变，且全是未感染的人，作为蒙克卡罗的输入源
init_persons_state=[] #迭代每次感染的状态
each_round_of_infection = [] #list[ list[] ] 感染时序图 O(t)

def init(x,y,fag,k):
    global once
    global init_persons_state,INIT_STATE_DATA,isF

    if fag==False:
        cleanAllPng()
        infected_person.append(People((x,y),False))
        init_persons_state = infected_person+un_infected_person
        INIT_STATE_DATA=deepcopy(init_persons_state)
        INIT_STATE_DATA[0].state=True
        cleanAllFile()
        ##0号感染图，标注了0号病人的位置
        towplt.figure(figsize=(10,7))
        render(towplt)
        towplt.close()
    else:
        isF=True
        infected_person.append(deepcopy(INIT_STATE_DATA[k]))
    init_persons_state = infected_person+un_infected_person
    appendEROI()

#向时序图中添加，每一轮感染后都会调用这个
def appendEROI():
    each_round_of_infection.append(deepcopy(init_persons_state))

##N轮感染
def nInfected():
    is_inf_list=[]
    global was_n_inf
    global infn
    infn=0
    def report():
        if isF==False:
            print('-'*30)
            print("第%d轮感染，新增%d个感染者"%(was_n_inf,infn))
            print("总计感染:%d,未被感染%d"%(len(infected_person),len(un_infected_person)))

    def flush_db():
        for i in is_inf_list:
            try:
                un_infected_person.remove(i)
                infected_person.append(i)
                i.state=False
            except Exception:
                pass
        is_inf_list.clear()

    def infected(p0):
        global infn
        #[0,100]闭区间
        if randint(0,100)<U:#p0被感染
            # un_infected_person.remove(p0);
            # infected_person.append(p0);
            # p0.state=False
            is_inf_list.append(p0)
            infn += 1
    #感染规则：传给最近的N个人，概率为u
    for i in infected_person:
        late_person = getInfPersonRangeN(i)
        for j in late_person:
            infected(j)
    was_n_inf+=1
    flush_db()
    appendEROI()
    report()
    if len(un_infected_person)==0:
        print("X")

#取得感染者最近的N个人
def getInfPersonRangeN(inf_person):#参数感染者
    res = []
    desp = []
    def js(p0):#参数正常人
        return abs(p0.point[0]-inf_person.point[0]) + abs(p0.point[1]-inf_person.point[1])
    for i in un_infected_person:
        nlen = js(i)
        if nlen>MAX_INF: #超出感染距离无法感染
            continue
        if(len(res)<N):
            res.append(i)
            desp.append(nlen)
        else:#把该人与上一次最小N人比较
            max = 0
            idx = 0
            for d in desp:
                if(nlen<d):
                    desp[idx]=nlen
                    res[idx]=i
                    break
                idx += 1
    return res

####从persons中提取坐标
def getData():
    if flag==True:
        result = {'infx':[],'infy':[],
                'un_infx':[],'un_infy':[]}
        for i in infected_person:
            result['infx'].append(i.point[0])
            result['infy'].append(i.point[1])

        for i in un_infected_person:
            result['un_infx'].append(i.point[0])
            result['un_infy'].append(i.point[1])
        res_cache = result
        return result
    else:#已失效 互虐该项
        print("缓存提取")
        return res_cache

def render(plan):
    res = getData()
    for i in infected_person:
        plan.scatter(res['infx'],res['infy'],s=POINTSIZE,c='red')
    for i in un_infected_person:
        plan.scatter(res['un_infx'],res['un_infy'],s=POINTSIZE,c='yellow')
    saveNow(plan,was_n_inf)

def generate(x,y,fag,k):#fag=T表示蒙特卡洛的算法开始,且k表示预测的0号病人
    global un_infected_person,infected_person,init_persons_state,was_n_inf
    un_infected_person.clear()
    infected_person.clear()
    init_persons_state.clear()
    each_round_of_infection.clear()
    was_n_inf=0
    if fag==False:
        for i in range(0,PMAX-1):
            un_infected_person.append(People(genPoint(),True))
    else:
        un_infected_person = deepcopy(INIT_STATE_DATA)
        del un_infected_person[k]
    init(x,y,fag,k)
    

def genPoint():
    point = (randint(0,WMAX),randint(0,HMAX))
    return point