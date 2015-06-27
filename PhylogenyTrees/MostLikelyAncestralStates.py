from PhylogenyTrees.PhylogenyTree import PhylogenyTree, initialize_leaf_probabilities
from Consts import *


__author__ = 'ronvis'





def initialize(tree):
    if tree.is_leaf():
        initialize_leaf_probabilities(tree)
    else:
        for child in tree.children:
            initialize(child)
    return tree


def update_children(tree):
    updated_children = []

    for i in range(len(tree.children)):
        child = tree.children[i]
        if child.needs_updating():
            updated_children.append(update(child))
        else:
            updated_children.append(child)

    tree.children = updated_children

    return tree


def do_children_need_updating(tree):
    for child in tree.children:
        if child.needs_updating():
            return True
    return False


def substitution_probability(X, Y, m_year_lapse):
    specific_sub_prob = 0.25 * (1 - math.pow(math.e, -(m_year_lapse * SUBTITUTIONS_PER_M_YEARS)))
    if X != Y:
        return specific_sub_prob
    else:
        return 1 - 3 * specific_sub_prob


def max_prob(X, m_year_lapse, child):  # TODO - find better name

    result = (0.0, None)
    for Y in DNA_NUCLEOTIDES:
        prob = substitution_probability(X, Y, m_year_lapse) * child.probabilities_dict[Y][0]
        if prob > result[0]:
            source = Y
            result = (prob, source)

    return result


def get_best_state_probability(root, nucleotide):
    probabilities_and_sources = []

    X = nucleotide
    for child in root.children:
        m_year_lapse = root.million_years_ago - child.million_years_ago
        (prob, source) = max_prob(X, m_year_lapse, child)
        probabilities_and_sources.append((prob, source))

    sources = []
    mul_probs = 1.0
    for (prob, source) in probabilities_and_sources:
        mul_probs = mul_probs * prob
        sources.append(source)

    return (mul_probs, sources)


def update_root(root):
    updated_probabilities = {}

    for nucleotide in DNA_NUCLEOTIDES:
        updated_probabilities[nucleotide] = get_best_state_probability(root, nucleotide)

    root.probabilities_dict = updated_probabilities

    return root


def update(tree):
    if tree.children_need_updating():
        tree = update_children(tree)
    tree = update_root(tree)


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


def build_tree_for_exercise():  # TODO - shorten, clean, make pretty code
    A_leaf = PhylogenyTree(name='A', million_years_ago=0, nucleotide=G)
    B_leaf = PhylogenyTree(name='B', million_years_ago=0, nucleotide=T)
    C_leaf = PhylogenyTree(name='C', million_years_ago=0, nucleotide=G)
    D_leaf = PhylogenyTree(name='D', million_years_ago=0, nucleotide=T)
    E_leaf = PhylogenyTree(name='E', million_years_ago=0, nucleotide=G)
    F_leaf = PhylogenyTree(name='F', million_years_ago=0, nucleotide=T)

    G_node = PhylogenyTree(name='G', million_years_ago=100, children=[A_leaf, B_leaf])
    H_node = PhylogenyTree(name='H', million_years_ago=100, children=[E_leaf, F_leaf])

    I_node = PhylogenyTree(name='I', million_years_ago=200, children=[G_node, C_leaf])
    J_node = PhylogenyTree(name='J', million_years_ago=200, children=[D_leaf, H_node])

    K_node = PhylogenyTree(name='K', million_years_ago=500, children=[I_node, J_node])

    return K_node

if __name__ == "__main__":
    tree = build_tree_for_exercise()
    tree = caculate_most_likely_ancestral_states(tree)
    print tree

