__author__ = 'ronvis'

from BioCommon.Helper import generate_score_function


def initMatrix(S, T, homology):
    """
    :rtype : str[][]
    """

    # create a zero matrix
    matrix = [[0 for x in range(len(S) + 1)] for x in range(len(T) + 1)]
    matrix[0][0] = 1  # null match is 100%

    gapOdd = homology('a', '_')

    # start hardcore calculation
    for i in range(1, len(S) + 1, 1):
        for j in range(1, len(T) + 1, 1):
            # decide and score
            align = matrix[j - 1][i - 1] * homology(S[i - 1], T[j - 1])
            sgap = matrix[j - 1][i] * gapOdd
            tgap = matrix[j][i - 1] * gapOdd

            matrix[j][i] = align + sgap + tgap

    return matrix


def test():
    # S = random_dna(length=5)
    # T = random_dna(length=10)
    S = 'GCATCGATTCCGAGC'
    T = 'GCCATGATGAAC'
    homology = generate_score_function(32.0 / 160, 2.0 / 160, 1.0 / 160)

    matrix = initMatrix(S, T, homology)

    # needleman_wunch_printer(S, T, matrix)
    print 'sumHomology: ', str(matrix[len(T)][len(S)])


if __name__ == '__main__':
    test()