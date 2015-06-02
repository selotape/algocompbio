from random import choice, random
from math import log
import sys

MIN_INF = -sys.maxint

__author__ = 'ronvis'


def log0(x):
    if x == 0:
        return float('-inf')
    else:
        return log(x)


def random_dna(length):
    DNA = ""
    for count in range(length):
        DNA += choice("CGTA")
    return DNA


class score_function:
    def __init__(self, matchScore, mismatchScore, gapScore):
        self.matchScore = matchScore
        self.mismatchScore = mismatchScore
        self.gapScore = gapScore

    def score(self, x, y):
        if (x == y):
            return self.matchScore
        elif (x == '_' or y == '_'):
            return self.gapScore
        else:
            return self.mismatchScore


# print matrix with headers (in csv format)
def needleman_wunch_printer(S, T, matrix):
    printableS = ',,' + ','.join(S)
    printableT = ' ' + T

    print printableS

    i = 0
    for row in matrix:
        print printableT[i] + ',' + ','.join(str(c) for c in row)
        i = i + 1


def generate_score_function(xx, xy, x_):
    return score_function(xx, xy, x_).score


def init_dict_matrix(rows, columns, default):
    M = {}
    for a in rows:
        M[a] = {}
        for b in columns:
            M[a][b] = default
    return M


def random_hmm_args():
    a = random()
    b = random() * (1 - a)
    c = random()
    d = random()
    e = random() * (1 - d)
    f = random()
    g = random()
    h = random() * (1 - g)
    i = random()
    j = random()
    k = random() * (1 - j)
    l = random()

    return a, b, c, d, e, f, g, h, i, j, k, l


def printer(T, E, score):
    print "| %.2f %.2f %.2f  : %.2f %.2f %.2f  : %.2f %.2f %.2f  : %.2f %.2f %.2f  : %.4f |" % \
          (T['A']['B'], T['A']['C'], E['A']['0'],
           T['B']['A'], T['B']['D'], E['B']['0'],
           T['C']['B'], T['C']['B'], E['C']['0'],
           T['D']['A'], T['D']['B'], E['D']['0'], score)


def header_printer(X):
    if len(X) > 45:
        print ''.join(X)
    else:
        print ' '.join(X)
    print '------------------------------------------------------------------------------------'
    print "| A->B A->C A->0  : B->A B->D B->0  : C->A C->B C->0  : D->A D->B D->0  :   Score  |"
    print '------------------------------------------------------------------------------------'