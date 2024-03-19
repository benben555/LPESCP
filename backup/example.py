'''
Date: 2020/3/19
'''

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, pair
from charm.core.engine.util import objectToBytes
from charm.toolbox.IBSig import *

debug = False

class AGG319(IBSig):

    def __init__(self,groupobj):
        IBSig.__init__(self)
        global group
        group = groupobj

    '''Select the generator and generate the public-private key of the system '''
    def setup(self):
        s, g = group.random(ZR), group.random(G2)
        p_pub = g ** s
        T = group.hash(p_pub, G1)
        obj = {'a': g, 'b': p_pub}
        w = objectToBytes(obj, group)
        W = group.hash(w, G1)
        msk = {'s': s}
        mpk = {'g': g, 'p_pub': p_pub, 'T': T, 'W': W}
        return (mpk, msk)

    '''Generate the public-private key of the users'''
    def keygen(self, mpk, msk, ID):

        s = msk['s']
        g, p_pub = mpk['g'], mpk['p_pub']
        Q = group.hash(ID, G1)

        '''a part of sk'''
        d_id = Q**s
        x = group.random(ZR)
        pk_id = g**x

        sk = {'s': s, 'd_id': d_id, 'x': x}
        pk = {'pk_id': pk_id, 'ID': ID, 'Q': Q}
        return (pk, sk)

    '''Generate the signature of message'''
    def sign(self, pk, sk, mpk, message):
        r = group.random(ZR)
        U = mpk['g'] ** r

        obj1 = {'a': message, 'b': pk['ID'], 'c': pk['pk_id']}
        h = objectToBytes(obj1, group)
        h = group.hash(h, ZR)

        V = (mpk['T']**r)*((sk['d_id']*(mpk['W']**sk['x']))**h)

        hQ = pk['Q']**h
        hpk_id = pk['pk_id']**h

        sig = {'V': V, 'U': U, 'hQ': hQ, 'hpk_id': hpk_id}
        print("signature: '%s'" %sig)
        return sig

    '''Verify the signature of message'''
    def verify(self, pk, sig, mpk, message):
        obj1 = {'a': message, 'b': pk['ID'], 'c': pk['pk_id']}
        h = objectToBytes(obj1, group)
        h = group.hash(h, ZR)
        if pair(mpk['g'], sig['V']) == pair(sig['U'], mpk['T']) * (pair(mpk['p_pub'], pk['Q'])**h) * pair((pk['pk_id']**h), mpk['W']):
            print("pass the verify of signature")
            return True
        return False

    '''Aggregate the signatures of multiple messages'''
    def aggregate(self, sig, sig1, sig2):

        V = sig['V'] * sig1['V'] * sig2['V']
        U = sig['U'] * sig1['U'] * sig2['U']
        hQ = sig['hQ'] * sig1['hQ'] * sig2['hQ']
        hpk_id = sig['hpk_id'] * sig1['hpk_id'] * sig2['hpk_id']

        agg_sign = {'V': V, 'U': U, 'hQ': hQ, 'hpk_id': hpk_id}

        print("aggregate the signature...")
        print("aggregate sign: '%s'" %agg_sign)
        return agg_sign

    '''Aggregate verify the signatures of multiple messages'''
    def agg_verify(self, mpk, agg_sign):

        print("aggregate verify the aggregate signature...")
        if pair(mpk['g'], agg_sign['V']) == pair(agg_sign['U'], mpk['T']) * pair(mpk['p_pub'], agg_sign['hQ']) * pair(agg_sign['hpk_id'], mpk['W']):
            print("aggregate verify success!")
            return True
        return False

def setInfo(mpk, msk, Agg):

    V, U, hQ, hpk_id = 1, 1, 1, 1

    while True:
        # flag = input("please input your choice(continue or exit):\n")
        # if flag == "exit":
        #     break
        ID = input("please input your ID:\n")
        message = input("please input your message:\n")
        M = {'ID': ID, 'message': message}
        (pk, sk) = Agg.keygen(mpk, msk, M['ID'])
        sig = Agg.sign(pk, sk, mpk, M['message'])
        assert Agg.verify(pk, sig, mpk, M['message']), "Failure!"
        V = V*sig['V']
        U = U*sig['U']
        hQ = hQ*sig['hQ']
        hpk_id = hpk_id*sig['hpk_id']
        flag = input("please input your choice(continue or exit):\n")
        if flag == "exit":
            break

    agg_sign = {'V': V, 'U': U, 'hQ': hQ, 'hpk_id': hpk_id}
    return agg_sign


def main():
    groupobj = PairingGroup('MNT224')
    Agg = AGG319(groupobj)
    (mpk, msk) = Agg.setup()
    agg_sign = setInfo(mpk, msk, Agg)

    assert Agg.agg_verify(mpk, agg_sign), "agg_verify Failure"

    if debug: print('Verify Success!!!')


if __name__ == "__main__":
    debug = True
    main()
