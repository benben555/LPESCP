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


def GlobalSetup():
    g = group.random(G1)
    alpha = group.random(ZR)
    g1 = g ** alpha
    mk = {'alpha': alpha}
    gp = {'g': g, 'g1': g1}
    return (mk, gp)


def KeyGen(gp):
    x_u = group.random(ZR)
    pk_u = gp['g'] ** x_u
    return (x_u, pk_u)


def CertGen(gp, mk, id_u, pk_u):
    obj1 = {'a': id_u, 'b': pk_u}
    h = objectToBytes(obj1, group)
    h_u = group.hash(h, G1)
    Cert_u = h_u ** mk['alpha']
    return Cert_u


def Encrypt(gp, w, id_s, sk_s, cert_s, id_r, pk_r):
    # obj1 = {'a': pk_r ** sk_s}
    # k1 = objectToBytes(obj1, group)
    k1 = group.serialize(pk_r ** sk_s)
    obj2 = {'a': id_r, 'b': pk_r}
    h_r = objectToBytes(obj2, group)
    h_r = group.hash(h_r, G1)
    # obj3 = {'a': pair(cert_s, h_r)}
    # k2 = objectToBytes(obj3, group)
    k2 = group.serialize(pair(cert_s, h_r))
    r = group.random(ZR)
    C1 = gp['g'] ** r
    obj4 = {'a': w, 'b': k1, 'c': k2}
    W = objectToBytes(obj4, group)
    W = group.hash(W, ZR)
    # obj5 = {'a': pair(pk_r * gp['g1'], h_r) ** (r * w)}
    # C2 = objectToBytes(obj5, group)
    C2 = group.serialize(pair(pk_r * gp['g1'], h_r) ** (r * W))
    return (C1, C2)


def Trapdoor(gp, w, id_s, pk_s, id_r, pk_r, sk_r, cert_r):
    # obj1 = {'a': pk_s ** sk_r}
    # k1 = objectToBytes(obj1, group)
    k1 = group.serialize(pk_s ** sk_r)
    obj2 = {'a': id_s, 'b': pk_s}
    h_s = objectToBytes(obj2, group)
    h_s = group.hash(h_s, G1)
    # obj3 = {'a': pair(h_s, cert_r)}
    # k2=objectToBytes(obj3, group)
    k2 = group.serialize(pair(h_s, cert_r))
    obj4 = {'a': id_r, 'b': pk_r}
    h_r = objectToBytes(obj4, group)
    h_r = group.hash(h_r, G1)
    obj5 = {'a': w, 'b': k1, 'c': k2}
    W = objectToBytes(obj5, group)
    W = group.hash(W, ZR)
    Tw = ((h_r ** sk_r) * cert_r) ** W
    return Tw


def Test(gp, Cw, Tw):
    C1, C2 = Cw[0], Cw[1]
    C22 = group.serialize(pair(C1, Tw))
    return C2 == C22


for i in range(500):
    start = time.perf_counter()
    mk, gp = GlobalSetup()
    sk_u1, pk_u1 = KeyGen(gp)
    sk_u2, pk_u2 = KeyGen(gp)
    Cert_u1 = CertGen(gp, mk, 1, pk_u1)
    Cert_u2 = CertGen(gp, mk, 2, pk_u2)
    Cw = Encrypt(gp, b"urgent", 1, sk_u1, Cert_u1, 2, pk_u2)
    Tw = Trapdoor(gp, b"urgent", 1, pk_u1, 2, pk_u2, sk_u2, Cert_u2)
    print(Test(gp, Cw, Tw))
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end - start))
    with open('../scheme_result/CBSE.txt', 'a', encoding='UTF - 8') as f:
        data = f.write(str(end - start) + "\n")
