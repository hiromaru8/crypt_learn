from fractions import Fraction
import random

from pqc.lattice.math.gram_schmidt import GS0
from pqc.lattice.math.round_fraction import round_fraction
from pqc.lattice.math.util import *


def LLL(
    B: Matrix,
    n: int,
    m:int,
    delta: Fraction
) -> None:
    """
    LLL基底簡約
    
    Parameters
    ----------
    B : Matrix
        基底行列（各行が基底ベクトル）
    n : int
        次元
    m : int
        ベクトルの次元
    delta : Fraction
        LLLパラメータ（δ）

    Returns
    -------
    None
        Bを直接変更する。
    """

    # 1. Gram-Schmidt直交化
    #  直交化ベクトル b₀*, b₁*, ...
    #  係数 μᵢⱼ
    GS, mu = GS0(B, n, m)

    # 直交化ベクトルのノルム²
    # BB[i] = ||b_i*||^2
    BB: list[Fraction] = [
        Fraction(0)
        for _ in range(n)
    ]
    for i in range(n):
        BB[i] = norm_squared(GS[i])

    # k = 1 としてLLL反復開始
    k: int = 1
    while k <= n - 1:

        # サイズ縮約
        #   Gram-Schmidt係数μᵢⱼが |μ[k][j]| > 1/2 (i>j) なら
        #       b_i ← b_i - 「μᵢⱼ」b_j
        #           「a」は実数aの四捨五入による最近似整数
        #       μᵢⱼ ←  μᵢⱼ - 「μᵢⱼ」μⱼ
        for j in range(k - 1, -1, -1):  # j = k-1 ～ 0 を逆順に確認

            if abs(mu[k][j]) > Fraction(1, 2):

                q: int = round_fraction(mu[k][j])

                # B[k] -= q * B[j]
                for i in range(m):
                    B[k][i] -= q * B[j][i]

                # mu[k][l] -= q * mu[j][l]
                for l in range(j + 1):
                    mu[k][l] -= (
                        q * mu[j][l]
                    )

        # Lovasz条件
        if BB[k] >= (delta - mu[k][k - 1] ** 2) * BB[k - 1]:
            k += 1

        else:
            # B[k-1] と B[k] を交換
            B[k - 1], B[k] = (B[k], B[k - 1])

            # Gram-Schmidtを再計算
            GS, mu = GS0(B, n, m)

            for i in range(n):
                BB[i] = norm_squared(GS[i])

            k = max(k - 1, 1)




# ========================================
# メイン処理
# ========================================
# py -m pqc.lattice.LLL
if __name__ == "__main__":

    # n次元の基底行列を生成
    n: int = 20
    m: int = n

    # 基底の範囲を指定
    bound: int = 2 ** n

    # n × n のゼロ行列
    B: Matrix = [
        [Fraction(0) for _ in range(n)]
        for _ in range(n)
    ]
    # 初期行列を表示
    print_matrix(B)
    
    # B[0,0] = bound
    B[0][0] = Fraction(bound)
    
    # B[i,i] = 1
    # B[i,0] = randint(0,bound)
    for i in range(1, n):
        B[i][i] = Fraction(1)
        B[i][0] = Fraction(
            random.randint(0, bound)    # これは、0からboundまでのランダムな整数を生成する
        )


    print("LLL前:")
    print_matrix(B)

    LLL(B, n, m, Fraction(99, 100))

    print()
    print("LLL後:")
    print_matrix(B)