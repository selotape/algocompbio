from PhylogenyTrees.PhylogenyTree import PhylogenyTree

__author__ = 'ronvis'

C = 'C'
T = 'T'
G = 'G'
A = 'A'
DNA_NUCLEOTIDES = [A, G, T, C]



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
    return tree


def bottom_up(tree):
    tree = initialize(tree)
    tree = update(tree)
    return tree


def top_down(tree):
    return tree


def caculate_most_likely_ancestral_states(tree):
    tree = bottom_up(tree)
    tree = top_down(tree)

    return tree


def build_tree_for_exercise():
    A_leaf = PhylogenyTree(name='A', nucleotide=G)
    B_leaf = PhylogenyTree(name='B', nucleotide=T)
    C_leaf = PhylogenyTree(name='C', nucleotide=G)
    D_leaf = PhylogenyTree(name='D', nucleotide=T)
    E_leaf = PhylogenyTree(name='E', nucleotide=G)
    F_leaf = PhylogenyTree(name='F', nucleotide=T)

    G_node = PhylogenyTree(name='G', children=[A_leaf, B_leaf])
    H_node = PhylogenyTree(name='H', children=[E_leaf, F_leaf])

    I_node = PhylogenyTree(name='I', children=[G_node, C_leaf])
    J_node = PhylogenyTree(name='J', children=[D_leaf, H_node])

    K_node = PhylogenyTree(name='K', children=[I_node, J_node])

    return K_node

if __name__ == "__main__":
    tree = build_tree_for_exercise()
    tree = caculate_most_likely_ancestral_states(tree)
    print tree

