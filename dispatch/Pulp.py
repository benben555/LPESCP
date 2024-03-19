import math

from pulp import *  # 导入 PuLP库函数

import tools


def pulp(Provide, Demand, st_provide_weight, st_demand_weight):
    MyProbLP = LpProblem("LPProbDemo1", sense=LpMaximize)
    '''
        定义一个规划问题
        pulp.LpProblem 是定义问题的构造函数。
    　　"LPProbDemo1"是用户定义的问题名（用于输出信息）。
    　　参数 sense 用来指定求最小值/最大值问题，可选参数值：LpMinimize、LpMaximize 。
    '''
    if sum(Provide) < sum(Demand):  # 供小于需
        a = len(Demand)
        res = [0] * a
        material = [i for i in range(a)]
        x = LpVariable.dicts('电量', material, lowBound=0, cat='Continuous')
        MyProbLP += lpSum(
            [((1 - 1 / (st_demand_weight[i] + 1)) * (1 if Demand[i] == 0 else (1 / Demand[i] * x[i]))) for i in
             material])
        for i in material:
            MyProbLP += (x[i] <= Demand[i])
        MyProbLP += lpSum([x[i] for i in material]) <= sum(Provide)
    else:
        a = len(Provide)
        res = [0] * a
        material = [i for i in range(a)]
        x = LpVariable.dicts('电量', material, lowBound=0, cat='Continuous')
        MyProbLP += lpSum(
            [((1 - 1 / (st_provide_weight[i] + 1)) * (1 if Provide[i] == 0 else (1 - 1 / Provide[i] * x[i]))) for i
             in material])
        for i in material:
            MyProbLP += (x[i] <= Provide[i])
        MyProbLP += lpSum([x[i] for i in material]) == sum(Demand)

    MyProbLP.solve()
    # print("Status:", LpStatus[MyProbLP.status])  # 输出求解状态
    for v in MyProbLP.variables():
        temp = v.name.split('_')[1]
        res[int(temp)] = v.varValue
        # print(v.name, "=", v.varValue)  # 输出每个变量的最优值
    # print("F(x) = ", value(MyProbLP.objective))  # 输出最优解的目标函数值
    weight = value(MyProbLP.objective)
    current_path = os.path.dirname(__file__)
    if sum(Provide) < sum(Demand):
        weight = tools.result(weight * 5)
        with open(current_path + '/../satisfy/processed_LPESCP.txt', 'a', encoding='UTF - 8') as f:
            f.write("\n" + str(weight))
        return Provide, res, weight
    else:
        for i in range(len(Demand)):
            weight += (1 - 1 / (st_demand_weight[i] + 1)) ** 2
        weight = tools.result(weight * 5)
        with open(current_path + '/../satisfy/processed_LPESCP.txt', 'a', encoding='UTF - 8') as f:
            f.write("\n" + str(weight))
        return res, Demand, weight
