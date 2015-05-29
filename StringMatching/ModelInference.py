from copy import deepcopy
from sys import maxint
from pprint import PrettyPrinter
from collections import defaultdict

from Viterbi import viterbi


__author__ = 'ronvis'


# ##CONSTANTS###
DEFAULT_MARGIN = 0.005
VITERBI = 'viterbi'
BAUM_WELCH = 'baum-welch'
MIN_INF = -maxint

pprint = PrettyPrinter(indent=4).pprint


def sufficient_transition_statistics(states, path):
    # init
    Nt = {}
    for state in states:
        Nt[state] = defaultdict(int)

    # calculate
    for current, next in zip(path, path[1:]):
        Nt[current][next] += 1


    # normalize
    for a in states:
        total_appearances = sum(Nt[a].values())

        if total_appearances:
            for b in states:
                Nt[a][b] = float(Nt[a][b]) / total_appearances
        else:  # this state is unobserved so we'll arbitrarily assign equal transition probabilities
            for b in states:
                Nt[a][b] = 1.0 / len(states)

    return Nt


def sufficient_emission_statistics(states, path, X):
    pass


def viterbi_inference(X, S, E, T):
    E1, T1 = deepcopy((E, T))
    E2, T2 = deepcopy((E, T))
    states = E1.keys()

    logprob1, path1 = viterbi(X, states, S, T, E)
    logprob2, path2 = 0, []

    while logprob1 != logprob2:
        Nt = sufficient_transition_statistics(states, path1)
        Ne = sufficient_emission_statistics(states, path1, X)
        # E1, T1 = normalize(Nt, Ne)
        # logprob1, path1 = viterbi(X, states, S, T1, E1)

        logprob1 = logprob2
    return E1, T1


def baum_welch_inference(X, S, E, T, sigma):
    pass


def infer_model(X, method, S, E, T, sigma=DEFAULT_MARGIN):

    if ('viterbi' == method):
        E, T = viterbi_inference(X, S, E, T)
    elif 'baum-welch' == method:
        E, T = baum_welch_inference(X, S, E, T, sigma)
    else:
        raise NotImplementedError("This algorithm is yet to be invented.")
    return E, T


def test_inferences():
    method = VITERBI

    X = '11010011110101010111100011010011010010101101010101000101010101010010101010110101010000001100000011000000110'

    S = {'Trns0': 0.499999, 'Trns1': 0.499999, 'Bckg0': 0.000001, 'Bckg1': 0.000001}

    T = {
        'Trns0': {'Trns0': 0.9 * 0.7, 'Trns1': 0.9 * 0.3, 'Bckg0': 0.099999, 'Bckg1': 0.000001},
        'Trns1': {'Trns0': 0.9 * 0.1, 'Trns1': 0.9 * 0.9, 'Bckg0': 0.000001, 'Bckg1': 0.1},
        'Bckg0': {'Trns0': 0.8 * 0.7, 'Trns1': 0.8 * 0.3, 'Bckg0': 0.199999, 'Bckg1': 0.000001},
        'Bckg1': {'Trns0': 0.8 * 0.1, 'Trns1': 0.8 * 0.9, 'Bckg0': 0.000001, 'Bckg1': 0.199999}
    }

    E = {
        'Trns0': {'0': 0.75, '1': 0.2, 's': 0.05},
        'Trns1': {'0': 0.2, '1': 0.75, 's': 0.05},
        'Bckg0': {'0': 0.5, '1': 0.499999, 's': 0.000001},
        'Bckg1': {'0': 0.5, '1': 0.499999, 's': 0.000001}
    }

    E, T = infer_model(X, method, S, E, T)
    # pprint(E)
    # pprint(T)


test_inferences()

