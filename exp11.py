import random
from matplotlib import pyplot as plt
from pulp import *  # 导入 PuLP库函数
from scipy.optimize import LinearConstraint, NonlinearConstraint, minimize

import tools
import numpy as np
from numpy import array


def Weight(Provide, Demand, st_provide_weight, st_demand_weight):
    cap = sum(Provide)  # 提供能源总和
    total_demand = sum(Demand)  # 需求能源总和
    a = len(Demand)  # a个需求用户
    b = len(Provide)  # b个供电用户
    st_true_provide = [0.0] * b
    st_true_demand = [0.0] * a

    if cap > total_demand:  # 供大于需
        m = 0
        test_provide_weight = sum(st_provide_weight)
        temp = [0.0] * b
        for i in range(b):
            temp[i] = test_provide_weight / st_provide_weight[i]
        while total_demand > 0:
            for i in range(b):
                if st_true_provide[i] < Provide[i]:
                    m += temp[i]
            if m == 0:
                break
            mr = total_demand / m
            total_demand = 0
            m = 0
            for i in range(b):
                if st_true_provide[i] < Provide[i]:
                    st_true_provide[i] += (mr * temp[i])
                    st_true_provide[i] = tools.ceil2(st_true_provide[i])
                    if st_true_provide[i] > Provide[i]:
                        total_demand += (st_true_provide[i] - Provide[i])
                        st_true_provide[i] = Provide[i]
        temp = st_provide_weight.index(min(st_provide_weight))
        st_true_provide[temp] = round(
            sum(st_true_provide) - sum(st_true_provide[:temp]) - sum(st_true_provide[temp + 1:]), 2)
        st_true_demand = Demand
    else:
        st_true_provide = Provide
        while cap > 0:
            n = 0
            for i in range(a):
                if st_true_demand[i] < Demand[i]:
                    n += st_demand_weight[i]
            if n == 0:
                break
            br = cap / n
            cap = 0
            for i in range(a):
                if st_true_demand[i] < Demand[i]:
                    st_true_demand[i] += (br * st_demand_weight[i])
                    st_true_demand[i] = tools.floor2(st_true_demand[i])
                    if st_true_demand[i] > Demand[i]:
                        cap += (st_true_demand[i] - Demand[i])
                        st_true_demand[i] = Demand[i]
        temp = st_demand_weight.index(min(st_demand_weight))
        st_true_demand[temp] = round(sum(st_true_demand) - sum(st_true_demand[:temp]) - sum(st_true_demand[temp + 1:]),
                                     2)
    print("求出每个供电用户供给的电量为", st_true_provide)
    print("求出每个需求用户得到的电量为", st_true_demand)
    weight = tools.sum_weight(Provide, Demand, st_true_provide, st_true_demand, st_provide_weight, st_demand_weight)
    weight = tools.result(weight)
    print("max-min-fair满意度 is", weight)
    print(tools.ceil2(sum(st_true_provide)), tools.floor2(sum(st_true_demand)))
    with open('WMMF.txt', 'a', encoding='UTF - 8') as f:
        f.write(str(weight) + '\n')
    return st_true_provide, st_true_demand, weight


def only_weight(Provide, Demand, st_provide_weight, st_demand_weight):
    cap = sum(Provide)  # 提供能源总和
    total_demand = sum(Demand)  # 需求能源总和
    a = len(Demand)  # a个需求用户
    b = len(Provide)  # b个供电用户
    st_true_provide = [0.0] * b
    st_true_demand = [0.0] * a

    if cap > total_demand:  # 供大于需
        distribution = np.argsort(array(st_provide_weight))
        temp_tg = 0
        for i in distribution:
            if temp_tg + Provide[i] < total_demand:
                temp_tg += Provide[i]
                st_true_provide[i] = Provide[i]
            else:
                # st_true_provide[i] = tools.ceil2(total_demand - temp_tg)
                st_true_provide[i] = round(total_demand - sum(st_true_provide[:i]) - sum(st_true_provide[i + 1:]), 2)
                break
    else:
        st_true_provide = Provide
    distribution = np.argsort(-array(st_demand_weight))
    for i in distribution:
        if cap > Demand[i]:
            cap = tools.floor2(cap - Demand[i])
            st_true_demand[i] = Demand[i]
        else:
            # st_true_demand[i] = cap
            st_true_demand[i] = round(sum(Provide) - sum(st_true_demand[:i]) - sum(st_true_demand[i + 1:]), 2)
            break
    print("最后每个供电用户供给的电量为", st_true_provide)
    print("最后每个需求用户得到的电量为", st_true_demand)
    weight = tools.sum_weight(Provide, Demand, st_true_provide, st_true_demand, st_provide_weight, st_demand_weight)
    weight = tools.result(weight)
    print("只考虑权重的能源调度算法满意度 is", weight)
    print(sum(st_true_provide), sum(st_true_demand))
    with open('PIPO.txt', 'a', encoding='UTF - 8') as f:
        f.write(str(weight) + '\n')
    return st_true_provide, st_true_demand, weight


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
            [((1 - 1 / (st_demand_weight[i] + 1)) ** 2 * (1 if Demand[i] == 0 else (1 / Demand[i] * x[i]))) for i in
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
            [((1 - 1 / (st_provide_weight[i] + 1)) ** 2 * (1 if Provide[i] == 0 else (1 - 1 / Provide[i] * x[i]))) for i
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
    if sum(Provide) < sum(Demand):
        weight = tools.result(weight)
        print("pulp满意度:", weight)
        return Provide, res, weight
    else:
        for i in range(len(Demand)):
            weight += (1 - 1 / (st_demand_weight[i] + 1))
        weight = tools.result(weight)
        print("pulp满意度:", weight)
        return res, Demand, weight


def scipy0(Provide, Demand, st_provide_weight, st_demand_weight):
    D_num = len(Demand)
    S_num = len(Provide)
    if sum(Provide) < sum(Demand):  # 供小于需
        def objective(x, st_demand_weight, Demand):
            D_terms = [(st_demand_weight[i] / (st_demand_weight[i] + 1)) * np.sqrt(np.maximum(x[i] / Demand[i], 0)) for
                       i in range(D_num)]
            return -(sum(D_terms))

        # 约束条件
        # def constraint(x):
        #     D_sum = np.sum(x[:D_num])
        #     S_sum = sum(Provide)
        #     return D_sum - S_sum

        # 非线性约束条件：D <= Demand, S <= Provide
        # def nonlinear_constraint(x):
        #     # constraints = []
        #     # for i in range(D_num):
        #     #     constraints.append(x[i] - Demand[i])
        #     constraints=(np.sum(x[:D_num]) - sum(Provide))
        #     return constraints

        # 定义约束条件
        A_eq = np.ones(D_num)
        b_eq = np.sum(Provide)

        linear_constraint = LinearConstraint(A_eq[np.newaxis, :], b_eq, b_eq)
        # linear_constraint = LinearConstraint(np.eye(D_num), 0, np.inf)
        # nonlinear_constraint = NonlinearConstraint(nonlinear_constraint, 0, 0)
        # 初始猜测值
        x0 = np.full(D_num, np.mean(Demand))

        # 定义优化问题
        problem = {
            'fun': lambda x: objective(x, st_demand_weight, Demand),
            'x0': x0,
            'constraints': [linear_constraint],
            'bounds': [(0, p) for p in Demand],
            'method': 'trust-constr',
            'options': {'disp': True, 'gtol': 1e-5}
        }

        # 调用优化器求解问题
        solution = minimize(**problem)
        res = solution.x[:D_num]
        weight = -solution.fun
    else:  # 供大于需
        def objective(x, st_provide_weight, Provide):
            S_terms = [
                (st_provide_weight[i] / (st_provide_weight[i] + 1)) * (
                    np.sqrt(np.maximum(1 - x[i] / Provide[i], 0)) if Provide[i] != 0 else 0) for
                i in range(S_num)]
            return -(sum(S_terms))

        # 约束条件
        # def constraint(x):
        #     S_sum = np.sum(x[:S_num])
        #     D_sum = sum(Demand)
        #     return S_sum - D_sum

        # 非线性约束条件：D <= Demand, S <= Provide
        # def nonlinear_constraint(x):
        #     constraints=(sum(Demand) - np.sum(x[:S_num]))
        #     return constraints

        # 定义约束条件
        A_eq = np.ones(S_num)
        b_eq = np.sum(Demand)

        linear_constraint = LinearConstraint(A_eq[np.newaxis, :], b_eq, b_eq)
        # linear_constraint = LinearConstraint(np.eye(S_num), 0, Provide)
        # nonlinear_constraint = NonlinearConstraint(nonlinear_constraint, 0, 0)
        # 初始猜测值
        x0 = np.full(S_num, np.mean(Provide))

        # 定义优化问题
        problem = {
            'fun': lambda x: objective(x, st_provide_weight, Provide),
            'x0': x0,
            'constraints': [linear_constraint],
            'bounds': [(0, p) for p in Provide],
            'method': 'trust-constr',
            'options': {'disp': True, 'gtol': 1e-5}
        }

        # 调用优化器求解问题
        solution = minimize(**problem)
        res = solution.x[:S_num]
        weight = -solution.fun
    # 打印结果
    print("Optimal solution:")
    print("Objective value at the optimal solution:")
    print(-solution.fun)  # 取负数以还原最大化结果
    if sum(Provide) < sum(Demand):
        weight = tools.sum_weight(Provide, Demand, Provide, res, st_provide_weight, st_demand_weight)
        weight = tools.result(weight)
        print("scipy满意度:", weight)
        with open('LPESCP.txt', 'a', encoding='UTF - 8') as f:
            f.write(str(weight) + '\n')
        return Provide, res, weight

    else:
        # for i in range(len(Demand)):
        #     weight += (1 - 1 / (st_demand_weight[i] + 1))
        weight = tools.sum_weight(Provide, Demand, res, Demand, st_provide_weight, st_demand_weight)
        weight = tools.result(weight)
        print("scipy满意度:", weight)
        with open('LPESCP.txt', 'a', encoding='UTF - 8') as f:
            f.write(str(weight) + '\n')
        return res, Demand, weight


a = random.randint(8, 15)
b = 20 - a
st_true_demand = [0.0] * a
st_max_demand = []
st_demand_weight = []
st_max_provide = []
st_provide_weight = []
for i in range(b):
    st_max_provide.append(round(max(0.1, random.random() * 100 - 5), 2))
    st_provide_weight.append(round(random.random() * 10, 2))
for i in range(a):
    st_max_demand.append(round(random.random() * 100, 2))
    st_demand_weight.append(round(random.random() * 10, 2))
st_true_provide = [0.0] * b
total_demand = sum(st_max_demand)
if sum(st_max_provide) < 0.9 * total_demand:
    # print("less", st_max_provide)
    # print(sum(st_max_provide))
    for i in range(len(st_max_provide)):
        st_max_provide[i] = max(round(st_max_provide[i] + (0.9 * total_demand - sum(st_max_provide)) / b, 2), 0)
if sum(st_max_provide) > 1.1 * total_demand:
    # print("more", st_max_provide)
    # print(sum(st_max_provide))
    for i in range(len(st_max_provide)):
        st_max_provide[i] = max(round(st_max_provide[i] - (sum(st_max_provide) - 1.1 * total_demand) / b, 2), 0)
cap = round(sum(st_max_provide), 2)
# print("\n\n")
print("有", a, "个需求用户")
print("各自的用电要求分别是", st_max_demand)
print("各自的权重分别是", st_demand_weight)
print("有", b, "个供电用户")
print("各自的最大供电量分别是", st_max_provide)
print("各自的权重分别是", st_provide_weight)
print("\n")
print("总供电量是", round(cap, 2))
print("总需电量是", round(total_demand, 2))

n = 0.0
br = 0
init_cap = 0
remain_cap = cap
m = 0.0
mr = 0.0
title2 = '供小于需时供电用户能源调度图'
title4 = '供小于需时需电用户能源调度图'
if cap > total_demand:
    title2 = '供大于需时供电用户能源调度图'
    title4 = '供大于需时需电用户能源调度图'
print("scipy")
st_true0_provide, st_true0_demand, _ = scipy0(st_max_provide, st_max_demand, st_provide_weight,
                                              st_demand_weight)

print("最后每个供电用户供给的电量为", np.around(st_true0_provide, decimals=2))
print("最后每个需求用户得到的电量为", np.around(st_true0_demand, decimals=2))
# print("plup")
# st_true_provide, st_true_demand, _ = pulp(st_max_provide, st_max_demand, st_provide_weight,
#                                           st_demand_weight)
#
# print("最后每个供电用户供给的电量为", st_true_provide)
# print("最后每个需求用户得到的电量为", st_true_demand)
print("MaxMinFair")
st_true_provide2, st_true_demand2, _ = Weight(st_max_provide, st_max_demand, st_provide_weight,
                                              st_demand_weight)

# print("最后每个供电用户供给的电量为", st_true_provide)
# print("最后每个需求用户得到的电量为", st_true_demand)
print("OnlyWeight")
st_true_provide3, st_true_demand3, _ = only_weight(st_max_provide, st_max_demand, st_provide_weight,
                                                   st_demand_weight)

# print("最后每个供电用户供给的电量为", st_true_provide)
# print("最后每个需求用户得到的电量为", st_true_demand)
# strs = ''
# strs += "有" + str(a) + "个需求用户\n"
# strs += "各自的用电要求分别是" + str(st_max_demand) + "\n"
# strs += "各自的权重分别是" + str(st_demand_weight) + "\n"
# strs += "有" + str(b) + "个供电用户" + "\n"
# strs += "各自的最大供电量分别是" + str(st_max_provide) + "\n"
# strs += "总供电量是" + str(round(cap, 2)) + "\n"
# strs += "总需电量是" + str(round(sum(st_max_demand), 2)) + "\n"
# strs += "最后每个需求用户得到的电量为" + str(st_true0_demand) + "\n\n"
# with open('data.txt', 'a', encoding='UTF - 8') as f:
#     data = f.write(strs)
# x轴坐标, a=5, 返回[0, 1, 2, 3, 4]
# x = np.arange(1, 1 + a)
x = [i + 1 for i in range(a)]
# x轴坐标, a=5, 返回[0, 1, 2, 3, 4]
# x1 = np.arange(1, 1 + b)
x1 = [i + 1 for i in range(b)]
# fig = plt.figure(figsize=(10, 9))
# plt.subplots_adjust(left=None, bottom=0.15, right=None, top=None, wspace=0.3, hspace=0.5)
# ax1 = fig.add_subplot(2, 2, 1)
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei显示中文\n",
# ax2 = fig.add_subplot(2, 1, 1)
total_width, n = 0.8, 2
# 每种类型的柱状图宽度
width = total_width / n

plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei显示中文\n",
# plt.title(title2)  # 添加标题\n",
plt.xlabel('User ID')  # 添加横轴标签\n",
plt.ylabel('Electricity energy (kW·h)')  # 添加y轴名称\n",
# 画柱状图
plt.bar(x1, st_max_provide, width=width, label="Maximum Electricity Supplied")
x11 = [i + 1 + width for i in range(b)]
plt.bar(x11, st_true0_provide, width=width, label="Actual Electricity Supplied")
plt.xticks(x1)
plt.legend(fontsize=7)

# ax3 = fig.add_subplot(2, 2, 3)
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei显示中文\n",
plt.savefig('1.svg', format='svg', dpi=150)  # 输出
plt.show()
#
# ax4 = fig.add_subplot(2, 1, 2)


total_width, n = 0.8, 2
# 每种类型的柱状图宽度
width = total_width / n
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei显示中文\n",
# plt.title(title4)  # 添加标题\n",
plt.xlabel('User ID')  # 添加横轴标签\n",
plt.ylabel('Electricity energy (kW·h)')  # 添加y轴名称\n",
# 画柱状图
plt.bar(x, st_max_demand, width=width, label="Electricity Demand")
x2 = [i + 1 + width for i in range(a)]

plt.bar(x2, st_true0_demand, width=width, label="Actual Electricity Received")
plt.xticks(x)
# 显示图例
plt.legend(fontsize=7)
# 显示柱状图
plt.savefig('2.svg', format='svg', dpi=150)  # 输出
plt.show()
#
