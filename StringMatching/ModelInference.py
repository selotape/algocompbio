from copy import deepcopy
from sys import maxint
from pprint import PrettyPrinter

__author__ = 'ronvis'


# ##CONSTANTS###
DEFAULT_MARGIN = 0.005
VITERBI = 'viterbi'
BAUMWELCH = 'baum-welch'
MIN_INF = -maxint

pprint = PrettyPrinter(indent=4).pprint


def viterbiInference(X, S, E, T):
    E_, T_ = deepcopy((E, T))

    print id(E), id(E_)

    return E_, T_


def baumWelchInference(X, S, E, T, sigma):
    pass


def inferModel(X, method, S, E, T, sigma=DEFAULT_MARGIN):
    """

    :rtype : object
    """
    if ('viterbi' == method):
        E, T = viterbiInference(X, S, E, T)
    elif 'baum-welch' == method:
        E, T = baumWelchInference(X, S, E, T, sigma)
    else:
        raise NotImplementedError("This algorithm is yet to be invented.")
    return E, T


def testInferences():
    method = VITERBI

    X = '1101000'

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

    E, T = inferModel(X, method, S, E, T)
    pprint(E)
    pprint(T)


testInferences()

