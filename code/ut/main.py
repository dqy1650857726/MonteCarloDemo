
from utl import generate
from utl import un_infected_person
from pprint import pprint
from utl import render
import matplotlib.pyplot as plt
from random import randint
from utl import nInfected
from utl import init 
from utl  import each_round_of_infection
from copy import deepcopy
from monte import passResult
from out import wtToFile
from out import inputData
from out import reportA

true_each_round_of_infection = [] #真实感染图的时序图O(t)
from monte import findZeroInf
def main():
    in__ = inputData()
    generate(in__[0],in__[1],False,-99)
    fig = plt.figure(figsize=(10,7))
    fig.canvas.set_window_title("感染实况")
    plt.ion()
    plt.title("0 hao bing ren zhui zong ")
    for i in range(0,in__[2]):
        plt.cla()
        nInfected()
        render(plt)
        plt.pause(0.8)
    #保存时序图
    true_each_round_of_infection = deepcopy(each_round_of_infection)
    print("传播模型感染完成，时序图已经保存！\r\n你要进行几次蒙特卡洛模拟？请输入:(建议不要大于100次)")
    ment_num = int(input())
    plt.close()
    last_sorce_max_result = []
    for i in range(0,ment_num):
        res = findZeroInf(in__[2],true_each_round_of_infection)
        tmp = passResult(res)[0:3]
        wtToFile(tmp,i+1)
        print("第" +str(i+1)+"次完成,完成度:" + str(i+1) + "/" + str(ment_num) +"，按回车进行下一次.")
        last_sorce_max_result.append(tmp[0])
        input()
    print('-'*30)
    print('完成！详细报告在./MonteCarloOutInfo/下')
    reportA(last_sorce_max_result,in__)

if __name__ == "__main__":
    main()