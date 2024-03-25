import os

import tools


def Weight(Provide, Demand, st_provide_weight, st_demand_weight):
    cap = sum(Provide)  # 提供能源总和
    total_demand = sum(Demand)  # 需求能源总和
    a = len(Demand)  # a个需求用户
    b = len(Provide)  # b个供电用户
    st_true_provide = [0.0] * b
    st_true_demand = [0.0] * a

    if cap > total_demand:  # 供大于需
        m = 0
        temp_sums = sum(st_provide_weight)
        temp = [0.0] * b
        for i in range(b):
            temp[i] = temp_sums / st_provide_weight[i]
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

    print("求出每个供电用户供给的电量为", st_true_provide)
    print("求出每个需求用户得到的电量为", st_true_demand)
    weight = tools.sum_weight(Provide, Demand, st_true_provide, st_true_demand, st_provide_weight, st_demand_weight)
    weight = tools.result(weight * 5)
    print("max-min-fair满意度 is", weight)
    current_path = os.path.dirname(__file__)
    with open(current_path + '/../satisfy/processed_WMMF.txt', 'a', encoding='UTF - 8') as f:
        f.write("\n" + str(weight))
    print(tools.ceil2(sum(st_true_provide)), tools.floor2(sum(st_true_demand)))
    return st_true_provide, st_true_demand, weight
