from fractions import Fraction



# ベクトルの型
Vector = list[Fraction]

# 行列の型
Matrix = list[Vector]


def dot(a: Vector, b: Vector) -> Fraction:
    """ベクトルの内積
       v = (v_0, v_1, ..., v_{n-1}) と w = (w_0, w_1, ..., w_{n-1}) の内積は
         <v, w> = v_0 * w_0 + v_1 * w_1 + ... + v_{n-1} * w_{n-1}
    """
    return sum(x * y for x, y in zip(a, b))


def norm_squared(v: Vector) -> Fraction:
    """ベクトルのノルムの2乗
        ||v||^2 = Σ_{i=0}^{n-1} v_i^2
                = <v, v> = v_0^2 + v_1^2 + ... + v_{n-1}^2
    """
    return dot(v, v)



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



def print_matrix(B: Matrix, space_num: int = 2, header: str = "") -> None:
    """行列を見やすく表示"""
    if header:
        print(header, end="")
    head_space = len(header)

    for i, row in enumerate(B):
        if i > 0:
            print(" "*head_space, end="")
        print([
            # 整数の場合は整数として表示し、有理数の場合は分数として表示
            f"{int(x):{space_num}d}" if x.denominator == 1 else f"{x.numerator:{space_num-len(str(x.denominator))-1}d}/{x.denominator}"
            for x in row
        ])

def print_vector(v: Vector, space_num: int = 2,  header: str = "") -> None:
    """ベクトルを見やすく表示"""
    if header:
        print(header, end="")

    print([
        # 整数の場合は整数として表示し、有理数の場合は分数として表示
        f"{int(x):{space_num}d}" if x.denominator == 1 else f"{x.numerator:{space_num-len(str(x.denominator))-1}d}/{x.denominator}"
        for x in v
    ])

