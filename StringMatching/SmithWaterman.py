__author__ = 'ronvis'

from StringMatching.NWHelper import generateScoreFunction

def initMatrix(S, T, sigma):
    # create a zero matrix
    matrix = [[0 for x in range(len(S)+1)] for x in range(len(T)+1)]

    gapScore = sigma('a', '_')

    path = ''
    # start hardcore calculation
    for i in range(1, len(S)+1, 1):
        for j in range(1, len(T)+1, 1):
            # decide and score
            align = matrix[j-1][i-1] + sigma(S[i-1], T[j-1])
            SGap = matrix[j-1][i] + gapScore
            TGap = matrix[j][i-1] + gapScore
            pick = max(align, SGap, TGap, 0)
            matrix[j][i] = pick

    return matrix


def printScoreMatrix(S, T, sigma):
    matrix = initMatrix(S, T, sigma)

    printableS = '       ' + '   '.join(S)
    printableT = ' ' + T
    print printableS

    i = 0
    for row in matrix:
        print printableT[i] + ' ' + str(row)
        i=i+1


if __name__ == "__main__":
    # S = randomDna(length=5)
    # T = randomDna(length=10)
    S = 'GCATCGATTCCGAGC'
    T = 'GCCATGATGAAC'
    sigma = generateScoreFunction(2, -2, -3)

    printScoreMatrix(S, T, sigma)