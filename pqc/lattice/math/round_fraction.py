from fractions import Fraction


def round_fraction(x: Fraction) -> int:
    """
    Fractionを最近傍整数へ丸める。

    Sageのround()に近い用途で使用する。

    Parameters
    ----------
    x : Fraction
        丸める有理数

    Returns
    -------
    int
        最近傍整数
    """
    
    if x >= 0:
        return (
            x.numerator * 2 + x.denominator
        ) // (
            2 * x.denominator
        )

    return -round_fraction(-x)

