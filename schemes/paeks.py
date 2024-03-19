from charm.core.engine.util import objectToBytes
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, pair, GT

group = PairingGroup("SS512")


def Setup():
    g = group.random(G1)
    p = group.order()
    u = pair(g, g)
    params = {'G1': G1, 'GT': GT, 'p': p, 'g': g, 'u': u}
    return params


def KeyGen_R(params):
    x = group.random(ZR)
    pk_r = params['g'] ** x
    return (x, pk_r)


def KeyGen_S(params):
    y = group.random(ZR)
    pk_s = params['g'] ** y
    return (y, pk_s)


def PAEKS(params, w, pk_r, sk_s):
    r = group.random(ZR)
    A = group.serialize(params['u'] ** (sk_s * r))
    obj1 = {'a': w, 'b': pk_r ** sk_s}
    v = objectToBytes(obj1, group)
    v = group.hash(v, ZR)
    B = (params['g'] ** (v * r)) * (pk_r ** r)
    return (A, B)


def Trapdoor(params, w, pk_s, sk_r):
    obj1 = {'a': w, 'b': pk_s ** sk_r}
    v = objectToBytes(obj1, group)
    v = group.hash(v, ZR)
    Tw = pk_s ** ((sk_r + v) ** -1)
    return Tw


def Test(Cw, Tw):
    A, B = Cw
    return group.serialize(pair(Tw, B)) == A

import time

for i in range(500):
    start = time.perf_counter()
    params = Setup()
    sk_r, pk_r = KeyGen_R(params)
    sk_s, pk_s = KeyGen_S(params)
    Cw = PAEKS(params, 'urgent', pk_r, sk_s)
    Tw = Trapdoor(params, 'urgent', pk_s, sk_r)
    print(Test(Cw, Tw))
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end - start))
    with open('../scheme_result/paeks.txt', 'a', encoding='UTF - 8') as f:
        data = f.write(str(end - start) + "\n")