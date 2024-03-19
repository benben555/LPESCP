# import random
#
# def generate_shares(secret, num_parties, prime):
#     # 生成Shamir秘密共享的n个密钥
#     coefficients = [secret] + [random.randint(0, prime) for _ in range(num_parties - 1)]
#     shares = [(i, sum(coefficients[j] * i**j for j in range(len(coefficients)))) for i in range(1, num_parties+1)]
#     return shares
#
# def reconstruct_secret(shares, prime):
#     # 重构秘密
#     result = 0
#     for i, share in shares:
#         numerator, denominator = 1, 1
#         for j, _ in shares:
#             if i == j:
#                 continue
#             numerator *= -j
#             numerator %= prime
#             denominator *= i-j
#             denominator %= prime
#         lagrange_coefficient = numerator * pow(denominator, -1, prime)
#         result += share * lagrange_coefficient
#         result %= prime
#     return result
#
# def average_salary(salaries):
#     # 计算平均工资
#     num_parties = len(salaries)
#     prime = 2**31 - 1  # 选取一个足够大的质数作为模数
#     shares = [generate_shares(salary, num_parties, prime) for salary in salaries]
#     # 对每个密钥的每个份额进行加法
#     combined_shares = [(i, sum(share[i-1][1] for share in shares)) for i in range(1, num_parties+1)]
#     # 重构加法结果并除以n得到平均工资
#     average = reconstruct_secret(combined_shares, prime) // num_parties
#     return average
#
# # 示例用法
# salaries = [50003, 60000, 70000]
# average = average_salary(salaries)
# print("平均工资为:", average)
from phe import paillier
import random

def generate_encrypted_shares(secret, num_parties, public_key):
    # 生成Paillier同态加密的n个密钥
    shares = []
    for i in range(num_parties):
        r = random.randint(1, public_key.n-1)
        share = public_key.encrypt(secret, r)
        shares.append(share)
    return shares

def average_salary(salaries):
    # 计算平均工资
    num_parties = len(salaries)
    public_key, private_key = paillier.generate_paillier_keypair()
    encrypted_shares = [generate_encrypted_shares(salary, num_parties, public_key) for salary in salaries]
    # 对每个密钥的每个份额进行同态加法
    combined_encrypted_shares = [public_key.encrypt(0, 1)] * num_parties
    for i in range(num_parties):
        for j in range(num_parties):
            combined_encrypted_shares[i] += encrypted_shares[j][i]
    # 解密加法结果并除以n得到平均工资
    combined_share = private_key.decrypt(combined_encrypted_shares[0])
    for i in range(1, num_parties):
        combined_share += private_key.decrypt(combined_encrypted_shares[i])
    average = combined_share // num_parties
    return average

# 示例用法
salaries = [50000, 60000, 70000]
average = average_salary(salaries)
print("平均工资为:", average)