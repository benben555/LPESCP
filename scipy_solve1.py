import numpy as np
from scipy.optimize import minimize, NonlinearConstraint, LinearConstraint
import random

import tools

# 随机生成参数
D_num = 9
S_num = 11
D_max = [98.85, 26.31, 35.37, 0.8, 62.02, 73.1, 75.36, 86.27, 14.43]
p_D = [5.24, 2.01, 8.88, 5.82, 2.3, 0.24, 6.11, 4.88, 9.37]
S_max = [76.2, 70.3, 27.43, 89.74, 18.65, 39.7, 42.68, 46.28, 32.47, 1.02, 47.03]
p_S = [6.85, 1.11, 6.42, 9.65, 7.56, 0.86, 4.14, 8.72, 4.26, 5.89, 8.68]


# 目标函数
# def objective(x):
#     D_terms = [(x[i] / (x[i] + 1)) * np.sqrt(np.maximum(x[i] / D_max[i], 0)) for i in range(D_num)]
#     S_terms = [(x[D_num + j] / (x[D_num + j] + 1)) * np.sqrt(np.maximum(1 - x[D_num + j] / S_max[j], 0)) for j in range(S_num)]
#     return -(sum(D_terms) + sum(S_terms))
#
# # 约束条件
# def constraint(x):
#     D_sum = np.sum(x[:D_num])
#     S_sum = np.sum(x[D_num:])
#     return D_sum - S_sum
#
# # 非线性约束条件：D <= D_max, S <= S_max
# def nonlinear_constraint(x):
#     constraints = []
#     for i in range(D_num):
#         constraints.append(x[i] - D_max[i])
#     for j in range(S_num):
#         constraints.append(x[D_num + j] - S_max[j])
#     constraints.append(np.sum(x[:D_num]) - np.sum(x[D_num:]))
#     return constraints
#
# # 定义约束条件
# linear_constraint = LinearConstraint(np.eye(D_num + S_num), 0, np.inf)
# nonlinear_constraint = NonlinearConstraint(nonlinear_constraint, -np.inf, 0)
# # 初始猜测值
# x0 = np.concatenate((p_D, p_S))
#
# # 定义优化问题
# problem = {
#     'fun': objective,
#     'x0': x0,
#     'constraints': [linear_constraint, nonlinear_constraint],
#     'bounds': [(0, None)] * (D_num + S_num),
#     'options': {'disp': True}
# }
#
# # 调用优化器求解问题
# solution = minimize(**problem)

# 打印结果
def objective(x):
    S_terms = [
        (p_S[i] / (p_S[i] + 1)) * (
            np.sqrt(np.maximum(1 - x[i] / S_max[i], 0)) if S_max[i] != 0 else 0) for
        i in range(S_num)]
    return -(sum(S_terms))


# 约束条件
def constraint(x):
    S_sum = np.sum(x[:S_num])
    D_sum = sum(D_max)
    return S_sum - D_sum


# 非线性约束条件：D <= Demand, S <= Provide
def nonlinear_constraint(x):
    constraints = []
    for j in range(S_num):
        constraints.append(x[j] - S_max[j])
    constraints.append(sum(D_max) - np.sum(x[:S_num]))
    return constraints


# 定义约束条件
linear_constraint = LinearConstraint(np.eye(S_num), 0, np.inf)
nonlinear_constraint = NonlinearConstraint(nonlinear_constraint, -np.inf, 0)
# 初始猜测值
x0 = p_S

# 定义优化问题
problem = {
    'fun': objective,
    'x0': x0,
    'constraints': [linear_constraint, nonlinear_constraint],
    'bounds': [(0, None)] * S_num,
    'options': {'disp': True}
}

# 调用优化器求解问题
solution = minimize(**problem)
weight=-solution.fun
if sum(S_max) < sum(D_max):
    weight = tools.result(weight)
    print("scipy满意度:", weight)
else:
    for i in range(len(D_max)):
        weight += (1 - 1 / (p_D[i] + 1))
    weight = tools.result(weight)
    print("scipy满意度:", weight)
print("Optimal solution:")
print("需电：",np.around(solution.x[:D_num], decimals=2))
print(sum(solution.x[:D_num]))
print("供电：",np.around(solution.x[D_num:], decimals=2))
print(sum(solution.x[D_num:]))
print("Objective value at the optimal solution:")
print(-solution.fun)  # 取负数以还原最大化结果
