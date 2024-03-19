import time

from charm.core.engine.util import objectToBytes
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, pair, GT

group = PairingGroup("SS512")
'''count = 10
group = PairingGroup("MNT224")
g = group.random(GT)
assert g.initPP(), "failed to init pre-computation table"
h = group.random(GT)
a, b = group.random(ZR, 2)

assert group.InitBenchmark(), "failed to initialize benchmark"
group.StartBenchmark(["RealTime"])
for i in range(count):
    A = g ** a
group.EndBenchmark()
print("With PP: ", group.GetBenchmark("RealTime"))

assert group.InitBenchmark(), "failed to initialize benchmark"
group.StartBenchmark(["RealTime"])
for i in range(count):
    B = h ** b
group.EndBenchmark()
print("Without: ", group.GetBenchmark("RealTime"))'''
'''
        obj1 = {'a': message, 'b': pk['ID'], 'c': pk['pk_id']}
        h = objectToBytes(obj1, group)
        h = group.hash(h, ZR)  //{0,1}->Zq
'''


def Setup():
    g = group.random(G1)
    p = group.order()
    u = pair(g, g)
    params = {'g': g, 'p': p, 'u': u}
    return params


def KeyGen_R(params):
    x = group.random(ZR)
    pk_R = params['g'] ** x
    sk_R = x
    return (sk_R, pk_R)


def KeyGen_S(params):
    y = group.random(ZR)
    pk_S = params['g'] ** y
    sk_S = y
    return (sk_S, pk_S)


def PAEKS(params, w,pk_R,sk_S):
    r=group.random(ZR)
    A=group.serialize(params['u']**(sk_S*r))
    v=group.hash((w,pk_R**sk_S),ZR)
    B=params['g']**(v*r)*(pk_R**r)
    Cw=(A,B)
    return Cw


def Trapdoor(params,w,pk_S,sk_R):
    v=group.hash((w,pk_S**sk_R),ZR)
    Tw=pk_S**((sk_R+v)**-1)
    return Tw


def Test(Cw, Tw):
    A, B = Cw[0], Cw[1]
    return group.serialize(pair(Tw,B))==A


for i in range(500):
    start = time.perf_counter()
    params = Setup()
    sk_R, pk_R = KeyGen_R(params)
    sk_S, pk_S = KeyGen_S(params)
    Cw = PAEKS(params, "urgent", pk_R, sk_S)
    Tw = Trapdoor(params, "urgent", pk_S, sk_R)
    print(Test(Cw, Tw))
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end - start))
    with open('../scheme_result/user-friendly-PAEKS.txt', 'a', encoding='UTF - 8') as f:
        data = f.write(str(end - start) + "\n")
