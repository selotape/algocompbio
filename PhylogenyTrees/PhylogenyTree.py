from pprint import PrettyPrinter

from PhylogenyTrees.Consts import DNA_NUCLEOTIDES


pprint = PrettyPrinter.pprint


def empty_nucleotide_probabilities():
    return dict([(nucleotide, (0.0, None)) for nucleotide in DNA_NUCLEOTIDES])


def initialize_leaf_probabilities(leaf):
    for nucleotide in DNA_NUCLEOTIDES:
        if nucleotide == leaf.nucleotide:
            leaf.probabilities_dict[nucleotide] = (1.0, None)
        else:
            leaf.probabilities_dict[nucleotide] = (0.0, None)


class PhylogenyTree:
    def __init__(self, name, million_years_ago, nucleotide=None, children=None, nucleotide_probabilities=None):
        self.name = name
        self.million_years_ago = million_years_ago
        self.nucleotide = nucleotide
        self.children = children or []
        self.probabilities_dict = nucleotide_probabilities or empty_nucleotide_probabilities()
        self.subtree_prob = 0.0


    def __str__(self, level=0):
        ret = self.name
        if self.is_leaf():
            ret = '(' + ret + ')'
        # ret = "\t" * level + ret + ' ' + str(self.probabilities_dict) + "\n"
        ret = "\t" * level + ret + ' ' + str(self.nucleotide) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)

        return ret


    def is_leaf(self):
        if not self.children:
            return True
        else:
            return False

    def children_need_updating(self):
        for child in self.children:
            if child.needs_updating():
                return True
        return False

    def needs_updating(self):
        for prob in self.probabilities_dict.values():
            if prob[0] != 0:
                return False
        return True


