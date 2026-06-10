from typing import Optional

# 楕円曲線上の点(x, y)を表す型
# None は無限遠点(Point at Infinity)を表す
ECPoint = Optional[tuple[int, int]]


def inverse_mod(k: int, p: int) -> int:
    """
    有限体 GF(p) 上の乗法逆元を計算する。

    k * x ≡ 1 (mod p)

    を満たす x を返す。

    Args:
        k: 逆元を求める値
        p: 素数位数

    Returns:
        k の mod p における逆元
    """
    return pow(k % p, -1, p)


def point_add(
    P: ECPoint,
    Q: ECPoint,
    a: int,
    p: int
) -> ECPoint:
    """
    楕円曲線上の2点の加算を行う。

    曲線:
        y² = x³ + ax + b (mod p)

    Args:
        P: 点P
        Q: 点Q
        a: 曲線パラメータ a
        p: 素数位数

    Returns:
        P + Q
        無限遠点の場合は None
    """

    # O + Q = Q
    if P is None:
        return Q

    # P + O = P
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # P + (-P) = O
    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if P == Q:
        # 点倍算
        #
        # s = (3x² + a) / (2y)
        #
        s = (
            (3 * x1 * x1 + a)
            * inverse_mod(2 * y1, p)
        ) % p

    else:
        # 点加算
        #
        # s = (y2 - y1) / (x2 - x1)
        #
        s = (
            (y2 - y1)
            * inverse_mod(x2 - x1, p)
        ) % p

    # 加算後の座標を計算
    x3 = (s * s - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p

    return (x3, y3)

def scalar_mult(
    k: int,
    P: ECPoint,
    a: int,
    p: int
) -> ECPoint:
    """
    スカラー倍算 kP を行う。

    Double-and-Add 法を使用。

    Args:
        k: スカラー値(秘密鍵)
        P: 楕円曲線上の点
        a: 曲線パラメータ a
        p: 素数位数

    Returns:
        kP
    """
    # 計算結果
    result: ECPoint = None

    # 現在加算対象の点
    addend = P

    while k > 0:

        # kのLSBが1なら加算
        if k & 1:
            result = point_add(
                result,
                addend,
                a,
                p
            )

        # 次のビットへ向けて点倍算
        addend = point_add(
            addend,
            addend,
            a,
            p
        )

        # k >>= 1
        k >>= 1

    return result

# ============================================================
# NIST P-521 Curve Parameters
# (https://www.nist.gov/publications/recommendations-discrete-logarithm-based-cryptography-elliptic-curve-domain-parameters?utm_source=chatgpt.com)
# NIST CAVP ECCCDH Primitive Test Vector
# (https://csrc.nist.gov/Projects/Cryptographic-Algorithm-Validation-Program/Component-Testing?utm_source=chatgpt.com)
# FIPS 186-4 / SP800-186
# secp521r1
# ============================================================

# p = 2^521 - 1
p = (1 << 521) - 1

# a = -3 mod p
a = p - 3

b = int(
    "0051953EB9618E1C9A1F929A21A0B68540EEA2DA725B99B315F3B8B489918EF1"
    "09E156193951EC7E937B1652C0BD3BB1BF073573DF883D2C34F1EF451FD46B50"
    "3F00",
    16
)

# Base Point G
Gx = int(
    "00C6858E06B70404E9CD9E3ECB662395B4429C648139053FB521F828AF606B4D"
    "3DBAA14B5E77EFE75928FE1DC127A2FFA8DE3348B3C1856A429BF97E7E31C2E5"
    "BD66",
    16
)

Gy = int(
    "011839296A789A3BC0045C8A5FB42C7D1BD998F54449579B446817AFBD17273E"
    "662C97EE72995EF42640C550B9013FAD0761353C7086A272C24088BE94769FD1"
    "6650",
    16
)

G: tuple[int, int] = (Gx, Gy)

# ============================================================
# NIST CAVP ECCCDH Primitive Test Vector
# Curve: P-521
# COUNT = 0
# ============================================================
# 相手公開鍵 QCAVS = (QCAVSx, QCAVSy)
QCAVSx = int(
    "000000685A48E86C79F0F0875F7BC18D25EB5FC8C0B07E5DA4F4370F3A949034"
    "0854334B1E1B87FA395464C60626124A4E70D0F785601D37C09870EBF1766668"
    "77A2046D",
    16
)

QCAVSy = int(
    "000001BA52C56FC8776D9E8F5DB4F0CC27636D0B741BBE05400697942E80B739"
    "884A83BDE99E0F6716939E632BC8986FA18DCCD443A348B6C3E522497955A4F3"
    "C302F676",
    16
)

# 自装置秘密鍵
dIUT = int(
    "0000017EECC07AB4B329068FBA65E56A1F8890AA935E57134AE0FFCCE8027351"
    "51F4EAC6564F6EE9974C5E6887A1FEFEE5743AE2241BFEB95D5CE31DDCB6F9ED"
    "B4D6FC47",
    16
)

# NISTが規定する期待共有秘密(x座標)
ZIUT_expected = int(
    "005FC70477C3E63BC3954BD0DF3EA0D1F41EE21746ED95FC5E1FDF90930D5E13"
    "6672D72CC770742D1711C3C3A4C334A0AD9759436A4D3C5BF6E74B9578FAC148"
    "C831",
    16
)
# 相手の公開鍵
peer_public: tuple[int, int] = (
    QCAVSx,
    QCAVSy
)

# ============================================================
# ECDH Shared Secret Calculation
# ============================================================
# shared_point = dIUT × QCAVS
shared_point = scalar_mult(
    dIUT,
    peer_public,
    a,
    p
)

if shared_point is None:
    raise RuntimeError("ECDH calculation failed")

# SP800-56Aでは共有秘密としてx座標を使用
shared_x = shared_point[0]

print("Computed Z:")
print(f"{shared_x:0131X}") # 131桁の16進数で表示.足りない桁を0で埋める

print()
print("Expected Z:")
print(f"{ZIUT_expected:0131X}")# 131桁の16進数で表示.足りない桁を0で埋める

print()
print("Match =", shared_x == ZIUT_expected)
