import random
from matplotlib import pyplot as plt
from pulp import *  # 导入 PuLP库函数
from scipy.optimize import LinearConstraint, NonlinearConstraint, minimize, basinhopping, differential_evolution
import time
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
            temp[i] = test_provide_weight / st_provide_weight[i] if st_provide_weight[i] != 0 else 0
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
        # temp = st_provide_weight.index(min(st_provide_weight))
        # st_true_provide[temp] = round(
        #     sum(st_true_provide) - sum(st_true_provide[:temp]) - sum(st_true_provide[temp + 1:]), 2)
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
        # temp = st_demand_weight.index(min(st_demand_weight))
        # st_true_demand[temp] = round(sum(st_true_demand) - sum(st_true_demand[:temp]) - sum(st_true_demand[temp + 1:]),
        #                            2)
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
                st_true_provide[i] = tools.ceil2(total_demand - temp_tg)
                # st_true_provide[i] = round(total_demand - sum(st_true_provide[:i]) - sum(st_true_provide[i + 1:]), 2)
                break
    else:
        st_true_provide = Provide
    distribution = np.argsort(-array(st_demand_weight))
    for i in distribution:
        if cap > Demand[i]:
            cap = tools.floor2(cap - Demand[i])
            st_true_demand[i] = Demand[i]
        else:
            st_true_demand[i] = cap
            # st_true_demand[i] = round(sum(Provide) - sum(st_true_demand[:i]) - sum(st_true_demand[i + 1:]), 2)
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


def scipy0(Provide, Demand, st_provide_weight, st_demand_weight):
    D_num = len(Demand)
    S_num = len(Provide)
    if sum(Provide) < sum(Demand):  # 供小于需
        func = lambda x: -sum([(st_demand_weight[i] / (st_demand_weight[i] + 1)) *
                               np.sqrt(np.maximum(x[i] / Demand[i], 0)) for i in range(D_num)])
        cons = {'type': 'eq', 'fun': lambda x: np.sum(x[:D_num]) - sum(Provide)}
        bounds = [(0, p) for p in Demand]
        minimizer_kwargs = {"method": "SLSQP", "constraints": cons, "bounds": bounds}
        x0 = np.full(D_num, np.mean(Demand))
        ret = basinhopping(func, x0, minimizer_kwargs=minimizer_kwargs, niter=66)
        print(ret.x[:D_num])
        print(ret.fun)
        res = ret.x[:D_num]
        # for i in range(D_num):
        #     res[i] = tools.ceil2(res[i])
        weight = -ret.fun

    else:  # 供大于需

        func = lambda x: -sum([(st_provide_weight[i] / (st_provide_weight[i] + 1)) *
                               np.sqrt(np.maximum(1 - x[i] / Provide[i], 0)) for
                               i in range(S_num)])
        cons = {'type': 'eq', 'fun': lambda x: np.sum(x[:S_num]) - sum(Demand)}
        bounds = [(0, p) for p in Provide]
        # minimizer_kwargs = {"method": "SLSQP", "constraints": cons, "bounds": bounds}
        minimizer_kwargs = {"method": "SLSQP", "constraints": cons, "bounds": bounds}
        x0 = np.full(S_num, np.mean(Provide))

        ret = basinhopping(func, x0, minimizer_kwargs=minimizer_kwargs, niter=66)
        print(ret.x[:S_num])
        print(ret.fun)
        res = ret.x[:S_num]
        # for i in range(S_num):
        #     res[i] = tools.floor2(res[i])
        weight = -ret.fun
    # 打印结果
    print("Optimal solution:")
    print("Objective value at the optimal solution:")
    if sum(Provide) < sum(Demand):
        weight = tools.result(weight)
        print("scipy满意度:", weight)
        with open('LPESCP.txt', 'a', encoding='UTF - 8') as f:
            f.write(str(weight) + '\n')
        return Provide, res, weight

    else:
        for i in range(len(Demand)):
            weight += (1 - 1 / (st_demand_weight[i] + 1))
        weight = tools.result(weight)
        print("scipy满意度:", weight)
        with open('LPESCP.txt', 'a', encoding='UTF - 8') as f:
            f.write(str(weight) + '\n')
        return res, Demand, weight


for i in range(1):

    a = random.randint(8, 15)
    b = 20 - a
    st_true_demand = [0.0] * a
    st_max_demand = []
    st_demand_weight = []
    st_max_provide = []
    st_provide_weight = []
    for i in range(b):
        st_max_provide.append(round(max(1.5, random.random() * 100 - 5), 2))
        st_provide_weight.append(round(random.random() * 10, 2))
    for i in range(a):
        st_max_demand.append(round(max(1.5, random.random() * 100), 2))
        st_demand_weight.append(round(random.random() * 10, 2))
    st_true_provide = [0.0] * b
    total_demand = sum(st_max_demand)
    # if sum(st_max_provide) < 0.9 * total_demand:
    #     # print("less", st_max_provide)
    #     # print(sum(st_max_provide))
    #     for i in range(len(st_max_provide)):
    #         st_max_provide[i] = max(round(st_max_provide[i] + (0.9 * total_demand - sum(st_max_provide)) / b, 2), 1.5)
    # if sum(st_max_provide) > 1.1 * total_demand:
    #     # print("more", st_max_provide)
    #     # print(sum(st_max_provide))
    #     for i in range(len(st_max_provide)):
    #         st_max_provide[i] = max(round(st_max_provide[i] - (sum(st_max_provide) - 1.1 * total_demand) / b, 2), 1.5)
    cap = round(sum(st_max_provide), 2)
    # print("\n\n")
    # print("有", a, "个需求用户")
    # print("各自的用电要求分别是", st_max_demand)
    # print("各自的权重分别是", st_demand_weight)
    # print("有", b, "个供电用户")
    # print("各自的最大供电量分别是", st_max_provide)
    # print("各自的权重分别是", st_provide_weight)
    # print("\n")
    # print("总供电量是", round(cap, 2))
    # print("总需电量是", round(total_demand, 2))
    # strs = ''
    # strs += "有" + str(a) + "个需求用户\n"
    # strs += "各自的用电要求分别是" + str(st_max_demand) + "\n"
    # strs += "各自的权重分别是" + str(st_demand_weight) + "\n"
    # strs += "有" + str(b) + "个供电用户" + "\n"
    # strs += "各自的最大供电量分别是" + str(st_max_provide) + "\n"
    # strs += "各自的权重分别是" + str(st_provide_weight) + "\n"
    # strs += "总供电量是" + str(round(cap, 2)) + "\n"
    # strs += "总需电量是" + str(round(sum(st_max_demand), 2)) + "\n\n"

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

    st_true0_provide, st_true0_demand, weight0 = scipy0(st_max_provide, st_max_demand, st_provide_weight,
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
    st_true_provide2, st_true_demand2, weight1 = Weight(st_max_provide, st_max_demand, st_provide_weight,
                                                        st_demand_weight)

    # print("最后每个供电用户供给的电量为", st_true_provide)
    # print("最后每个需求用户得到的电量为", st_true_demand)
    print("OnlyWeight")
    start = time.perf_counter()
    st_true_provide3, st_true_demand3, weight2 = only_weight(st_max_provide, st_max_demand, st_provide_weight,
                                                             st_demand_weight)
    end = time.perf_counter()
    runTime = end - start
    print("运行时间：", runTime)
    with open('d.txt', 'a', encoding='UTF - 8') as f:
        if weight0 >= weight1 and weight0 >= weight2:
            f.write(str(weight0 >= weight1 and weight0 >= weight2) + (
                "供小于需" if sum(st_max_demand) > sum(st_max_provide) else "供大于需") + '\n')
        else:
            f.write("scipy:" + str(weight0) + ";max-min:" + str(weight1) + ";only_weight:" + str(weight2) + '\n')
