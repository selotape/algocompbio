__author__ = 'ronvis'
from collections import defaultdict
from pprint import PrettyPrinter

pprint = PrettyPrinter.pprint

class PhylogenyTree:
    def __init__(self, name, nucleotide='', children=[], father=None, nucleotide_probabilities=defaultdict(int)):
        self.name = name
        self.nucleotide = nucleotide
        self.children = children
        self.father = father
        self.nucleotide_probabilities = nucleotide_probabilities


    def is_leaf(self):
        if not self.children:
            return True
        else:
            return False

    def __str__(self, level=0):
        ret = self.name
        if self.is_leaf():
            ret = '(' + ret + ')'
        ret = "\t" * level + ret + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)

        return ret

    def __repr__(self):
        return '<tree node representation>'