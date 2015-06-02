import argparse

from BioCommon.Helper import random_hmm_args, header_printer, printer
from BioCommon.Consts import *
from HmmInferenceViterbi import viterbi_inference
from HmmInferenceBaumWelch import baum_welch_inference


def infer_model(method, observation, start_p, emission_p, transmission_p, alphabet, states, sigma=DEFAULT_MARGIN):
    if VITERBI == method:
        T, E, current_logprob = viterbi_inference(observation, start_p, emission_p, transmission_p, alphabet, states)
    elif BAUM_WELCH == method:
        T, E, current_logprob = baum_welch_inference(observation, start_p, emission_p, transmission_p, sigma, alphabet,
                                                     states)
    else:
        raise NotImplementedError("algorithm \'%s\' is yet to be invented." % method)

    return T, E, current_logprob


def emission_matrix(prm):
    return {
        'A': {'0': prm[2], '1': 1 - prm[2]},
        'B': {'0': prm[5], '1': 1 - prm[5]},
        'C': {'0': prm[8], '1': 1 - prm[8]},
        'D': {'0': prm[11], '1': 1 - prm[11]}
    }


def transission_matrix(prm):
    return {
        'A': {'A': 1 - prm[0] - prm[1], 'B': prm[0], 'C': prm[1], 'D': 0.0},
        'B': {'A': prm[3], 'B': 1 - prm[3] - prm[4], 'C': 0.0, 'D': prm[4]},
        'C': {'A': prm[6], 'B': prm[7], 'C': 1 - prm[6] - prm[7], 'D': 0.0},
        'D': {'A': prm[9], 'B': prm[10], 'C': 0.0, 'D': 1 - prm[9] - prm[10]}
    }


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Execute HMM inference')
    parser.add_argument('-attempts', type=int, default=1)
    parser.add_argument('-hmm_params', type=float, nargs='+', default=random_hmm_args())
    parser.add_argument('-algorithm', type=str)
    parser.add_argument('-observation', type=str)
    args = parser.parse_args()

    attempts = args.attempts
    prm = args.hmm_params
    alphabet = ['0', '1']
    S = {'A': 0.5, 'B': 0.5, 'C': 0.0, 'D': 0.0}
    states = S.keys()
    algorithm = args.algorithm
    observation = args.observation

    best_log_likelihood = float('-inf')
    while attempts > 0:
        E = emission_matrix(prm)
        T = transission_matrix(prm)
        _T, _E, current_log_likelihood = infer_model(algorithm, observation, S, E, T, alphabet, states)
        if current_log_likelihood > best_log_likelihood:
            best_T, best_E, best_log_likelihood = _T, _E, current_log_likelihood
        attempts -= 1

        prm = random_hmm_args()


    print '\n\n\n'
    print '--------------------------------------------------------------'
    print '----------------- AND THE GRAND WINNER IS... -----------------'
    header_printer(observation)
    printer(best_T, best_E, best_log_likelihood)