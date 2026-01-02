import hashlib
import os

def shake128(data, outlen):
    return hashlib.shake_128(data).digest(outlen)

# -----------------
# 基本定数
# -----------------
N = 256        # 学習用（本物は256）
Q = 3329
ETA = 2


# -----------------
# 多項式演算
# -----------------

def poly_add(a, b):
    """
    多項式の加算（係数ごと、mod Q）

    a, b:
        長さ N のリスト
        a[i] = x^i の係数

    戻り値:
        (a + b) mod Q

    Kyberでの意味:
        ・ノイズ e を足す
        ・複数項の結果を合成する
        ・Z_q[x] の「加算」
    """
    # zip(a, b) により
    #   (a[0], b[0]), (a[1], b[1]), ... を順に処理
    return [(x + y) % Q for x, y in zip(a, b)]

def poly_mul(a, b):
    """
    多項式の乗算（Z_q[x] / (x^N + 1)）

    数学的には：
        c(x) = a(x) * b(x) mod (x^N + 1)

    重要ポイント：
        x^N ≡ -1 という関係を使う
        → 係数が N を超えたら「符号反転」して折り返す

    Kyberでの意味：
        ・A * s
        ・A * r
        ・b * r
        の「*」に相当
        （本物Kyberでは NTT で高速化）
    """

    # 結果多項式 c(x) の係数（初期値 0）
    res = [0] * N

    # a(x) = Σ a[i] x^i
    # b(x) = Σ b[j] x^j
    #
    # 通常の多項式乗算では
    #   a[i] * b[j] は x^(i+j) の係数に加算される
    for i in range(N):
        for j in range(N):
            # i+j が N 未満ならそのまま
            # i+j が N 以上なら
            #   x^(i+j) = x^(i+j-N) * x^N
            #          = -x^(i+j-N)
            #
            # → 添字は (i+j)%N
            k = (i + j) % N

            # x^N = -1 による符号反転
            sign = -1 if (i + j) >= N else 1

            # res[k] += sign * a[i] * b[j]
            # mod Q を取りながら加算
            res[k] = (res[k] + sign * a[i] * b[j]) % Q

    return res

# -----------------
# ノイズ生成
# -----------------
def cbd(buf, eta, n):
    """
    Kyber-style Centered Binomial Distribution
    buf : bytes (長さは ceil(n*2*eta/8) 以上)
    eta : Kyber512 -> 2
    n   : number of coefficients
    """
    res = []
    bitpos = 0

    for _ in range(n):
        a = 0
        b = 0
        for _ in range(eta):
            byte = buf[bitpos >> 3]
            bit  = (byte >> (bitpos & 7)) & 1
            a += bit
            bitpos += 1

        for _ in range(eta):
            byte = buf[bitpos >> 3]
            bit  = (byte >> (bitpos & 7)) & 1
            b += bit
            bitpos += 1

        res.append(a - b)

    return res
def cbd_bytes_needed(n, eta):
    return (n * 2 * eta + 7) // 8

def sample_noise(seed, label, n, eta):
    length = cbd_bytes_needed(n, eta)
    buf = shake128(seed + label, length)
    return cbd(buf, eta, n)

# -----------------
# 鍵生成
# -----------------
def keygen():
    seed = os.urandom(32)
    print("Keygen seed:", seed.hex())
    
    # 行列 A（学習用簡略版）
    A = [[int.from_bytes(shake128(seed + bytes([i, j]), 2), 'little') % Q
          for j in range(N)] for i in range(N)]

    s = sample_noise(seed, b"s", N, ETA)
    e = sample_noise(seed, b"e", N, ETA)

    b = poly_add(
        [sum(A[i][j] * s[j] for j in range(N)) % Q for i in range(N)],
        e
    )

    return (A, b), s

# -----------------
# KDF (鍵導出関数)
# -----------------
def kdf(bit):
    return hashlib.sha256(bytes([bit])).digest()


# -----------------
# 鍵カプセル化
# -----------------
def encapsulate(pk):
    A, b = pk
    seed = os.urandom(32)

    r  = sample_noise(seed, b"r",  N, ETA)
    e1 = sample_noise(seed, b"e1", N, ETA)
    e2 = sample_noise(seed, b"e2", 1, ETA)[0]

    u = poly_add(
        [sum(A[i][j] * r[j] for j in range(N)) % Q for i in range(N)],
        e1
    )

    v = (sum(b[i] * r[i] for i in range(N)) + e2) % Q

    bit = 1 if v > Q//2 else 0
    K = kdf(bit)

    return (u, v), K

# -----------------
# 鍵復号化
# -----------------
def decapsulate(sk, ct):
    u, v = ct
    s = sk

    v2 = (v - sum(u[i] * s[i] for i in range(N))) % Q

    bit = 1 if v2 > Q//2 else 0
    return kdf(bit)

if __name__ == "__main__":
    # 鍵生成
    pk, sk = keygen()

    # 鍵カプセル化
    ct, K1 = encapsulate(pk)

    # 鍵復号化
    K2 = decapsulate(sk, ct)

    print("K1:", K1.hex())
    print("K2:", K2.hex())
    print("一致:", K1 == K2)