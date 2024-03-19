'''
:Authors:         Shashank Agrawal
:Date:            5/2016
'''
import time

from charm.toolbox.pairinggroup import PairingGroup, GT
from ABE.ac17 import AC17CPABE


for i in range(50):
    start = time.perf_counter()
    # instantiate a bilinear pairing map
    pairing_group = PairingGroup('MNT224')

    # AC17 CP-ABE under DLIN (2-linear)
    cpabe = AC17CPABE(pairing_group, 2)

    # run the set up
    (pk, msk) = cpabe.setup()

    # generate a key
    attr_list = ['ONE', 'TWO', 'THREE']
    key = cpabe.keygen(pk, msk, attr_list)

    # choose a random message
    msg = pairing_group.random(GT)

    # generate a ciphertext
    policy_str = '((ONE and THREE) and (TWO OR FOUR))'
    ctxt = cpabe.encrypt(pk, msg, policy_str)

    # decryption
    rec_msg = cpabe.decrypt(pk, ctxt, key)
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end - start))


