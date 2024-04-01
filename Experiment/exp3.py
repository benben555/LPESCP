import time
from Schemes import PAEKS
from Schemes import CBSE
from Schemes import PAUKS
from Schemes import CBEKS
from  Schemes import Lightweight_PAEKS
for i in range(500):
    start = time.perf_counter()
    params = paeks.Setup()
    sk_r, pk_r = paeks.KeyGen_R(params)
    sk_s, pk_s = paeks.KeyGen_S(params)
    Cw = paeks.PAEKS(params, b'urgent', pk_r, sk_s)
    Tw = paeks.Trapdoor(params, b'urgent', pk_s, sk_r)
    print(paeks.Test(Cw, Tw))
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end - start))
    with open('../scheme_result/paeks.txt', 'a', encoding='UTF - 8') as f:
        f.write(str(end - start) + "\n")

    start = time.perf_counter()
    mk, gp = CBSE.GlobalSetup()
    sk_u1, pk_u1 = CBSE.KeyGen(gp)
    sk_u2, pk_u2 = CBSE.KeyGen(gp)
    Cert_u1 = CBSE.CertGen(gp, mk, 1, pk_u1)
    Cert_u2 = CBSE.CertGen(gp, mk, 2, pk_u2)
    Cw = CBSE.Encrypt(gp, b"urgent", 1, sk_u1, Cert_u1, 2, pk_u2)
    Tw = CBSE.Trapdoor(gp, b"urgent", 1, pk_u1, 2, pk_u2, sk_u2, Cert_u2)
    print(CBSE.Test(gp, Cw, Tw))
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end - start))
    with open('../scheme_result/CBSE.txt', 'a', encoding='UTF - 8') as f:
        f.write(str(end - start) + "\n")

    start = time.perf_counter()
    pp = PAUKS.Setup()
    sk_R, pk_R = PAUKS.KeyGen_R(pp)
    sk_S, pk_S = PAUKS.KeyGen_S(pp)
    C = PAUKS.Enc(pp, sk_S, pk_R, b"urgent")
    Tw = PAUKS.Trapdoor(pp, sk_R, pk_S, b"urgent")
    print(PAUKS.Test(pp, C, Tw))
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end - start))
    with open('../scheme_result/PAUKS.txt', 'a', encoding='UTF - 8') as f:
        f.write(str(end - start) + "\n")

    start = time.perf_counter()
    SPM, SMK = CBEKS.SystemSetup()
    SK_A, P_A = CBEKS.KeyGen(SPM, 1)
    SK_B, P_B = CBEKS.KeyGen(SPM, 2)
    PK_A, Cert_A = CBEKS.UserCertify(SPM, SMK, 1, P_A)
    PK_B, Cert_B = CBEKS.UserCertify(SPM, SMK, 2, P_B)
    Ckw = CBEKS.KeywordEnc(SPM, b"urgent", 1, SK_A, Cert_A, 2, PK_B)
    TD_kw = CBEKS.TrapdoorGen(SPM, b"urgent", 1, PK_A, 2, SK_B, Cert_B)
    print(CBEKS.MatchTest(SPM, Ckw, TD_kw, Cert_A, Cert_B, PK_A, PK_B, 1, 2))
    # print(MatchTest(SPM, Ckw, TD_kw))
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end - start))
    with open('../scheme_result/CBEKS.txt', 'a', encoding='UTF - 8') as f:
        f.write(str(end - start) + "\n")

    start = time.perf_counter()
    GSP = lightweight_peaks.SystemSetup()
    sk_s, pk_s = lightweight_peaks.ServerKeyGen(GSP)
    sk_A, pk_A = lightweight_peaks.UserKeyGen(GSP)
    sk_B, pk_B = lightweight_peaks.UserKeyGen(GSP)
    IC_kw = lightweight_peaks.IndexCiphertextGen(GSP, b"urgent", pk_s, sk_A, pk_A, pk_B)
    ST_kw = lightweight_peaks.SearchTrapdoorGen(GSP, b"urgent", pk_A, sk_B, pk_B)
    print(lightweight_peaks.MatchTest(GSP, sk_s, IC_kw, ST_kw))
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end - start))
    with open('lightweight_peaks.txt', 'a', encoding='UTF - 8') as f:
        f.write(str(end - start) + "\n")