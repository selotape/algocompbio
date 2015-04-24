from NWHelper import generateScoreFunction, randomDna
from NeedlemanWunsch import printScoreMatrix

def test():
    # S = randomDna(length=5)
    # T = randomDna(length=10)
    S = 'GCATCGATTCCGAGC'
    T = 'GCCATGATGAAC'
    sigma = generateScoreFunction(2, -2, -3)

    printScoreMatrix(S, T, sigma)


if __name__ == "__main__":
    test()






