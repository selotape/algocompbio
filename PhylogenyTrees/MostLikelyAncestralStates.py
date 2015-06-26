from PhylogenyTrees.PhylogenyTree import PhylogenyTree

__author__ = 'ronvis'

DNA_NUCLEOTIDES = ['A', 'G', 'T', 'C']


def initialize_nonleaf_probabilities(tree):
    pass


def initialize_leaf_probabilities(leaf):
    for nucleotide in DNA_NUCLEOTIDES:
        if nucleotide == leaf.nucleotide:
            leaf.nucleotide_probabilities[nucleotide] = 1.0
        else:
            leaf.nucleotide_probabilities[nucleotide] = 0.0


def initialize(tree):
    if tree.is_leaf():
        initialize_leaf_probabilities(tree)
    else:
        for child in tree.children:
            initialize(child)
        initialize_nonleaf_probabilities(tree)

    return tree


def update(tree):
    pass


def bottom_up(tree):
    tree = initialize(tree)
    tree = update(tree)
    return tree


def top_down(tree):
    return tree


def algorithm(tree):
    tree = bottom_up(tree)
    tree = top_down(tree)

    return tree


def build_tree_for_exercise():
    return PhylogenyTree()


if __name__ == "__main__":
    tree = build_tree_for_exercise()
    tree = algorithm(tree)
    print tree

