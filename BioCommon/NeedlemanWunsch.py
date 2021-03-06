__author__ = 'ronvis'

from BioCommon.Helper import generate_score_function, needleman_wunch_printer


def initMatrix(S, T, sigma):
    """
    :rtype : str[][]
    """

    # create a zero matrix
    matrix = [[0 for x in range(len(S) + 1)] for x in range(len(T) + 1)]

    gapscore = sigma('a', '_')

    # fill first line & column
    for i in range(len(S) + 1):
        matrix[0][i] = i * gapscore

    for j in range(len(T) + 1):
        matrix[j][0] = j * gapscore

    # start hardcore calculation
    for i in range(1, len(S) + 1, 1):
        for j in range(1, len(T) + 1, 1):
            # decide and score
            align = matrix[j - 1][i - 1] + sigma(S[i - 1], T[j - 1])
            sgap = matrix[j - 1][i] + gapscore
            tgap = matrix[j][i - 1] + gapscore
            pick = max(align, sgap, tgap)
            matrix[j][i] = pick

    return matrix


def printScoreMatrix(S, T, sigma):
    matrix = initMatrix(S, T, sigma)
    needleman_wunch_printer(S, T, matrix)


def test():
    # S = random_dna(length=5)
    # T = random_dna(length=10)
    S = 'GCATCGATTCCGAGC'
    T = 'GCCATGATGAAC'
    sigma = generate_score_function(2, -2, -3)

    printScoreMatrix(S, T, sigma)


if __name__ == '__main__':
    test()