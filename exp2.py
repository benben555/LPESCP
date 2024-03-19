"""
    考虑K=kG ，其中K、G为椭圆曲线Ep(a,b)上的点，n为G的阶（nG=O∞ ），k为小于n的整数。
    则给定k和G，根据加法法则，计算K很容易但反过来，给定K和G，求k就非常困难。
    因为实际使用中的ECC原则上把p取得相当大，n也相当大，要把n个解点逐一算出来列成上表是不可能的。
    这就是椭圆曲线加密算法的数学依据
    点G称为基点（base point）
    k（k<n）为私有密钥（private key）
    K为公开密钥（public key)
"""
import math
import random
import numpy as np
import matplotlib.pyplot as plt

import tools
from dispatch import MaxMinFair, OnlyWeight, Pulp


class User:
    def __init__(self, P_U1_x, P_U1_y, P_U2_x, P_U2_y, P_U3, g_U, N_U, MC_U, Cert=0, Qu=None):
        self.P_U1_x = P_U1_x
        self.P_U1_y = P_U1_y
        self.P_U3 = P_U3
        self.P_U2_x = P_U2_x
        self.P_U2_y = P_U2_y
        self.PK_U1 = (P_U1_x, P_U1_y)
        self.PK_U2 = (P_U2_x, P_U2_y)
        self.g_U = g_U
        self.N_U = N_U
        self.MC_U = MC_U
        self.Cert = Cert
        self.Qu = Qu


class Spm:
    def __init__(self, a, b, q, p, G_x, G_y, P_pub_x, P_pub_y):
        self.a = a
        self.b = b
        self.q = q
        self.p = p
        self.G_x = G_x
        self.G_y = G_y
        self.P = (G_x, G_y)
        self.P_pub_x = P_pub_x
        self.P_pub_y = P_pub_y
        self.P_pub = (P_pub_x, P_pub_y)


user = {}
ming = {}
ciphertext = {}

for i in range(500):

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
        print("less", st_max_provide)
        print(sum(st_max_provide))
        for i in range(len(st_max_provide)):
            st_max_provide[i] = max(round(st_max_provide[i] + (0.9 * total_demand - sum(st_max_provide)) / b, 2), 0)
    if sum(st_max_provide) > 1.1 * total_demand:
        print("more", st_max_provide)
        print(sum(st_max_provide))
        for i in range(len(st_max_provide)):
            st_max_provide[i] = max(round(st_max_provide[i] - (sum(st_max_provide) - 1.1 * total_demand) / b, 2), 0)
    cap = round(sum(st_max_provide), 2)
    print("\n\n")
    print("有", a, "个需求用户")
    print("各自的用电要求分别是", st_max_demand)
    print("各自的权重分别是", st_demand_weight)
    print("有", b, "个供电用户")
    print("各自的最大供电量分别是", st_max_provide)
    print("各自的权重分别是", st_provide_weight)
    print("\n\n")
    print("总供电量是", round(cap, 2))
    print("总需电量是", round(total_demand, 2))
    print("WMMF")
    st_true_provide, st_true_demand, quota1 = MaxMinFair.Weight(st_max_provide, st_max_demand, st_provide_weight, st_demand_weight)
    print("\n")
    print("PIPO")
    st_true2_provide, st_true2_demand, quota2 = OnlyWeight.only_weight(st_max_provide, st_max_demand, st_provide_weight,
                                                                       st_demand_weight)
    print("\n")
    print("LPESCP")
    st_true3_provide, st_true3_demand, quota3 = Pulp.pulp(st_max_provide, st_max_demand, st_provide_weight, st_demand_weight)
    print("最后每个供电用户供给的电量为", st_true3_provide)
    print("最后每个需求用户得到的电量为", st_true3_demand)
    print("linear满意度 is", quota3)
    # print(quota2 <= quota3 and quota1 <= quota3)
    # print(tools.ceil2(sum(st_true_provide)) >= tools.floor2(sum(st_true_demand)))
    # print(tools.ceil2(sum(st_true2_provide)) >= tools.floor2(sum(st_true2_demand)))
    # print(tools.ceil2(sum(st_true3_provide)) >= tools.floor2(sum(st_true3_demand)))