import numpy as np
from scipy.optimize import minimize, LinearConstraint, NonlinearConstraint

def objective(x, st_provide_weight, Provide):
    S_terms = [
        (st_provide_weight[i] / (st_provide_weight[i] + 1)) * np.sqrt(np.maximum(1 - x[i] / Provide[i], 0))
        for i in range(S_num)
    ]
    return -np.sum(S_terms)

def constraint(x):
    S_sum = np.sum(x[:S_num])
    D_sum = np.sum(Demand)
    return S_sum - D_sum

def nonlinear_constraint(x):
    constraints = []
    for j in range(S_num):  # Update the range
        constraints.append(x[j] - Provide[j])
    constraints.append(np.sum(Demand) - np.sum(x[:S_num]))
    return constraints

# Initialize variables
D_num = 8
S_num = 12
st_provide_weight = np.array([6.85, 1.11, 6.42, 9.65, 7.56, 0.86, 4.14, 8.72, 4.26, 5.89, 8.68,3.62])
# st_demand_weight=p_D = [9.1, 5.35, 5.02, 8.88, 6.58, 7.78, 5.88, 4.79]
Provide = np.array([3.96, 63.13, 21.93, 33.01, 74.19, 20.65, 39.05, 21.7, 66.05, 46.86, 14.79, 61.04])
Demand = np.array([53.62, 65.52, 25.82, 83.49, 15.72, 8.15, 74.24, 16.77])

# Define constraints
linear_constraint = LinearConstraint(np.eye(S_num), 0, np.inf)
nonlinear_constraint = NonlinearConstraint(nonlinear_constraint, -np.inf, 0)

# Initial guess
x0 = np.zeros(S_num)  # Update the length

# Define optimization problem
problem = {
    'fun': lambda x: objective(x, st_provide_weight, Provide),
    'x0': x0,
    'constraints': [linear_constraint, nonlinear_constraint],
    'bounds': [(0, p) for p in Provide],  # Variable bounds based on Provide
    'options': {'disp': True}
}

# Solve the optimization problem
solution = minimize(**problem)

# Extract the optimal solution
opt_solution = solution.x[:S_num]  # Extract only the supply variables
print("供电：",np.around(solution.x[:S_num], decimals=2))
print("Optimal solution:", opt_solution)


'''
        def objective(x, st_provide_weight, Provide):
            S_terms = [
                (st_provide_weight[i] / (st_provide_weight[i] + 1)) * (
                    np.sqrt(np.maximum(1 - x[i] / Provide[i], 0)) if Provide[i] != 0 else 0) for
                i in range(S_num)]
            return -(sum(S_terms))


        # 非线性约束条件：D <= Demand, S <= Provide
        def nonlinear_constraint(x):
            constraints=(sum(Demand) - np.sum(x[:S_num]))
            return constraints

        # 定义约束条件
        linear_constraint = LinearConstraint(np.eye(S_num), 0, Provide)
        nonlinear_constraint = NonlinearConstraint(nonlinear_constraint, 0, 0)
        # 初始猜测值
        x0 = np.full(S_num, np.mean(Provide))

        # 定义优化问题
        problem = {
            'fun': lambda x: objective(x, st_provide_weight, Provide),
            'x0': x0,
            'constraints': [linear_constraint, nonlinear_constraint],
            'bounds': [(0, p) for p in Provide],
            'options': {'disp': True}
        }

        # 调用优化器求解问题
        solution = minimize(**problem)
'''
'''
import numpy as np
from scipy.optimize import minimize, LinearConstraint

def objective(x, st_provide_weight, Provide):
    S_terms = [
        (st_provide_weight[i] / (st_provide_weight[i] + 1)) * np.sqrt(np.maximum(1 - x[i] / Provide[i], 0))
        for i in range(S_num)
    ]
    return -np.sum(S_terms)

# Define constraints
A = np.eye(S_num)
b = np.zeros(S_num)
A_eq = np.ones((1, S_num))
b_eq = np.sum(Demand)

linear_constraint = LinearConstraint(np.vstack((A, A_eq)), np.concatenate((b, b_eq)), Provide)

# Initial guess
x0 = np.full(S_num, np.mean(Provide))

# Define optimization problem
problem = {
    'fun': lambda x: objective(x, st_provide_weight, Provide),
    'x0': x0,
    'constraints': linear_constraint,
    'bounds': [(0, p) for p in Provide],
    'options': {'disp': True}
}

# Solve the optimization problem
solution = minimize(**problem)

'''