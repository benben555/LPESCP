import numpy as np
from scipy.optimize import minimize, NonlinearConstraint, LinearConstraint
D_num = 8
S_num = 12
D_max = [53.62, 65.52, 25.82, 83.49, 15.72, 8.15, 74.24, 16.77]
p_D = [9.1, 5.35, 5.02, 8.88, 6.58, 7.78, 5.88, 4.79]
S_max = [3.96, 63.13, 21.93, 33.01, 74.19, 0, 39.05, 21.7, 66.05, 46.86, 14.79, 61.04]
p_S = [6.85, 1.11, 6.42, 9.65, 7.56, 0.86, 4.14, 8.72, 4.26, 5.89, 8.68]
def objective(x):
    S_terms = [
        (p_S[i] / (p_S[i] + 1)) * (
            np.sqrt(np.maximum(1 - x[i] / S_max[i], 0)) if S_max[i] != 0 else 0) for
        i in range(S_num)]
    return -(sum(S_terms))


# 约束条件
def constraint1(x):
    S_sum = np.sum(x[:S_num])
    D_sum = sum(D_max)
    return D_sum - S_sum


# 非线性约束条件：D <= Demand, S <= Provide
def nonlinear_constraint(x):
    constraints = []
    for j in range(S_num):
        constraints.append(x[j] - S_max[j])
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
    'constraints': [constraint1, linear_constraint, nonlinear_constraint],
    'bounds': [(0, None)] * S_num,
    'options': {'disp': True}
}

# 调用优化器求解问题
solution = minimize(**problem)
