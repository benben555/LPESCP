import math
import random
import time
import numpy as np
from charm.core.math.elliptic_curve import serialize, order
from charm.schemes.pkenc.pkenc_rsa import RSA_Enc
from charm.toolbox.eccurve import prime192v2
from charm.toolbox.ecgroup import ECGroup, ZR, G

group = ECGroup(prime192v2)


def SystemSetup():
    P = group.random(G)
    lam = group.random(ZR)
    P_pub = P ** lam
    SPM = {'P': P, 'P_pub': P_pub}
    SMK = {'lam': lam}
    return SPM, SMK


def KeyGen(SPM, IDu):
    SK_U1 = group.random(ZR)
    SK_U2 = group.random(ZR)
    SK_U = (SK_U1, SK_U2)
    P_U1 = SPM['P'] ** SK_U1
    P_U2 = SPM['P'] ** SK_U2
    P_U = (P_U1, P_U2)
    return SK_U, P_U


def UserCertify(SPM, SMK, IDu, P_U):
    Beta_U = group.random(ZR)
    Q_U = SPM['P'] ** Beta_U
    P_U1, P_U2 = P_U
    PK_U = (P_U1, P_U2, Q_U)
    Cert_U = Beta_U + group.hash((IDu, P_U1, P_U2, Q_U)) * SMK['lam']
    return PK_U, Cert_U


def KeywordEnc(SPM, kw, IDA, SK_A, Cert_A, IDB, PK_B):
    PK_B1, PK_B2, PK_B3 = PK_B
    SK_A1, SK_A2 = SK_A
    r = group.random(ZR)
    C1 = SPM['P'] ** r
    tao = PK_B1 ** SK_A1
    RB = PK_B2 * PK_B3 * (SPM['P_pub'] ** group.hash((IDB, PK_B1, PK_B2, PK_B3)))
    miu = RB ** (r * group.hash((IDA, IDB, tao, kw)))
    s = group.random(ZR)
    C2 = s * ((SK_A2 + Cert_A) ** -1)
    v = SPM['P'] ** s
    t = group.random(ZR)
    C3 = t - group.hash((miu, v))
    C4 = group.hash((C1, C2, C3, t))
    Ckw = (C1, C2, C3, C4)
    return Ckw


def TrapdoorGen(SPM, kw, IDA, PK_A, IDB, SK_B, Cert_B):
    PK_A1, PK_A2, PK_A3 = PK_A
    SK_B1, SK_B2 = SK_B
    tao2 = PK_A1 ** SK_B1
    TD1 = group.hash((IDA, IDB, tao2, kw)) * (SK_B2 + Cert_B)
    TD2 = PK_A2 * PK_A3 * (SPM['P_pub'] ** group.hash((IDA, PK_A1, PK_A2, PK_A3)))
    TD_kw = (TD1, TD2)
    return TD_kw

# def MatchTest(SPM, Ckw, TD_kw):
def MatchTest(SPM, Ckw, TD_kw, Cert_A, Cert_B, PK_A, PK_B, IDA, IDB):
    PK_B1, PK_B2, PK_B3 = PK_B
    PK_A1, PK_A2, PK_A3 = PK_A
    if PK_A3 * SPM['P_pub'] ** group.hash((IDA, PK_A1, PK_A2, PK_A3)) != SPM['P'] ** Cert_A:
        return False
    if PK_B3 * SPM['P_pub'] ** group.hash((IDB, PK_B1, PK_B2, PK_B3)) != SPM['P'] ** Cert_B:
        return False
    TD1, TD2 = TD_kw
    C1, C2, C3, C4 = Ckw
    t = C3 + group.hash((C1 ** TD1, TD2 ** C2))
    return C4 == group.hash((C1, C2, C3, t))


for i in range(500):
    start = time.perf_counter()
    SPM, SMK = SystemSetup()
    SK_A, P_A = KeyGen(SPM, 1)
    SK_B, P_B = KeyGen(SPM, 2)
    PK_A, Cert_A = UserCertify(SPM, SMK, 1, P_A)
    PK_B, Cert_B = UserCertify(SPM, SMK, 2, P_B)
    Ckw = KeywordEnc(SPM, "urgent", 1, SK_A, Cert_A, 2, PK_B)
    TD_kw = TrapdoorGen(SPM, "urgent", 1, PK_A, 2, SK_B, Cert_B)
    print(MatchTest(SPM, Ckw, TD_kw, Cert_A, Cert_B, PK_A, PK_B, 1, 2))
    # print(MatchTest(SPM, Ckw, TD_kw))
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end - start))
    with open('../scheme_result/CBEKS.txt', 'a', encoding='UTF - 8') as f:
        data = f.write(str(end - start) + "\n")
