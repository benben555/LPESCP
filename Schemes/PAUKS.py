import time

from charm.core.engine.util import objectToBytes
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, pair, GT

group = PairingGroup("SS512")


def Setup():
    g = group.random(G1)
    p = group.order()
    pp = {'g': g, 'p': p}
    return pp


def KeyGen_R(pp):
    x1 = group.random(ZR)
    x2 = group.random(ZR)
    x3 = group.random(ZR)
    x4 = group.random(ZR)
    pk_R1 = pp['g'] ** x1
    pk_R2 = pp['g'] ** x2
    pk_R3 = pp['g'] ** x3
    sk_R1 = x1
    sk_R2 = x2
    sk_R3 = x3
    sk_R4 = x4
    pk_R = (pk_R1, pk_R2, pk_R3)
    sk_R = (sk_R1, sk_R2, sk_R3, sk_R4)
    return (sk_R, pk_R)


def KeyGen_S(pp):
    y = group.random(ZR)
    pk_S = pp['g'] ** y
    sk_S = y
    return (sk_S, pk_S)


def Enc(pp, sk_S, pk_R, w):
    r1 = group.random(ZR)
    r2 = group.random(ZR)
    pk_R1, pk_R2, pk_R3 = pk_R
    C1 = (pk_R2 ** (group.hash((pk_R1 ** sk_S, w), ZR)) * pk_R3) ** r1
    C2 = pp['g'] ** r1
    obj = {'a': pk_R1 ** sk_S}
    h_r = objectToBytes(obj, group)
    h_r = group.hash(h_r, ZR)
    C3 = ((pk_R2 ** (h_r) * pk_R3) ** r2) * (pp['g'] ** (h_r * r1))
    C4 = group.hash(w, G1) ** r2
    C5 = group.hash((C1, C2, C3, C4), G1)
    C = (C1, C2, C3, C4)
    return C


def Trapdoor(pp, sk_R, pk_S, w):
    sk_R1, sk_R2, sk_R3, sk_R4 = sk_R
    r3 = group.random(ZR)
    Tw1 = pp['g'] ** (r3 * (sk_R2 * group.hash((pk_S ** sk_R1, w), ZR) + sk_R3) ** -1)
    Tw2 = pp['g'] ** r3
    Tw = (Tw1, Tw2)
    return Tw


def Test(pp,C, Tw):
    C1, C2, C3, C4=C
    Tw1,Tw2=Tw
    return pair(C1, Tw1) == pair(C2,Tw2)


for i in range(500):
    start = time.perf_counter()
    pp = Setup()
    sk_R, pk_R = KeyGen_R(pp)
    sk_S, pk_S = KeyGen_S(pp)
    C = Enc(pp, sk_S, pk_R, "urgent")
    Tw = Trapdoor(pp, sk_R, pk_S, "urgent")
    print(Test(pp, C, Tw))
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end - start))
    with open('../scheme_result/PAUKS.txt', 'a', encoding='UTF - 8') as f:
        data = f.write(str(end - start) + "\n")
