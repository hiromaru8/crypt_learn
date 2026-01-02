import random

# 基本定数
N = 256        # 本物は256（まずは小さく）
Q = 3329

# -----------------
# 多項式演算
# -----------------
def poly_add(a, b):
    """ 多項式の加算

    Args:
        a (_type_): 
        b (_type_): 

    Returns:
        _type_: _a + b_ の多項式
    """
    
    return [(x + y) % Q for x, y in zip(a, b)]

def poly_mul(a, b):
    """ 多項式の乗算 (簡易版)"""
    
    res = [0]*N
    for i in range(N):
        for j in range(N):
            k = (i + j) % N
            sign = -1 if (i + j) >= N else 1
            res[k] = (res[k] + sign * a[i] * b[j]) % Q
    return res

# -----------------
# 鍵生成
# -----------------
def keygen():
    A = [[random.randint(0, Q-1) for _ in range(N)] for _ in range(N)]
    s = [random.randint(0, 1) for _ in range(N)]
    e = [random.randint(0, 1) for _ in range(N)]

    b = poly_add(
        [sum(A[i][j] * s[j] for j in range(N)) % Q for i in range(N)],
        e
    )
    return (A, b), s

# -----------------
# Encapsulate / Decapsulate
# -----------------
def encapsulate(pk):
    """ 鍵カプセル化"""
    A, b = pk
    r = [random.randint(0, 1) for _ in range(N)]
    e1 = [random.randint(0, 1) for _ in range(N)]
    e2 = random.randint(0, 1)

    u = poly_add(
        [sum(A[i][j] * r[j] for j in range(N)) % Q for i in range(N)],
        e1
    )

    v = (sum(b[i] * r[i] for i in range(N)) + e2) % Q

    K = v % 2   # 本物は KDF
    return (u, v), K


def decapsulate(sk, ct):
    """ 鍵復号化

    Args:
        sk (): 秘密鍵
        ct (_type_): 暗号文

    Returns:
        _type_: 復号化された鍵
    """
    u, v = ct
    s = sk
    v2 = (v - sum(u[i] * s[i] for i in range(N))) % Q
    return v2 % 2

if __name__ == "__main__":
    # 鍵生成
    pk, sk = keygen()
    print("Public Key:", pk)
    print("Secret Key:", sk)

    # 鍵カプセル化
    ct, K1 = encapsulate(pk)
    print("Ciphertext:", ct)
    print("Encapsulated Key:", K1)

    # 鍵復号化
    K2 = decapsulate(sk, ct)
    print("Decapsulated Key:", K2)

    assert K1 == K2, "Keys do not match!"
    
    print("Keys match!")
    
    
    