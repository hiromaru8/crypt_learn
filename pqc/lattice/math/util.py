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

def format_matrix(B: Matrix, space_num: int = 2, header: str = "") -> str:
    """行列を見やすく表示"""
    format=""
    if header:
        format += header
    head_space = len(header)

    for i, row in enumerate(B):
        if i > 0:
            format += " "*head_space
        format += str([
            # 整数の場合は整数として表示し、有理数の場合は分数として表示
            f"{int(x):{space_num}d}" if x.denominator == 1 else f"{x.numerator:{space_num-len(str(x.denominator))-1}d}/{x.denominator}"
            for x in row
        ])
        format += "\n"
    return format


def print_vector(v: Vector, space_num: int = 2,  header: str = "") -> None:
    """ベクトルを見やすく表示"""
    if header:
        print(header, end="")

    print([
        # 整数の場合は整数として表示し、有理数の場合は分数として表示
        f"{int(x):{space_num}d}" if x.denominator == 1 else f"{x.numerator:{space_num-len(str(x.denominator))-1}d}/{x.denominator}"
        for x in v
    ])

def format_vector(v: Vector, space_num: int = 2,  header: str = "") -> str:
    """ベクトルを見やすく表示"""
    format=""
    if header:
        format += header

    format += str([
        # 整数の場合は整数として表示し、有理数の場合は分数として表示
        f"{int(x):{space_num}d}" if x.denominator == 1 else f"{x.numerator:{space_num-len(str(x.denominator))-1}d}/{x.denominator}"
        for x in v
    ])
    
    return format
