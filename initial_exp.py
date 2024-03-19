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

if __name__ == "__main__":
    # 加密
    # text = input("user：请输入需要加密的字符串:")
    # text_encrypted_base64 = rsa.encryption(text, public_key)
    # print('密文：', text_encrypted_base64)

    # 解密
    # text_decrypted = rsa.decryption(text_encrypted_base64, private_key)
    # print('明文：', text_decrypted)
    a = random.randint(8, 15)
    b = 20 - a

    '''# user1生成私钥，小key
    key = int(input("user1：请输入私钥key（<{}）：".format(p)))
    # user1生成公钥，大KEY
    KEY_x, kEY_y = get_ng(G_x, G_y, key, a, q)

    # user2阶段
    # user2拿到user1的公钥KEY，Ep(a,b)阶n，加密需要加密的明文数据
    # 加密准备
    k = int(input("user2：请输入一个整数k（<{}）用于求kG和kQ：".format(p)))
    k_G_x, k_G_y = get_ng(G_x, G_y, k, a, q)  # kG
    k_Q_x, k_Q_y = get_ng(KEY_x, kEY_y, k, a, q)  # kQ
    # 加密
    plain_text = input("user2：请输入需要加密的字符串:")
    plain_text = plain_text.strip()
    # plain_text = int(input("user1：请输入需要加密的密文："))
    c = []
    print("密文为：", end="")
    for char in plain_text:
        intchar = ord(char)
        cipher_text = intchar * k_Q_x
        c.append([k_G_x, k_G_y, cipher_text])
        print("({},{}),{}".format(k_G_x, k_G_y, cipher_text), end="-")

    # user1阶段
    # 拿到user2加密的数据进行解密
    # 知道 k_G_x,k_G_y，key情况下，求解k_Q_x,k_Q_y是容易的，然后plain_text = cipher_text/k_Q_x
    print("\nuser1解密得到明文：", end="")
    for charArr in c:
        decrypto_text_x, decrypto_text_y = get_ng(charArr[0], charArr[1], key, a, q)
        print(chr(charArr[2] // decrypto_text_x), end="")'''
    # a = random.randint(8, 15)
    # b = 20 - a
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
        temp_sums = sum(st_provide_weight)
        temp = [0.0] * b
        for i in range(b):
            temp[i] = round(math.ceil(temp_sums / st_provide_weight[i]), 2)
        while total_demand > 0:
            for i in range(0, b):
                if st_true_provide[i] < st_max_provide[i]:
                    m += temp[i]
            if m == 0:
                break
            mr = total_demand / m
            total_demand = 0
            m = 0
            for i in range(0, b):
                if st_true_provide[i] < st_max_provide[i]:
                    st_true_provide[i] += (mr * temp[i])
                    st_true_provide[i] = round(st_true_provide[i], 2)
                    if st_true_provide[i] > st_max_provide[i]:
                        total_demand += (st_true_provide[i] - st_max_provide[i])
                        st_true_provide[i] = st_max_provide[i]
        print("每个供电用户供给的最大电量为", st_max_provide)
        print("最后每个供电用户供给的电量为", st_true_provide)
    else:
        st_true_provide = st_max_provide
    while cap > 0:
        for i in range(0, a):
            if st_true_demand[i] < st_max_demand[i]:
                n += st_demand_weight[i]
        if n == 0:
            break
        br = cap / n
        cap = 0
        n = 0
        for i in range(0, a):
            if st_true_demand[i] < st_max_demand[i]:
                st_true_demand[i] += (br * st_demand_weight[i])
                st_true_demand[i] = round(st_true_demand[i], 2)
                if st_true_demand[i] > st_max_demand[i]:
                    cap += (st_true_demand[i] - st_max_demand[i])
                    st_true_demand[i] = st_max_demand[i]

    print("最后每个供电用户供给的电量为", st_true_provide)
    print("最后每个需求用户得到的电量为", st_true_demand)
    strs = ''
    strs += "有" + str(a) + "个需求用户\n"
    strs += "各自的用电要求分别是" + str(st_max_demand) + "\n"
    strs += "各自的权重分别是" + str(st_demand_weight) + "\n"
    strs += "有" + str(b) + "个供电用户" + "\n"
    strs += "各自的最大供电量分别是" + str(st_max_provide) + "\n"
    strs += "总供电量是" + str(round(cap, 2)) + "\n"
    strs += "总需电量是" + str(round(sum(st_max_demand), 2)) + "\n"
    strs += "最后每个需求用户得到的电量为" + str(st_true_demand) + "\n\n"
    with open('data.txt', 'a', encoding='UTF - 8') as f:
        data = f.write(strs)
    # x轴坐标, a=5, 返回[0, 1, 2, 3, 4]
    x = np.arange(1, 1 + a)
    # x轴坐标, a=5, 返回[0, 1, 2, 3, 4]
    x1 = np.arange(1, 1 + b)
    fig = plt.figure(figsize=(10, 9))
    plt.subplots_adjust(left=None, bottom=0.15, right=None, top=None, wspace=0.3, hspace=0.5)
    # ax1 = fig.add_subplot(2, 2, 1)
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei显示中文\n",
    # .title('供电用户权重图')  # 添加标题\n",
    # plt.xlabel('供电用户编号')  # 添加横轴标签\n",
    # plt.ylabel('权重')  # 添加y轴名称\n",
    # ax1.bar(x1, st_provide_weight, label="供电用户所占的权重")
    # for a, b in zip(x1, st_provide_weight):
    #     plt.text(a, b, '%.2f' % b, ha='center', va='bottom', fontsize=10)
    # plt.legend(loc=1, bbox_to_anchor=(1.1, 1.3), borderaxespad=1.7)
    ax2 = fig.add_subplot(2, 1, 1)
    total_width, n = 0.8, 2
    # 每种类型的柱状图宽度
    width = total_width / n

    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei显示中文\n",
    plt.title(title2)  # 添加标题\n",
    plt.xlabel('用户编号')  # 添加横轴标签\n",
    plt.ylabel('电量')  # 添加y轴名称\n",
    # 画柱状图
    ax2.bar(x1, st_max_provide, width=width, label="供电用户的最大供电量")
    ax2.bar(x1 + width, st_true_provide, width=width, label="供电用户实际提供的电量")
    plt.legend(loc=1, bbox_to_anchor=(1.1, 1.4), borderaxespad=1.7)
    # ax3 = fig.add_subplot(2, 2, 3)
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei显示中文\n",
    # plt.title('需电用户权重图')  # 添加标题\n",
    # plt.xlabel('需电用户编号')  # 添加横轴标签\n",
    # plt.ylabel('权重')  # 添加y轴名称\n",
    # ax3.bar(x, st_demand_weight, label="需电用户所占的权重")
    # for a, b in zip(x, st_demand_weight):
    #     plt.text(a, b, '%.2f' % b, ha='center', va='bottom', fontsize=10)
    # plt.legend(loc=1, bbox_to_anchor=(1.1, 1.3), borderaxespad=1.7)
    ax4 = fig.add_subplot(2, 1, 2)
    # 重新设置x轴的坐标
    # x = x - (total_width - width) / 2
    # plt.rc('font', size=14)  # 设置图中字号大小\n",
    # plt.figure(figsize=(6, 4))  # 设置画布\n",
    # 有a/b/c三种类型的数据，n设置为3
    total_width, n = 0.8, 2
    # 每种类型的柱状图宽度
    width = total_width / n
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei显示中文\n",
    plt.title(title4)  # 添加标题\n",
    plt.xlabel('用户编号')  # 添加横轴标签\n",
    plt.ylabel('电量')  # 添加y轴名称\n",
    # 画柱状图
    ax4.bar(x, st_max_demand, width=width, label="需电用户的需求电量")
    ax4.bar(x + width, st_true_demand, width=width, label="需电用户实际得到的电量")
    # 显示图例
    plt.legend(loc=1, bbox_to_anchor=(1.1, 1.4), borderaxespad=1.7)
    # 显示柱状图
    plt.show()