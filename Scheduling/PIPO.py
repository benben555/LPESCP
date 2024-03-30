import math
import os

import numpy as np
from numpy import array

import tools


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
            break
    print("最后每个供电用户供给的电量为", st_true_provide)
    print("最后每个需求用户得到的电量为", st_true_demand)
    weight = tools.sum_weight(Provide, Demand, st_true_provide, st_true_demand, st_provide_weight, st_demand_weight)
    weight = tools.result(weight * 5)
    print("只考虑权重的能源调度算法满意度 is", weight)
    current_path = os.path.dirname(__file__)
    with open(current_path + '/../satisfy/PIPO.txt', 'a', encoding='UTF - 8') as f:
        f.write("\n" + str(weight))
    print(tools.ceil2(sum(st_true_provide)), tools.floor2(sum(st_true_demand)))
    return st_true_provide, st_true_demand, weight
