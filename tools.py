import decimal
import math
import gmpy2 as gy
import random
import time
import libnum


def Gen_data(user, a, b):
    st_demand = []
    st_provide = []
    demand = 0
    provide = 0
    # 生成一组互不相同的随机数
    power = {}
    st_power = []
    weight = {}
    st_weight = []
    nums = set()
    while len(nums) < a:
        nums.add(random.randint(1, 20))
    for i in range(1, a + b + 1):
        if i in nums:
            power[i] = round(random.random() * 100, 2)
            st_demand.append(i)
            demand += round(random.random() * 100, 2)
        else:
            power[i] = -round(max(0.1, random.random() * 100 - 5), 2)
            st_provide.append(i)
            provide += round(max(0.1, random.random() * 100 - 5), 2)
        weight[i] = max(round(random.random() * 10, 2), 0.1)
        user[i].Weight = weight[i]
    if provide < 0.9 * demand:
        for i in st_provide:
            power[i] = min(round(power[i] - (0.9 * demand - provide) / b, 2), 0)
    if provide > 1.1 * demand:
        for i in st_provide:
            power[i] = min(round(power[i] + (provide - 1.1 * demand) / b, 2), 0)
    for i in range(1, a + b + 1):
        st_power.append(power[i])
        st_weight.append(weight[i])
    print("\n")
    print("有", a, "个需求用户")
    print("有", b, "个供电用户")
    print("各自的供电量分别是", st_power)
    print("各自的权重分别是", st_weight)
    # print("总供电量是", provide)
    # print("总需电量是", demand)

    return power, weight


def test_time(_dir):
    with open(_dir, 'r') as fin:
        data = [float(x) for x in fin.read().split('\n')]
    average = sum(data)
    return average


def floor2(a):
    return math.floor(a * 100) / 100


def ceil2(a):
    return math.ceil(a * 100) / 100


def result(a):
    return math.floor(decimal.Decimal(a) * decimal.Decimal('1e10')) / 1e10


def sum_weight(Provide, Demand, st_true_provide, st_true_demand, st_provide_weight, st_demand_weight):
    a = len(Demand)
    b = len(Provide)
    sums = 0
    for i in range(a):
        if Demand[i] == 0:
            sums += (1 - 1 / (st_demand_weight[i] + 1))
        else:
            sums += (1 - 1 / (st_demand_weight[i] + 1)) * math.sqrt(st_true_demand[i] / Demand[i])
    for i in range(b):
        if Provide[i] == 0:
            sums += (1 - 1 / (st_provide_weight[i] + 1))
        else:
            sums += (1 - 1 / (st_provide_weight[i] + 1)) * math.sqrt((1 - st_true_provide[i] / Provide[i]))
    return sums


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
        # res = gy.div((x - 1), n)
        res = (x - 1) // n
        # this step is essential, directly using "/" causes bugs
        # due to the floating representation in python
        return res

    def __key_gen__(self):
        # generate random state
        while True:
            rs = gy.random_state(int(time.time()))
            p = self.__gen_prime__(rs)
            q = self.__gen_prime__(rs)
            n = p * q
            lmd = (p - 1) * (q - 1)
            # originally, lmd(lambda) is the least common multiple.
            # However, if using p,q of equivalent length, then lmd = (p-1)*(q-1)
            if gy.gcd(n, lmd) == 1:
                # This property is assured if both primes are of equal length
                break
        g = n + 1
        mu = gy.invert(lmd, n)
        # Originally,
        # g would be a random number smaller than n^2,
        # and mu = (L(g^lambda mod n^2))^(-1) mod n
        # Since q, p are of equivalent length, step can be simplified.
        self.pubKey = [n, g]
        self.priKey = [lmd, mu]
        return

    def decipher(self, ciphertext):
        n, g = self.pubKey
        lmd, mu = self.priKey
        m = self.__L__(gy.powmod(ciphertext, lmd, n ** 2), n) * mu % n
        print("raw message:", m)
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
