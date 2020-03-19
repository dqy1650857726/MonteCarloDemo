import os
import matplotlib.pyplot as pyp3

sequence_diagram_dir = './SequenceDiagram/'
file_dir = 'MonteCarloOutInfo/'

#把当前的感染状态保存到文件
def saveNow(plan,i):
    global sequence_diagram_dir
    qname = sequence_diagram_dir + str(i) + '.png'
    plan.savefig(qname)

def cleanAllPng():
    lis = os.listdir(sequence_diagram_dir)
    for i in lis:
        os.remove(sequence_diagram_dir+i)

def wtToFile(data,n):
    qname = file_dir +"感染的报告汇总.info"
    fp = open(qname,'a')
    fp.writelines("第" + str(n) + "次蒙特卡洛模拟完成！可能3的源头：\n")
    fp.writelines("坐标    paz(该值越高为源头的概率越大)\n")
    for i in data:
        fp.writelines(str(i))
        fp.write('\n')
    fp.writelines("------------------------------------------\n")
    fp.close()

def cleanAllFile():
    fp = open(file_dir +"感染的报告汇总.info",'w+')
    fp.close()

def inputData():
    print("设定一个感染源")
    print("输入x坐标")
    x=int(input())
    print("输入y坐标")
    y=int(input())
    print('输入感染轮数')
    n=int(input())
    return x,y,n

def reportA(last_result,in__):
    x_data = [str(x) for x in range(1,len(last_result)+1)]
    y_data = [(abs(y_.x-in__[0])+abs(y_.y-in__[1])) for y_ in last_result]
    print(y_data)
    fig = pyp3.figure(figsize=(8,6))
    fig.canvas.set_window_title("蒙特卡洛模拟N次，每次的误差曲线")
    pyp3.rcParams['font.sans-serif']=['SimHei']
    pyp3.rcParams['axes.unicode_minus']=False
    pyp3.xlabel("第几次")
    pyp3.ylabel("误差，曼哈顿距离")
    pyp3.plot(x_data,y_data)
    pyp3.show()
    input()


    

