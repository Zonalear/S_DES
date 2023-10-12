# -*- coding: utf-8 -*-
import time
from s_des import keygen , encrypt
def brute_force(plain_text, cipher_text):
    start_time = time.time()
    for i in range(1024):  # 遍历所有可能的密钥
        key = format(i, '010b')  # 将i转换为10位二进制字符串
        keys = keygen([int(bit) for bit in key])  # 生成子密钥
        cipher = encrypt([int(bit) for bit in plain_text], keys)  # 加密
        if ''.join(map(str, cipher)) == cipher_text:  # 如果加密结果和已知的密文匹配
            print(f"Found the key: {key}, time elapsed: {time.time() - start_time} seconds")
            return key
    print(f"No key found, time elapsed: {time.time() - start_time} seconds")
    return None

if __name__ == '__main__':
    plain_text = '01110010'
    cipher_text = '01110111'
    brute_force(plain_text, cipher_text)