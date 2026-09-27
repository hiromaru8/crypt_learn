from fractions import Fraction
import inspect

from pqc.lattice.math.util import *
from pqc.lattice.math.gram_schmidt import *
from pqc.lattice.test.disp_param import *




TEST_CASES_GramSchmidt = [
    {
        "name": "test_vector_1",
        "B": [
            [Fraction(1), Fraction(1), Fraction(0)],
            [Fraction(1), Fraction(0), Fraction(1)],
            [Fraction(0), Fraction(1), Fraction(1)]
        ],
        "expected_GS": [
            [Fraction(1),   Fraction(1),    Fraction(0)],
            [Fraction(1,2), Fraction(-1,2), Fraction(1)],
            [Fraction(-2,3),Fraction(2,3),  Fraction(2,3)]
        ],
        "expected_mu": [
            [Fraction(1),   Fraction(0),    Fraction(0)],
            [Fraction(1, 2),Fraction(1),    Fraction(0)],
            [Fraction(1, 2),Fraction(1, 3), Fraction(1)]
        ]
    },
    {
        "name": "test_vector_2",
        "B": [
            [Fraction(1),   Fraction(1),    Fraction(1)],
            [Fraction(1),   Fraction(-1),   Fraction(2)],
            [Fraction(-1),  Fraction(1),    Fraction(3)]
        ],
        "expected_GS": [
            [Fraction(1),       Fraction(1),    Fraction(1)],
            [Fraction(1,3),     Fraction(-5,3), Fraction(4,3)],
            [Fraction(-15,7),   Fraction(5,7),  Fraction(10,7)]
        ],
        "expected_mu": [
            [Fraction(1),   Fraction(0),    Fraction(0)],
            [Fraction(2, 3),Fraction(1),    Fraction(0)],
            [Fraction(1),   Fraction(3, 7), Fraction(1)]
        ]
    },
    {
        "name": "test_vector_3",
        "B": [
            [Fraction(1),   Fraction(2)],
            [Fraction(6),   Fraction(2)],
            [Fraction(2),   Fraction(3)]
        ],
        "expected_GS": [
            [Fraction(1),   Fraction(2)],
            [Fraction(4),   Fraction(-2)],
            [Fraction(0),   Fraction(0)]
        ],
        "expected_mu": [
            [Fraction(1),   Fraction(0),    Fraction(0)],
            [Fraction(2),   Fraction(1),    Fraction(0)],
            [Fraction(8,5), Fraction(1, 10), Fraction(1)]
        ]
    }
]


def test_GS0(test_cases=TEST_CASES_GramSchmidt):
    """Gram-Schmidt直交化
    """
    print(TEST_FUNCTION_LINE)
    print(f"= {inspect.currentframe().f_code.co_name}()")
    print( "= test GS0(B, n) = (GS, mu)")
    print(TEST_FUNCTION_LINE)
    
    # TEST CASE 
    for i, test_case in enumerate(test_cases):
        DISP_SPACE = 5
        
        print(TEST_CASES_LINE)
        print(f"- test case {i + 1}: {test_case['name']}")
        print(TEST_CASES_LINE)
    
        # 入力
        B = test_case["B"]
        n = len(B)
        m = len(B[0])
        # 期待値
        expected_GS = test_case["expected_GS"]
        expected_mu = test_case["expected_mu"]
        
        # 入力値表示
        header = "n        = "
        print(header, n)
        header = "m        = "
        print(header, m)
        
        header = "B        = "
        print_matrix(B,  space_num=DISP_SPACE, header=header)
        
        # テスト対象
        GS, mu = GS0(B, n,m)
        
        # 出力表示
        header = "GS       = "
        print_matrix(GS, space_num=DISP_SPACE, header=header)
        header = "mu       = "
        print_matrix(mu, space_num=DISP_SPACE, header=header)
        
        # グラムｰシュミットの直交化ベクトルの直交性の確認
        # <b_i^*,b_j^*> = 0 (i != j)
        for i in range(n):
            for j in range(i):
                orthogonality = dot(GS[i],GS[j])
                assert orthogonality == 0
                
        # 期待値比較
        assert GS == expected_GS
        assert mu == expected_mu
    
    print(f"All test cases for {inspect.currentframe().f_code.co_name}() passed")
    print()


# py -m pqc.lattice.test.test_math_gram_schmidt > test.tmp
if __name__ == "__main__":

    test_GS0()
    
