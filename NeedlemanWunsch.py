__author__ = 'ronvis'


def initMatrix(S, T, sigma):
    # create a zero matrix
    matrix = [[0 for x in range(len(S)+1)] for x in range(len(T)+1)]

    gapScore = sigma('a', '_')

    # fill first line & column
    for i in range(len(S)+1):
        matrix[0][i] = i*gapScore

    for j in range(len(T)+1):
        matrix[j][0] = j*gapScore

    del i, j

    # start hardcore calculation
    for i in range(1, len(S)+1, 1):
        for j in range(1, len(T)+1, 1):
            print i, j
            # decide and score
            align = matrix[j-1][i-1] + sigma(S[i-1], T[j-1])
            SGap = matrix[j-1][i] + gapScore
            TGap = matrix[j][i-1] + gapScore
            matrix[j][i] = max(align, SGap, TGap)

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