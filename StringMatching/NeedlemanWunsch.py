__author__ = 'ronvis'

from StringMatching.Helper import generateScoreFunction, printCsv


def initMatrix(S, T, sigma):
    # create a zero matrix
    matrix = [[0 for x in range(len(S)+1)] for x in range(len(T)+1)]

    gapScore = sigma('a', '_')

    # fill first line & column
    for i in range(len(S)+1):
        matrix[0][i] = i*gapScore

    for j in range(len(T)+1):
        matrix[j][0] = j*gapScore

    path = ''
    # start hardcore calculation
    for i in range(1, len(S)+1, 1):
        for j in range(1, len(T)+1, 1):
            # decide and score
            align = matrix[j-1][i-1] + sigma(S[i-1], T[j-1])
            SGap = matrix[j-1][i] + gapScore
            TGap = matrix[j][i-1] + gapScore
            pick = max(align, SGap, TGap)
            matrix[j][i] = pick

    return matrix


def printScoreMatrix(S, T, sigma):
    matrix = initMatrix(S, T, sigma)
    printCsv(S, T, matrix)


def test():
    # S = randomDna(length=5)
    # T = randomDna(length=10)
    S = 'GCATCGATTCCGAGC'
    T = 'GCCATGATGAAC'
    sigma = generateScoreFunction(2, -2, -3)

    printScoreMatrix(S, T, sigma)

test()



