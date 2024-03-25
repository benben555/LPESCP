import numpy as np
from scipy.optimize import minimize
import random

# 随机生成参数
D_num = random.randint(8, 15)
S_num = 20 - D_num
D_max = []
p_D = []
S_max = []
p_S = []

for i in range(S_num):
    S_max.append(round(max(0.1, random.random() * 100 - 5), 2))
    p_S.append(round(random.random() * 10, 2))

for i in range(D_num):
    D_max.append(round(random.random() * 100, 2))
    p_D.append(round(random.random() * 10, 2))


# 目标函数
def objective(x):
    D_terms = [(x[i] / (x[i] + 1)) * np.sqrt(np.maximum(x[i] / D_max[i], 0)) for i in range(D_num)]
    S_terms = [(x[D_num + j] / (x[D_num + j] + 1)) * np.sqrt(np.maximum(1 - x[D_num + j] / S_max[j], 0)) for j in
               range(S_num)]
    return -(sum(D_terms) + sum(S_terms))


# 约束条件
def constraint(x):
    D_sum = np.sum(x[:D_num])
    S_sum = np.sum(x[D_num:])
    constraints = [D_sum - S_sum]  # D总和等于S总和约束
    constraints += [x[i] for i in range(D_num)]  # D变量大于零约束
    constraints += [x[D_num + j] for j in range(S_num)]  # S变量大于零约束
    return constraints


# 初始猜测值
x0 = np.concatenate((p_D, p_S))

# 定义优化问题
problem = {
    'fun': objective,
    'x0': x0,
    'constraints': [{'type': 'eq', 'fun': constraint}],
    'options': {'disp': True}
}

# 调用优化器求解问题
solution = minimize(**problem)

# 打印结果
print("Optimal solution:")
print(solution.x)
print("Objective value at the optimal solution:")
print(-solution.fun)  # 取负数以还原最大化结果
