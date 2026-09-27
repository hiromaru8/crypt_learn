from fractions import Fraction
import inspect
import logging
import random

from pqc.lattice.math.util import *
from pqc.lattice.math.round_fraction import round_fraction
from pqc.lattice.math.gram_schmidt import *
from pqc.lattice.test.disp_param import *

from pqc.lattice.base_logger import *

logger = logging.getLogger(__name__)

TEST_CASES_GramSchmidt = [
    {
        "name": "test_vector_1",
        "B": [
            [Fraction(1), Fraction(1), Fraction(0)],
            [Fraction(1), Fraction(0), Fraction(1)],
            [Fraction(0), Fraction(1), Fraction(1)]
        ]
    },
    {
        "name": "test_vector_2",
        "B": [
            [Fraction(1),   Fraction(1),    Fraction(1)],
            [Fraction(1),   Fraction(-1),   Fraction(2)],
            [Fraction(-1),  Fraction(1),    Fraction(3)]
        ]
    },
    {
        "name": "test_vector_3",
        "B": [
            [Fraction(1),   Fraction(2)],
            [Fraction(6),   Fraction(2)]
        ]
    }
]

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
    header = "    GS       = "
    message = format_matrix(GS, space_num=5, header=header)
    logger.debug(message)
    header = "    mu       = "
    message = format_matrix(mu, space_num=5, header=header)
    logger.debug(message)
    
    # 直交化ベクトルのノルム²
    # BB[i] = ||b_i*||^2
    BB: list[Fraction] = [
        Fraction(0)
        for _ in range(n)
    ]
    for i in range(n):
        BB[i] = norm_squared(GS[i])
    header = "    BB       = "
    message = format_vector(BB, space_num=5, header=header)
    logger.debug(message)

    # k = 1 としてLLL反復開始
    logger.debug("    LLL反復 Start")
    k: int = 1
    iter = 0
    while k <= n - 1:
        iter +=1
        logger.debug("        --------------")
        logger.debug(f"        k       = {k}")
        header      = "        B       = "
        message = format_matrix(B, space_num=5, header=header)
        logger.debug(message)
        
        # =======================
        # サイズ縮約
        #   Gram-Schmidt係数μᵢⱼが |μ[k][j]| > 1/2 (i>j) なら
        #       b_i ← b_i - 「μᵢⱼ」b_j
        #           「a」は実数aの四捨五入による最近似整数
        #       μᵢⱼ ←  μᵢⱼ - 「μᵢⱼ」μⱼ
        # =======================
        logger.debug("        == サイズ縮約 Start==")
        for j in range(k - 1, -1, -1):  # j = k-1 ～ 0 を逆順に確認
            logger.debug(f"            j       = {j}")
            message = f"            |mu[{k}][{j}]| > 1/2 = |{mu[k][j]}| > 1/2 = "
            message += str(abs(mu[k][j]) > Fraction(1, 2))
            logger.debug(message)
            
            if abs(mu[k][j]) > Fraction(1, 2):

                q: int = round_fraction(mu[k][j])
                logger.debug(f"                q       = {q}")

                # B[k] -= q * B[j]
                for i in range(m):
                    B[k][i] -= q * B[j][i]
                
                header = "                B       = "
                message = format_matrix(B, space_num=5, header=header)
                logger.debug(message)
                
                # mu[k][l] -= q * mu[j][l]
                for l in range(j + 1):
                    mu[k][l] -= (
                        q * mu[j][l]
                    )
                header = "                mu      = "
                message = format_matrix(mu, space_num=5, header=header)
                logger.debug(message)
                
        logger.debug("        == サイズ縮約 end ==")

        # ========================
        # Lovasz条件
        # ========================
        logger.debug("        == Lovasz条件 START ==")
        logger.debug(f"            BB[{k}] >= ({delta} - mu[{k}][{k - 1}] ** 2) * BB[{k - 1}]")
        logger.debug(f"            -> {BB[k]} >= ({delta} - {mu[k][k - 1]} ** 2) * {BB[k - 1]}")
        logger.debug(f"            -> {BB[k]} >= {(delta - mu[k][k - 1] ** 2) * BB[k - 1]}")
        logger.debug(f"            = {BB[k] >= (delta - mu[k][k - 1] ** 2) * BB[k - 1]}")
        if BB[k] >= (delta - mu[k][k - 1] ** 2) * BB[k - 1]:
            k += 1

        else:
            # B[k-1] と B[k] を交換
            B[k - 1], B[k] = (B[k], B[k - 1])

            # Gram-Schmidtを再計算
            GS, mu = GS0(B, n, m)

            for i in range(n):
                BB[i] = norm_squared(GS[i])
                
            logger.debug(f"            B[{k-1}] と B[{k}] を交換")
            header      = "            B       = "
            message     = format_matrix(B, space_num=5, header=header)
            logger.debug(message)
            header      = "            GS       = "
            message     = format_matrix(GS, space_num=5, header=header)
            logger.debug(message)
            header      = "            mu       = "
            message     = format_matrix(mu, space_num=5, header=header)
            logger.debug(message)
            header      = "            BB       = "
            message     = format_vector(BB, space_num=5, header=header)
            logger.debug(message)


            k = max(k - 1, 1)
            
            
        logger.debug("        == Lovasz条件 END ==")
    logger.debug("    LLL反復 END")
    logger.debug(f"    LLL反復回数は {iter}回")
    





def test_LLL(test_cases=TEST_CASES_GramSchmidt):
    DISP_SPACE = 5
    
    for i, test_case in enumerate(test_cases):
        logger.info(TEST_CASES_LINE)
        logger.info(f"- test case {i + 1}: {test_case['name']}")
        logger.info(TEST_CASES_LINE)

        # 入力
        B = test_case["B"]
        n = len(B)
        m = len(B[0])
        
        # 入力値表示
        logger.info(f"n        = {n}")
        logger.info(f"m        = {m}")
        logger.info("before LLL")
        header = "B        = "
        message = format_matrix(B,  space_num=DISP_SPACE, header=header)
        logger.info(message)
        
        logger.info("== LLL start === ")
        LLL(B=B,n=n,m=m,delta=Fraction(99, 100))
        logger.info("== LLL end === ")
    
        logger.info("after LLL")
        header = "B        = "
        message = format_matrix(B,  space_num=2, header=header)
        logger.info(message)


def make_testcase():
    
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
    
    
    # B[0,0] = bound
    B[0][0] = Fraction(bound)
    
    # B[i,i] = 1
    # B[i,0] = randint(0,bound)
    for i in range(1, n):
        B[i][i] = Fraction(1)
        B[i][0] = Fraction(
            random.randint(0, bound)    # これは、0からboundまでのランダムな整数を生成する
        )


    return  [
                {
                    "name": "test_vector_random",
                    "B"   : B
                },
            ]
    


# py -m pqc.lattice.test.test_LLL > test.tmp
if __name__ == "__main__":
    setup_logging()
    massage = "start"
    logger.info(massage)
    test_LLL()
    

    # testcase =make_testcase()
    test_LLL(make_testcase())
