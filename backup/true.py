import math
import random

import numpy as np
from charm.schemes.pkenc.pkenc_rsa import RSA_Enc
from charm.toolbox.eccurve import prime192v2
from charm.toolbox.ecgroup import ECGroup, ZR, G
from matplotlib import pyplot as plt

import paillier


class User:
    def __init__(self, P_U1, P_U2, P_U3, g_U, N_U, MC_U, Cert=0, Qu=None, pai=paillier.Paillier()):
        self.PK_U1 = P_U1
        self.PK_U3 = P_U3
        self.PK_U2 = P_U2
        self.g_U = g_U
        self.N_U = N_U
        self.MC_U = MC_U
        self.Cert = Cert
        self.PK_U4 = Qu
        self.Pai = pai


class Prikey:
    def __init__(self, SK_U1, SK_U2, lam_U):
        self.SK_U1 = SK_U1
        self.SK_U2 = SK_U2
        self.lam_U = lam_U


class Ciphertext:
    def __init__(self, id_u, message):
        self.id_u = id_u
        self.message = message


user = {}
ming = {}
prikey = {}
ciphertext = {}
group = ECGroup(prime192v2)
trials = 10
g = group.random(G)
SPM = {}
SMK = {}


def SystemSetup():
    print("SystemSetup:")
    P = group.random(G)
    lam = group.random(ZR)
    P_pub = P ** lam
    ID_space = [i for i in range(20)]
    KW_space = ["urgent", "normal", "anyway"]
    KC = {"urgent": 1, "normal": 2, "anyway": 3}
    SPM = {'P': P, 'ID_space': ID_space, 'KW_space': KW_space, 'P_pub': P_pub, 'KC': KC}
    SMK = {'lam': lam}
    return (SPM, SMK)


def KeyGen(SPM, IDu):
    SK_U1 = group.random(ZR)
    SK_U2 = group.random(ZR)
    P_U1 = SPM['P'] ** SK_U1
    P_U2 = SPM['P'] ** SK_U2
    pai = paillier.Paillier()
    pai.__key_gen__()
    g_U, N_U = pai.pubKey[1], pai.pubKey[0]
    lam_U = pai.priKey[0]
    MC_U = group.random(ZR)
    RC_U = group.random(ZR)
    P_U3 = pai.encipher(str(RC_U))

    user[IDu] = User(P_U1, P_U2, P_U3, g_U, N_U, MC_U, pai=pai)
    prikey[IDu] = Prikey(SK_U1, SK_U2, lam_U)


def UserCertify(SPM, SMK, IDu):
    print("UserCertify：")
    Beta_U = group.random(ZR)
    Q_U = SPM['P'] ** Beta_U
    user[IDu].PK_U4 = Q_U
    # PK_U = Pu + Qu
    Cert_U = Beta_U + group.hash((IDu, user[IDu].PK_U1, user[IDu].PK_U2, user[IDu].PK_U4)) * SMK['lam']
    user[IDu].Cert = Cert_U


def KeywordEnc(SPM, kw, IDA, IDB):
    print("KeywordEnc:")
    if kw not in SPM['KW_space']:
        print("please add the kw into KW_space")
        return
    KC_KW = SPM['KC'][kw]
    # PK_B1, PK_B2, PK_B3 = user[IDB].PK_U1, user[IDB].PK_U2, user[IDB].Qu
    # SK_A1 = group.random(ZR)
    # SK_A2 = group.random(ZR)
    r = group.random(ZR)
    C1 = SPM['P'] ** r
    tao = user[IDB].PK_U1 ** prikey[IDA].SK_U1
    RB = user[IDB].PK_U2 * user[IDB].PK_U4 * (
            SPM['P_pub'] ** group.hash((IDB, user[IDB].PK_U1, user[IDB].PK_U2, user[IDB].PK_U4)))
    miu = RB ** (r * group.hash((IDA, IDB, tao, kw)))
    s = group.random(ZR)
    C2 = s * ((prikey[IDA].SK_U2 + user[IDA].Cert) ** -1)
    v = SPM['P'] ** s
    t = group.random(ZR)
    # t = int(input("请输入私钥t（<{}）：".format(SPM.q)))
    print("miu:", miu)
    C3 = t - group.hash((miu, v))
    C4 = group.hash((C1, C2, C3, t))
    C5 = user[IDA].Pai.encipher(str(KC_KW))  # problem
    print("C1, C2, C3", C1, C2, C3)
    return C1, C2, C3, C4, C5


def TrapdoorGen(SPM, kw, IDA, IDB):
    print("TrapdoorGen:")
    PK_A1 = user[IDA].PK_U1
    PK_A2 = user[IDA].PK_U2
    PK_A4 = user[IDA].PK_U4
    SK_B1 = prikey[IDB].SK_U1
    SK_B2 = prikey[IDB].SK_U2
    tao2 = PK_A1 ** SK_B1
    TD1 = group.hash((IDA, IDB, tao2, kw)) * (SK_B2 + user[IDB].Cert)
    TD2 = PK_A2 * PK_A4 * (SPM['P_pub'] ** group.hash((IDA, PK_A1, PK_A2, PK_A4)))
    TD3 = 1  # problem
    return TD1, TD2, TD3


def MatchTest(SPM, C1, C2, C3, C4, TD1, TD2):
    print("MatchTest:")
    t = C3 + group.hash((C1 ** TD1, TD2 ** C2))
    return C4 == group.hash((C1, C2, C3, t))


# def check_Cert(IDu, SPM):  # (a,b,q,p) + P + P_pub
#     temp1, temp2 = get_ng(SPM.P_pub_x, SPM.P_pub_y, (f1(IDu, user[IDu].PK_U1, user[IDu].PK_U2, user[IDu].Qu)) % SPM.q,
#                           SPM.a, SPM.p)
#     return get_np(user[IDu].Qu[0], user[IDu].Qu[1], temp1, temp2, SPM.a, SPM.p) == get_ng(SPM.G_x, SPM.G_y,
#                                                                                           user[IDu].Cert,
#                                                                                           SPM.a, SPM.p)

rsa = RSA_Enc()
(public_key, private_key) = rsa.keygen(1024)
if __name__ == "__main__":
    # 加密
    # text = input("use：请输入需要加密的字符串:")
    # text_encrypted_base64 = rsa.encryption(text, public_key)
    # print('密文：', text_encrypted_base64)

    # 解密
    # text_decrypted = rsa.decryption(text_encrypted_base64, private_key)
    # print('明文：', text_decrypted)
    a = random.randint(8, 15)
    b = 20 - a
    SPM, SMK = SystemSetup()
    for i in range(20):
        KeyGen(SPM, i)
    # SMK = int(input("电力公司：请输入主私钥SMK的值："))
    for i in range(20):
        UserCertify(SPM, SMK, i)
        # print(check_Cert(i, SPM))
    kw = "urgent"
    # kw = input("user：请输入关键字:")
    # plain_text = input("user：请输入需要加密的字符串:")
    plain_text = b'hello world'
    # text_encrypted = rsa.encrypt(public_key, plain_text.encode())
    text_encrypted = rsa.encrypt(public_key, plain_text)
    print('密文：', text_encrypted)
    # ming[kw] = plain_text
    # IDA = random.randint(1, 20)
    # while True:
    #     IDB = random.randint(1, 20)
    #     if IDA != IDB:
    #         break
    IDA = 0
    IDB = 1
    C1, C2, C3, C4, C5 = KeywordEnc(SPM, kw, IDA, IDB)
    kw1 = input("user：请输入关键字kw1:")
    TD1, TD2, TD3 = TrapdoorGen(SPM, kw1, IDA, IDB)
    if MatchTest(SPM, C1, C2, C3, C4, TD1, TD2):
        print("转发解密")
        text_decrypted = rsa.decrypt(public_key, private_key, text_encrypted)
        print('明文：', text_decrypted)
    else:
        print("下一个")

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
    title2 = '供小于求时供电用户能源调度图'
    title4 = '供小于求时需电用户能源调度图'
    if cap > total_demand:
        title2 = '供大于求时供电用户能源调度图'
        title4 = '供大于求时需电用户能源调度图'
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
    with open('../data.txt', 'a', encoding='UTF - 8') as f:
        data = f.write(strs)
    # x轴坐标, a=5, 返回[0, 1, 2, 3, 4]
    x = np.arange(1, 1 + a)
    # x轴坐标, a=5, 返回[0, 1, 2, 3, 4]
    x1 = np.arange(1, 1 + b)
    fig = plt.figure(figsize=(10, 9))
    plt.subplots_adjust(left=None, bottom=0.15, right=None, top=None, wspace=0.3, hspace=0.5)
    ax1 = fig.add_subplot(2, 2, 1)
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei显示中文\n",
    plt.title('供电用户权重图')  # 添加标题\n",
    plt.xlabel('供电用户编号')  # 添加横轴标签\n",
    plt.ylabel('权重')  # 添加y轴名称\n",
    ax1.bar(x1, st_provide_weight, label="供电用户所占的权重")
    for a, b in zip(x1, st_provide_weight):
        plt.text(a, b, '%.2f' % b, ha='center', va='bottom', fontsize=10)
    plt.legend(loc=1, bbox_to_anchor=(1.1, 1.3), borderaxespad=1.7)
    ax2 = fig.add_subplot(2, 2, 2)
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
    ax3 = fig.add_subplot(2, 2, 3)
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei显示中文\n",
    plt.title('需电用户权重图')  # 添加标题\n",
    plt.xlabel('需电用户编号')  # 添加横轴标签\n",
    plt.ylabel('权重')  # 添加y轴名称\n",
    ax3.bar(x, st_demand_weight, label="需电用户所占的权重")
    for a, b in zip(x, st_demand_weight):
        plt.text(a, b, '%.2f' % b, ha='center', va='bottom', fontsize=10)
    plt.legend(loc=1, bbox_to_anchor=(1.1, 1.3), borderaxespad=1.7)
    ax4 = fig.add_subplot(2, 2, 4)
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
    ax4.bar(x, st_max_demand, width=width, label="用户的需求电量")
    ax4.bar(x + width, st_true_demand, width=width, label="用户实际得到的电量")
    # 显示图例
    plt.legend(loc=1, bbox_to_anchor=(1.1, 1.4), borderaxespad=1.7)
    # 显示柱状图
    plt.show()
