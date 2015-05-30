from pprint import PrettyPrinter

from HmmInferenceViterbi import viterbi_inference
from HmmInferenceBaumWelch import baum_welch_inference




# # # CONSTANTS # # #
_DEFAULT_MARGIN = 0.005
_VITERBI = 'viterbi'
_BAUM_WELCH = 'baum-welch'
pprint = PrettyPrinter(indent=4).pprint


def infer_model(method, X, S, E, T, alphabet, states, sigma=_DEFAULT_MARGIN):

    if ('viterbi' == method):
        E, T = viterbi_inference(X, S, E, T, alphabet, states)
    elif 'baum-welch' == method:
        E, T = baum_welch_inference(X, S, E, T, sigma, alphabet, states)
    else:
        raise NotImplementedError("algorithm \'%s\' is yet to be invented." % method)
    return E, T


def test_inferences():
    method = _BAUM_WELCH

    alphabet = ['0', '1']

    X = '11111111111111100000000000000000000111000000111111111111111000000000000'

    S = {'T0': 0.5, 'T1': 0.5, 'B0': 0.0, 'B1': 0.0}

    states = S.keys()

    T = {
        'T0': {'T0': 0.8, 'T1': 0.1, 'B0': 0.1, 'B1': 0.0},
        'T1': {'T0': 0.1, 'T1': 0.6, 'B0': 0.0, 'B1': 0.3},
        'B0': {'T0': 0.8, 'T1': 0.1, 'B0': 0.1, 'B1': 0.0},
        'B1': {'T0': 0.1, 'T1': 0.8, 'B0': 0.0, 'B1': 0.1}
    }

    E = {
        'T0': {'0': 0.9, '1': 0.1},
        'T1': {'0': 0.1, '1': 0.9},
        'B0': {'0': 0.5, '1': 0.5},
        'B1': {'0': 0.5, '1': 0.5}
    }

    E, T = infer_model(method, X, S, E, T, alphabet, states)
    print "Emmissions:"
    pprint(E)
    print "Transitions:"
    pprint(T)


if __name__ == '__main__':
    test_inferences()
















