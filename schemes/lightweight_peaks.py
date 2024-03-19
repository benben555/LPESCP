import random
import time

from charm.core.math.elliptic_curve import elliptic_curve
from charm.toolbox.eccurve import prime192v2
from charm.toolbox.ecgroup import ECGroup, ZR, G
import tools


# from backup import paillier


def SystemSetup():
    group = ECGroup(prime192v2)
    P = group.random(G)
    q = group.order()
    KW_space = ["urgent", "normal", "anyway"]
    EC = {"urgent": 10, "normal": 20, "anyway": 30, "other": 40, 'a': 21, 'b': 22, 'c': 33, 'abc': 45, 'age': 29}
    GSP = {'G': group, 'P': P, 'q': q, 'KW_space': KW_space, 'EC': EC}
    return GSP


def ServerKeyGen(GSP):
    s = GSP['G'].random(ZR)
    sk_s = s
    pk_s = GSP['P'] ** s
    kw = random.choice(list(GSP['EC']))
    # EC_U = GSP['EC'][kw]
    # c1=pai.encipher(str(RC_U))
    return (sk_s, pk_s)


# def UserKeyGen(GSP):
#     a1, a2 = GSP['G'].random(ZR), GSP['G'].random(ZR)
#     sk_A = (a1, a2)
#     pk_A1, pk_A2 = GSP['P'] ** a1, GSP['P'] ** a2
#     pk_A = (pk_A1, pk_A2)
#     return (sk_A, pk_A)
def UserKeyGen(GSP):
    a1, a2 = GSP['G'].random(ZR), GSP['G'].random(ZR)
    sk_A = (a1, a2)
    print(type(a1))
    print(a1)
    pk_A1, pk_A2 = GSP['P'] ** a1, GSP['P'] ** a2
    print(type(pk_A1))
    print(pk_A1)
    print()
    pk_A = (pk_A1, pk_A2)
    pai = tools.Paillier()
    pai.__key_gen__()
    g_U, N_U = pai.pubKey[1], pai.pubKey[0]
    lam_U = pai.priKey[0]
    W_U = GSP['G'].random(ZR)
    RC_U = random.randint(1, 50)
    P_U = pai.encipher(str(RC_U))
    return sk_A, pk_A, g_U, N_U, lam_U, RC_U, P_U, pai


def IndexCiphertextGen(GSP, kw, pk_s, sk_A, pk_A, pk_B):
    pk_A1, pk_A2 = pk_A
    sk_A1, sk_A2 = sk_A
    pk_B1, pk_B2 = pk_B
    lambda1 = GSP['G'].hash((pk_A1, pk_B1, pk_B1 ** sk_A1))
    lambda2 = GSP['G'].hash((pk_A2, pk_B2, pk_B2 ** sk_A2))
    r = GSP['G'].random(ZR)
    Q = GSP['P'] ** r * (pk_B1 ** GSP['G'].hash((kw, lambda1, lambda2))) ** r
    IC1 = pk_s ** r
    IC2 = GSP['G'].hash(Q)
    IC_kw = (IC1, IC2)
    return IC_kw


def SearchTrapdoorGen(GSP, kw, pk_A, sk_B, pk_B):
    pk_A1, pk_A2 = pk_A
    sk_B1, sk_B2 = sk_B
    pk_B1, pk_B2 = pk_B
    lambda1 = GSP['G'].hash((pk_A1, pk_B1, pk_A1 ** sk_B1))
    lambda2 = GSP['G'].hash((pk_A2, pk_B2, pk_A2 ** sk_B2))
    ST_kw = GSP['G'].hash((kw, lambda1, lambda2), ZR) * sk_B1
    return ST_kw


def MatchTest(GSP, sk_s, IC_kw, ST_kw):
    IC1, IC2 = IC_kw
    Q = IC1 ** (sk_s ** -1) * (IC1 ** ST_kw) ** (sk_s ** -1)
    return IC2 == GSP['G'].hash(Q)


for i in range(5):
    start = time.perf_counter()
    GSP = SystemSetup()
    sk_s, pk_s = ServerKeyGen(GSP)
    # UserKeyGen(GSP)
    r1 = "123"
    r1 = r1.zfill(20)
    temp = r1.encode('utf-8')
    r1 = GSP['G'].encode(temp)
    r = GSP['G'].zr(r1)
    b = GSP['P'] ** r
    print(GSP['G'].serialize(b).decode('utf-8'))

    r1 = "321"
    r1 = r1.zfill(20)
    temp = r1.encode('utf-8')
    r1 = GSP['G'].encode(temp)
    r = GSP['G'].zr(r1)
    b = GSP['P'] ** r
    print(GSP['G'].serialize(b).decode('utf-8'))
#     sk_B, pk_B = UserKeyGen(GSP)
#     IC_kw = IndexCiphertextGen(GSP, "urgent", pk_s, sk_A, pk_A, pk_B)
#     ST_kw = SearchTrapdoorGen(GSP, "urgent", pk_A, sk_B, pk_B)
#     print(MatchTest(GSP, sk_s, IC_kw, ST_kw))
#     end = time.perf_counter()
#     print('Running time: %s Seconds' % (end - start))
#     with open('lightweight_peaks.txt', 'a', encoding='UTF - 8') as f:
#         data = f.write(str(end - start) + "\n")
