# 定义置换表和S盒
P10 = [3,5,2,7,4,10,1,9,8,6]
P8 = [6,3,7,4,8,5,10,9]
IP = [2,6,3,1,4,8,5,7]
IP_inverse = [4,1,3,5,7,2,8,6]
E_P = [4,1,2,3,2,3,4,1]
P4 = [2,4,3,1]
S0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,0,2]]
S1 = [[0,1,2,3],[2,0,1,3],[3,0,1,2],[2,1,0,3]]

# 置换函数
def permute(k, arr, n):
    per = []
    for i in range(0,n):
        per.append(k[arr[i]-1])  # 根据arr中的位置信息进行置换
    return per

# 左移函数
def shift(l, n):
    s = l[n:] + l[:n]  # 左移n位
    return s

# 密钥生成函数
def keygen(key):
    key = permute(key, P10, 10)  # 第一次置换
    key = shift(key, 1)  # 左移
    key1 = permute(key, P8, 8)  # 第二次置换得到K1
    key = shift(key, 2)  # 再次左移
    key2 = permute(key, P8, 8)  # 第三次置换得到K2
    return key1, key2

# 轮函数F
def F(R, key):
    t = permute(R, E_P, 8)  # 扩展置换
    t = [t[i] ^ key[i] for i in range(8)]  # 与子密钥异或
    t = t[:4], t[4:]  # 分为两半
    row = int(str(t[0][0])+str(t[0][3]),2)  # 计算S盒的行
    col = int(''.join([str(x) for x in t[0][1:3]]),2)  # 计算S盒的列
    val = bin(S0[row][col])[2:].zfill(2)  # 从S盒中获取值
    row = int(str(t[1][0])+str(t[1][3]),2)
    col = int(''.join([str(x) for x in t[1][1:3]]),2)
    val += bin(S1[row][col])[2:].zfill(2)
    val = [int(x) for x in str(val)]
    val = permute(val, P4, 4)  # P4置换
    return val



# 加密函数
def encrypt(pt, keys):
    pt = permute(pt, IP, 8)  # 初始置换
    L, R = pt[:4], pt[4:]  # 分为左右两半
    temp = R
    # 计算轮函数F的结果，然后再与左半部分异或
    f = F(temp, keys[0])
    L = [L[i] ^ f[i] for i in range(4)]
    # 交换左右两部分
    L, R = R, L
    temp = R
    # 计算轮函数F的结果，然后再与左半部分异或
    f = F(temp, keys[1])
    L = [L[i] ^ f[i] for i in range(4)]
    pt = permute(L+R, IP_inverse, 8)  # 进行逆初始置换
    return pt

# 解密函数
def decrypt(pt, keys):
    pt = permute(pt, IP, 8)  # 初始置换
    L, R = pt[:4], pt[4:]  # 分为左右两半
    temp = R
    # 计算轮函数F的结果，然后再与左半部分异或
    f = F(temp, keys[1])
    L = [L[i] ^ f[i] for i in range(4)]
    # 交换左右两部分
    L, R = R, L
    temp = R
    # 计算轮函数F的结果，然后再与左半部分异或
    f = F(temp, keys[0])
    L = [L[i] ^ f[i] for i in range(4)]
    pt = permute(L+R, IP_inverse, 8)  # 进行逆初始置换
    return pt

def ascii_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)

def bin_to_ascii(binary):
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))


if __name__ == '__main__':

    # 测试
    key = '1010000010'
    pt = '01110010'
    key = [int(i) for i in key]
    pt = [int(i) for i in pt]
    keys = keygen(key)  # 生成子密钥K1和K2
    cipher = encrypt(pt, keys)  # 加密
    print('加密结果: ', ''.join([str(i) for i in cipher]))
    plain = decrypt(cipher, keys)  # 解密
    print('解密结果: ', ''.join([str(i) for i in plain]))