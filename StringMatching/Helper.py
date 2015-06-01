from random import choice
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

    def  score(self, x, y):
        if (x==y):
            return self.matchScore
        elif (x=='_' or y=='_'):
            return self.gapScore
        else:
            return self.mismatchScore


# print matrix with headers (in csv format)
def my_pretty_print(S, T, matrix):
    printableS = ',,' + ','.join(S)
    printableT = ' ' + T

    print printableS

    i = 0
    for row in matrix:
        print printableT[i] + ',' + ','.join(str(c) for c in row)
        i = i + 1


# print matrix with headers (in csv format) ---- from Liahav
def print_dp(V):
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for y in V[0]:
        s += "%.5s: " % y
        s += " ".join(("%.7s" % ("%f" % v[y]) if v[y] > MIN_INF else "  -INF ") for v in V)
        s += "\n"
    print(s)


def generate_score_function(xx, xy, x_):
    return score_function(xx, xy, x_).score


def init_dict_matrix(rows, columns, default):
    M = {}
    for a in rows:
        M[a] = {}
        for b in columns:
            M[a][b] = default
    return M


def printer(T, E, score):
    print "| %.2f %.2f %.2f  : %.2f %.2f %.2f  : %.2f %.2f %.2f  : %.2f %.2f %.2f  : %.4f |" % \
          (T['T0']['T1'], T['T0']['B0'], E['T0']['0'],
           T['T1']['T0'], T['T1']['B1'], E['T1']['0'],
           T['B0']['T1'], T['B0']['T1'], E['B0']['0'],
           T['B1']['T1'], T['B1']['T1'], E['B1']['0'], score)