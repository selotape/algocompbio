__author__ = 'ronvis'
from collections import defaultdict


class PhylogenyTree:
    def __init__(self):
        print 'initialize meeeeeeeeee'
        self.children = None
        self.father = None
        self.nucleotide = 'A'
        self.nucleotide_probabilities = defaultdict(int)


