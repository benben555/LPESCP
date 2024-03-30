import math

from pulp import *  # 导入 PuLP库函数

import tools


# def pulp(Provide, Demand, st_provide_weight, st_demand_weight):
#     MyProbLP = LpProblem("LPProbDemo1", sense=LpMaximize)
#     '''
#         定义一个规划问题
#         pulp.LpProblem 是定义问题的构造函数。
#     　　"LPProbDemo1"是用户定义的问题名（用于输出信息）。
#     　　参数 sense 用来指定求最小值/最大值问题，可选参数值：LpMinimize、LpMaximize 。
#     '''
#     if sum(Provide) < sum(Demand):  # 供小于需
#         a = len(Demand)
#         res = [0] * a
#         material = [i for i in range(a)]
#         x = LpVariable.dicts('电量', material, lowBound=0, cat='Continuous')
#         MyProbLP += lpSum(
#             [((1 - 1 / (st_demand_weight[i] + 1)) * (1 if Demand[i] == 0 else (1 / Demand[i] * x[i]))) for i in
#              material])
#         for i in material:
#             MyProbLP += (x[i] <= Demand[i])
#         MyProbLP += lpSum([x[i] for i in material]) <= sum(Provide)
#     else:
#         a = len(Provide)
#         res = [0] * a
#         material = [i for i in range(a)]
#         x = LpVariable.dicts('电量', material, lowBound=0, cat='Continuous')
#         MyProbLP += lpSum(
#             [((1 - 1 / (st_provide_weight[i] + 1)) * (1 if Provide[i] == 0 else (1 - 1 / Provide[i] * x[i]))) for i
#              in material])
#         for i in material:
#             MyProbLP += (x[i] <= Provide[i])
#         MyProbLP += lpSum([x[i] for i in material]) == sum(Demand)
#
#     MyProbLP.solve()
#     # print("Status:", LpStatus[MyProbLP.status])  # 输出求解状态
#     for v in MyProbLP.variables():
#         temp = v.name.split('_')[1]
#         res[int(temp)] = v.varValue
#         # print(v.name, "=", v.varValue)  # 输出每个变量的最优值
#     # print("F(x) = ", value(MyProbLP.objective))  # 输出最优解的目标函数值
#     weight = value(MyProbLP.objective)
#     current_path = os.path.dirname(__file__)
#     if sum(Provide) < sum(Demand):
#         weight = tools.result(weight * 5)
#         with open(current_path + '/../satisfy/processed_LPESCP.txt', 'a', encoding='UTF - 8') as f:
#             f.write("\n" + str(weight))
#         return Provide, res, weight
#     else:
#         for i in range(len(Demand)):
#             weight += (1 - 1 / (st_demand_weight[i] + 1)) ** 2
#         weight = tools.result(weight * 5)
#         with open(current_path + '/../satisfy/processed_LPESCP.txt', 'a', encoding='UTF - 8') as f:
#             f.write("\n" + str(weight))
#         return res, Demand, weight

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
    current_path = os.path.dirname(__file__)
    if sum(Provide) < sum(Demand):
        weight = tools.sum_weight(Provide, Demand, Provide, res, st_provide_weight, st_demand_weight)
        weight = tools.result(weight)
        print("scipy满意度:", weight)
        with open(current_path + '/../satisfy/LPESCP.txt', 'a', encoding='UTF - 8') as f:
            f.write(str(weight) + '\n')
        return Provide, res, weight

    else:
        # for i in range(len(Demand)):
        #     weight += (1 - 1 / (st_demand_weight[i] + 1))
        weight = tools.sum_weight(Provide, Demand, res, Demand, st_provide_weight, st_demand_weight)
        weight = tools.result(weight)
        print("scipy满意度:", weight)
        with open(current_path + '/../satisfy/LPESCP.txt', 'a', encoding='UTF - 8') as f:
            f.write(str(weight) + '\n')
        return res, Demand, weight