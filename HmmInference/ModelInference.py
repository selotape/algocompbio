import argparse
from pprint import PrettyPrinter

from HmmInference.HmmInferenceViterbi import viterbi_inference
from HmmInferenceBaumWelch import baum_welch_inference





# # # CONSTANTS # # #
_DEFAULT_MARGIN = 0.001
_VITERBI = 'Viterbi'
_BAUM_WELCH = 'BaumWelch'
pprint = PrettyPrinter(indent=4).pprint


def infer_model(method, observation, start_p, emission_p, transmission_p, alphabet, states, sigma=_DEFAULT_MARGIN):
    if _VITERBI == method:
        viterbi_inference(observation, start_p, emission_p, transmission_p, alphabet, states)
    elif _BAUM_WELCH == method:
        baum_welch_inference(observation, start_p, emission_p, transmission_p, sigma, alphabet, states)
    else:
        raise NotImplementedError("algorithm \'%s\' is yet to be invented." % method)


def test_inferences():
    method = _BAUM_WELCH
    # method = _VITERBI

    alphabet = ['0', '1']

    X = '1110111010100000010101011111001000000'

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

    infer_model(method, X, S, E, T, alphabet, states)
    # print "Emmissions:"
    # pprint(E)
    # print "Transitions:"
    # pprint(T)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute HMM inference')
    parser.add_argument('observation', type=str)
    parser.add_argument('algorithm', type=str)
    parser.add_argument('hmm_params', type=float, nargs='+')
    args = parser.parse_args()

    prm = args.hmm_params
    S = {'A': 0.5, 'B': 0.5, 'C': 0.0, 'D': 0.0}
    E = {
        'A': {'0': prm[2], '1': 1 - prm[2]},
        'B': {'0': prm[5], '1': 1 - prm[5]},
        'C': {'0': prm[8], '1': 1 - prm[8]},
        'D': {'0': prm[11], '1': 1 - prm[11]}
    }
    T = {
        'A': {'A': 1 - prm[0] - prm[1], 'B': prm[0], 'C': prm[1], 'D': 0.0},
        'B': {'A': prm[3], 'B': 1 - prm[3] - prm[4], 'C': 0.0, 'D': prm[4]},
        'C': {'A': prm[6], 'B': prm[7], 'C': 1 - prm[6] - prm[7], 'D': 0.0},
        'D': {'A': prm[9], 'B': prm[10], 'C': 0.0, 'D': 1 - prm[9] - prm[10]}
    }

    states = S.keys()
    alphabet = E.values()[0].keys()
    algorithm = args.algorithm
    observation = args.observation

    infer_model(algorithm, observation, S, E, T, alphabet, states)
    # test_inferences()

















