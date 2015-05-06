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


def generateScoreFunction(xx, xy, x_):
    return scoreFunction(xx, xy, x_).score