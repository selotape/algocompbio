from random import choice


def randomDna(length):

   DNA=""
   for count in range(length):
      DNA+=choice("CGTA")
   return DNA


__author__ = 'ronvis'


class scoreFunction:
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
def prettyPrint(S, T, matrix):
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


def generateScoreFunction(xx, xy, x_):
    return scoreFunction(xx, xy, x_).score