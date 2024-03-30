import random

from Scheduling import LPESCP
from charm.schemes.pkenc.pkenc_rsa import RSA_Enc
from schemes import lightweight_peaks as peaks
import tools
from random import choice, randint


class User:
    def __init__(self, sk_u, pk_u, g_u, n_u, lam_u, rc_u, p_u, pai=tools.Paillier(), power=0, weight=0, C2=0):
        self.SK_U = sk_u
        self.PK_U = pk_u
        self.P_U = p_u
        self.lam_U = lam_u
        self.g_U = g_u
        self.N_U = n_u
        self.RC_U = rc_u
        self.Pai = pai
        self.Power = power
        self.Weight = weight
        self.C2 = C2


user = {}  # 用户字典集合
ciphertext = {}  # 密文字典集合
rsa = RSA_Enc()
(public_key, private_key) = rsa.keygen(1024)
# KW_space = ["1", "2", "3", "normal", "urgent"]
# EC = {"urgent": 5, "normal": 4, "1": 1, "2": 2, '3': 3}
for i in range(500):
    ICs = {}  # 数据集中器存储的密文集合
    KWs = {}
    STs = {}  # 数据集中器存储的陷门集合
    # 电力公司
    GSP = peaks.SystemSetup()
    Demand = []  # 电力公司统计的需求电量列表
    Provide = []  # 电力公司统计的供给电量列表
    st_demand = []  # 电力公司统计的需求用户ID列表
    st_provide = []  # 电力公司统计的供给用户ID列表
    st_demand_weight = []  # 电力公司统计的需求权重列表
    st_provide_weight = []  # 电力公司统计的供给权重列表
    # 数据集中器
    sk_s, pk_s = peaks.ServerKeyGen(GSP)

    # 用户注册
    a = randint(8, 15)
    b = 20 - a
    c = randint(3, 8)
    sk_B, pk_B, g_B, N_B, lam_B, RC_B, P_B, pai_B = peaks.UserKeyGen(GSP)
    user[0] = User(sk_B, pk_B, g_B, N_B, lam_B, RC_B, P_B, pai=pai_B)
    for j in range(1, 21):
        sk_u, pk_u, g_U, N_U, lam_U, RC_U, P_U, pai = peaks.UserKeyGen(GSP)
        user[j] = User(sk_u, pk_u, g_U, N_U, lam_U, RC_U, P_U, pai=pai)
    power, weight = tools.Gen_data(user, a, b)

    # 用户发送密文
    for ID in range(1, 21):
        KWs[ID] = choice(list(GSP['EC']))
        plain_text = str(power[ID]).encode()
        text_encrypted = rsa.encrypt(public_key, plain_text)
        # print('user:', ID, '密文：', text_encrypted)
        IC_kw = peaks.IndexCiphertextGen(GSP, KWs[ID], pk_s, user[ID].SK_U, user[ID].PK_U, pk_B)
        ciphertext[ID] = text_encrypted
        ICs[ID] = IC_kw
        # 电力公司发送trapdoor
        kw1 = KWs[ID]
        ST_kw = peaks.SearchTrapdoorGen(GSP, kw1, user[ID].PK_U, sk_B, pk_B)
        STs[ID] = ST_kw

    # 数据集中器
    for ID in ICs:
        ST_kw = STs[ID]
        if peaks.MatchTest(GSP, sk_s, ICs[ID], ST_kw):
            # print("匹配成功,转发解密")
            kw = KWs[ID]
            temp = round(random.uniform(GSP['EC'][kw], GSP['EC'][kw] + 1), 2)
            text_decrypted = rsa.decrypt(public_key, private_key, ciphertext[ID])
            # print('明文：', text_decrypted.decode())
            if text_decrypted.decode()[0] == '-':
                Provide.append(eval(text_decrypted.decode()[1:]))
                st_provide.append(ID)
                st_provide_weight.append(user[ID].Weight*0.8+0.2*temp)
            else:
                Demand.append(eval(text_decrypted.decode()))
                st_demand.append(ID)
                st_demand_weight.append(user[ID].Weight*0.8+0.2*temp)
        else:
            print("匹配失败,下一个")
    print("provide", Provide)
    print(st_provide_weight)
    print(round(sum(Provide), 2))
    print("demand:", Demand)
    print(st_demand_weight)
    print(round(sum(Demand), 2))
    # 电力公司
    print("\n")
    print("LPESCP")
    st_true3_provide, st_true3_demand, quota3 = tools.sum_weight(Provide, Demand, st_provide_weight, st_demand_weight)
    print("最后每个供电用户供给的电量为", st_true3_provide)
    print("最后每个需求用户得到的电量为", st_true3_demand)
    print("LPESCP满意度 is", quota3)
