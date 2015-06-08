__author__ = 'ronvis'

from BioCommon.Helper import generate_score_function, needleman_wunch_printer


def init_matrix(S, T, sigma):
    # create a zero matrix
    matrix = [[0 for x in range(len(S) + 1)] for x in range(len(T) + 1)]

    gapScore = sigma('a', '_')

    # start hardcore calculation
    for i in range(1, len(S) + 1, 1):
        for j in range(1, len(T) + 1, 1):
            # decide and score
            align = matrix[j - 1][i - 1] + sigma(S[i - 1], T[j - 1])
            SGap = matrix[j - 1][i] + gapScore
            TGap = matrix[j][i - 1] + gapScore
            pick = max(align, SGap, TGap, 0)
            matrix[j][i] = pick

    return matrix


def print_score_matrix(S, T, sigma):
    matrix = init_matrix(S, T, sigma)
    needleman_wunch_printer(S, T, matrix)


def test():
    # S = random_dna(length=5)
    # T = random_dna(length=10)
    S = 'GCATCGATTCCGAGC'
    T = 'GCCATGATGAAC'
    sigma = generate_score_function(2, -2, -3)

    print_score_matrix(S, T, sigma)


if __name__ == '__main__':
    test()