import gmpy2 as gy
import random
import time
import libnum


class Paillier(object):
    def __init__(self, pubKey=None, priKey=None):
        self.pubKey = pubKey
        self.priKey = priKey

    def __gen_prime__(self, rs):
        p = gy.mpz_urandomb(rs, 1024)
        while not gy.is_prime(p):
            p += 1
        return p

    def __L__(self, x, n):
        res = (x - 1) // n
        return res

    def __key_gen__(self):
        while True:
            rs = gy.random_state(int(time.time()))
            p = self.__gen_prime__(rs)
            q = self.__gen_prime__(rs)
            n = p * q
            lmd = (p - 1) * (q - 1)
            if gy.gcd(n, lmd) == 1:
                break
        g = n + 1
        mu = gy.invert(lmd, n)
        self.pubKey = [n, g]
        self.priKey = [lmd, mu]
        return

    def decipher(self, ciphertext):

        n, g = self.pubKey
        lmd, mu = self.priKey
        m = self.__L__(gy.powmod(ciphertext, lmd, n ** 2), n) * mu % n
        # print("raw message:", int(m))
        plaintext = libnum.n2s(int(m))
        return plaintext

    def encipher(self, plaintext):
        m = libnum.s2n(plaintext)
        n, g = self.pubKey
        r = gy.mpz_random(gy.random_state(int(time.time())), n)
        while gy.gcd(n, r) != 1:
            r += 1
        ciphertext = gy.powmod(g, m, n ** 2) * gy.powmod(r, n, n ** 2) % (n ** 2)
        return ciphertext


for i in range(50):
    EC = {"urgent": 10, "normal": 20, "anyway": 30, "other": 40, }
    kw = random.choice(list(EC))
    C={}
    EC_U = EC[kw]
    pai = Paillier()
    pai.__key_gen__()
    g_U, N_U = pai.pubKey[1], pai.pubKey[0]
    lmd_U, miu_U = pai.priKey[0], pai.priKey[1]

    c1 = pai.encipher(str(EC_U))
    r1 = gy.mpz_random(gy.random_state(int(time.time())), N_U)
    while gy.gcd(N_U, r1) != 1:
        r1 += 1
    n=len(EC)

    for value in dict.values():
        C[i] = gy.powmod(g_U, EC[i], N_U ** 2) * gy.powmod(r1, N_U, N_U ** 2) % (N_U ** 2)
    # m = (gy.powmod(c1, lmd_U, N_U ** 2) - 1) // N_U * miu_U % N_U
    # m = pai.decipher(c1)
    # x1 = m - (m >= (N_U // 2)) * N_U
    # print("1：",int(pai.decipher(c1)))
    r2 = gy.mpz_random(gy.random_state(int(time.time())), N_U)
    while gy.gcd(N_U, r2) != 1:
        r2 += 1
    s = random.randrange(1, 10000000)
    while gy.gcd(N_U, s) != 1:
        s += 1
    print("s:", s)
    y = 29
    print("kw:", kw, " EC_U:", EC_U, " y:", y, " x-y=", EC_U - y)
    c2 = gy.powmod(c1, s, N_U ** 2) * gy.invert(gy.powmod(g_U, s * y, N_U ** 2), N_U ** 2) * gy.powmod(r2, N_U,
                                                                                                       N_U ** 2) % (
                 N_U ** 2)
    c3 = gy.powmod(g_U, s * (EC_U - y), N_U ** 2) * gy.powmod(gy.powmod(r1, s, N_U ** 2) * r2, N_U, N_U ** 2) % (
            N_U ** 2)
    # print(c2 == c3)
    f = pai.decipher(c2)
    f = libnum.s2n(f)
    print("(x-y)%n: ", f // s)
    x2 = f - (f >= (N_U // 2)) * N_U
    print("s(x-y): ", x2)
    print()
    # print(x2 * (x - y) > 0)
    # print(libnum.s2n(f)- N_U == s * (x - y))
    # print(libnum.s2n(f) in [1,2,3])

#
