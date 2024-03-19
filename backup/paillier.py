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


if __name__ == "__main__":
    pai = Paillier()
    pai.__key_gen__()
    pubKey = pai.pubKey
    priKey = pai.priKey
    print("Public/Private key generated.")
    print("pubKey:",pubKey[0],pubKey[1])
    print("priKey:",priKey[0],priKey[1])
    # plaintext = input("Enter your text: ")
    # plaintext = 'Cat is the cutest.'
    # print("Original text:", plaintext)
    # ciphertext = pai.encipher(plaintext)
    ciphertext = pai.encipher("2596429802100919793231257281739011709939626239598318513863")
    print("Ciphertext:", ciphertext)
    deciphertext = pai.decipher(ciphertext)
    print("Deciphertext: ", deciphertext)

