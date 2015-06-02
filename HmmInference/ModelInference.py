import argparse
from pprint import PrettyPrinter

from BioCommon.Helper import random_hmm_args, header_printer, printer
from HmmInference.HmmInferenceViterbi import viterbi_inference
from HmmInferenceBaumWelch import baum_welch_inference



# # # CONSTANTS # # #
_DEFAULT_MARGIN = 0.001
_VITERBI = 'Viterbi'
_BAUM_WELCH = 'BaumWelch'
pprint = PrettyPrinter(indent=4).pprint


def infer_model(method, observation, start_p, emission_p, transmission_p, alphabet, states, sigma=_DEFAULT_MARGIN):
    if _VITERBI == method:
        T, E, current_logprob = viterbi_inference(observation, start_p, emission_p, transmission_p, alphabet, states)
    elif _BAUM_WELCH == method:
        T, E, current_logprob = baum_welch_inference(observation, start_p, emission_p, transmission_p, sigma, alphabet,
                                                     states)
    else:
        raise NotImplementedError("algorithm \'%s\' is yet to be invented." % method)

    return T, E, current_logprob


if __name__ == '__main__':
    # TODO - tidy up messy, long main. do this by extracting the initialization in inference to a subroutine

    parser = argparse.ArgumentParser(description='Execute HMM inference')
    parser.add_argument('-attempts', type=int, default=1)
    parser.add_argument('-hmm_params', type=float, nargs='+', default=random_hmm_args())
    parser.add_argument('algorithm', type=str)
    parser.add_argument('observation', type=str)
    args = parser.parse_args()

    attempts = args.attempts
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

    best_T, best_E, best_log_likelihood = infer_model(algorithm, observation, S, E, T, alphabet, states)
    attempts -= 1

    if attempts < 1:
        exit()

    while attempts > 0:
        prm = random_hmm_args()
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
        _T, _E, current_log_likelihood = infer_model(algorithm, observation, S, E, T, alphabet, states)
        if current_log_likelihood > best_log_likelihood:
            best_T, best_E, best_log_likelihood = _T, _E, current_log_likelihood
        attempts -= 1

    print '\n\n\n'
    print '----------------- AND THE GRAND WINNER IS... -----------------'
    header_printer(observation)
    printer(best_T, best_E, best_log_likelihood)