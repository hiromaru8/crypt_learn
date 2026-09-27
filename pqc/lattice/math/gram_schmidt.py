from fractions import Fraction
from pqc.lattice.math.util import *

# Gram-Schmidt直交化
def GS0(
    B: Matrix,
    n: int,
    m: int
) -> tuple[Matrix, Matrix]:
    """
    Gram-Schmidt直交化

    Parameters
    ----------
    B : Matrix
        基底ベクトルのリスト(各行が基底ベクトル)
        b_0, b_1, ..., b_{n-1}
    n : int
        ベクトル数
    m : int
        ベクトルの次元

    Returns
    -------
    tuple[Matrix, Matrix]
        GS : Gram-Schmidt直交化後のベクトル
             b_0*, b_1*, ..., b_{n-1}*
        mu : Gram-Schmidt係数
             
    """

    # GS[i] = i番目のGram-Schmidt直交化ベクトルを格納する行列
    GS: Matrix = [
        [Fraction(0) for _ in range(m)]
        for _ in range(n)
    ]

    # mu[i][j] = Gram-Schmidt係数を格納する行列
    mu: Matrix = [
        [Fraction(0) for _ in range(n)]
        for _ in range(n)
    ]

    # Gram-Schmidt直交化の計算
    # j = 0, 1, ..., i-1 に対して、GS[i] = B[i] - sum(mu[i][j] * GS[j])
    for i in range(n):

        # GS[i] = B[i]
        GS[i]  = [
            Fraction(x)
            for x in B[i]
        ]

        # mu[i][i] = 1 
        mu[i][i] = Fraction(1)

        for j in range(i):

            # mu[i][j]= <B[i], GS[j]> / ||GS[j]||^2
            mu[i][j] = (
                dot(B[i], GS[j])
                / norm_squared(GS[j])
            )

            # GS[i] -= mu[i][j] * GS[j]
            # sum(mu[i][j] * GS[j]) を計算するために、GS[i]の各成分から mu[i][j] * GS[j] の各成分を引く
            for k in range(m):
                GS[i][k] -= (
                    mu[i][j] * GS[j][k]
                )

    return GS, mu



