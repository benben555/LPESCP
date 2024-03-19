# coding=utf-8
import time

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
import hashlib

Hash1pre = hashlib.md5


def Hash1(w):
    # 先对关键词w进行md5哈希
    hv = Hash1pre(str(w).encode('utf8')).hexdigest()
    # print(hv)
    # 再对md5值进行group.hash哈希，生成对应密文
    # 完整的Hash1由md5和group.hash组成
    hv = group.hash(hv, type=G1)
    return hv


Hash2 = hashlib.sha256


def Setup(param_id='SS512'):
    # 代码符号G1 x G2 →  GT
    group = PairingGroup(param_id)
    # 方案选用的是对称双线性对，故G2 = G1
    g = group.random(G1)
    alpha = group.random(ZR)
    # 生成私钥与公钥并进行序列化
    # Serialize a pairing object into bytes
    sk = group.serialize(alpha)
    pk = [group.serialize(g), group.serialize(g ** alpha)]
    return [sk, pk]


def Enc(pk, w, param_id='SS512'):
    group = PairingGroup(param_id)
    # 进行反序列化
    g, h = group.deserialize(pk[0]), group.deserialize(pk[1])
    r = group.random(ZR)
    t = pair(Hash1(w), h ** r)
    c1 = g ** r
    c2 = t
    # 对密文进行序列化
    # print(group.serialize(c2))
    return [group.serialize(c1), Hash2(group.serialize(c2)).hexdigest()]


def TdGen(sk, w, param_id='SS512'):
    group = PairingGroup(param_id)
    sk = group.deserialize(sk)
    td = Hash1(w) ** sk
    # 对陷门进行序列化
    return group.serialize(td)


def Test(td, c, param_id='SS512'):
    group = PairingGroup(param_id)
    c1 = group.deserialize(c[0])
    c2 = c[1]
    # print(c2)
    td = group.deserialize(td)
    return Hash2(group.serialize(pair(td, c1))).hexdigest() == c2


if __name__ == '__main__':
    for i in range(500):
        start = time.perf_counter()
        # 'SS512'是对称双线性对
        param_id = 'SS512'
        [sk, pk] = Setup(param_id)

        group = PairingGroup(param_id)

        c = Enc(pk, "yes")
        td = TdGen(sk, "yes")
        print(Test(td, c))
        end = time.perf_counter()
        print('Running time: %s Seconds' % (end - start))
        with open('../scheme_result/peks.txt', 'a', encoding='UTF - 8') as f:
            data = f.write(str(end - start) + "\n")