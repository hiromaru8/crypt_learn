from fractions import Fraction
from pqc.lattice.math.round_fraction import round_fraction


def test(x: Fraction):
    
    result = round_fraction(x)
    print(result)


# py -m pqc.lattice.test.test_round_fraction
if __name__ == "__main__":
    
    for i in range(1,10,1):
        print(f"1/{i} = ",end="")
        x = Fraction(1,i)
        test(x)
    
    test(Fraction(-3,2))
    
    