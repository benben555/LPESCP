from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpStatus
import math

# 创建问题实例
problem = LpProblem("Square Root Example", LpMinimize)

# 创建变量
x = LpVariable('x', lowBound=0)

# 设置目标函数
problem += lpSum([math.sqrt(x)])

# 添加约束条件
problem += x >= 16

# 求解问题
status = problem.solve()

# 打印最优解和最优值
if status == 1:
    print("最优解: x =", x.value())
    print("最优值:", math.sqrt(x.value()))
else:
    print("无法找到最优解")

# 打印问题状态
print("问题状态:", LpStatus[status])