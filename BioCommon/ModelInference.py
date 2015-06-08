import argparse

from BioCommon.Helper import random_hmm_args, header_printer, printer
from BioCommon.Consts import *
from BioCommon.ViterbiInference import viterbi_inference
from BaumWelchInference import baum_welch_inference


def infer_model(method, observation, start_p, emission_p, transmission_p, alphabet, states, sigma=DEFAULT_MARGIN):
    if VITERBI == method:
        T, E, current_logprob = viterbi_inference(observation, start_p, emission_p, transmission_p, alphabet, states)
    elif BAUM_WELCH == method:
        T, E, current_logprob = baum_welch_inference(observation, start_p, emission_p, transmission_p, sigma, alphabet,
                                                     states)
    else:
        raise NotImplementedError("algorithm \'%s\' is yet to be invented." % method)

    return T, E, current_logprob


def emission_matrix(params):
    return {
        'A': {'0': params[2], '1': 1 - params[2]},
        'B': {'0': params[5], '1': 1 - params[5]},
        'C': {'0': params[8], '1': 1 - params[8]},
        'D': {'0': params[11], '1': 1 - params[11]}
    }


def transission_matrix(params):
    return {
        'A': {'A': 1 - params[0] - params[1], 'B': params[0], 'C': params[1], 'D': 0.0},
        'B': {'A': params[3], 'B': 1 - params[3] - params[4], 'C': 0.0, 'D': params[4]},
        'C': {'A': params[6], 'B': params[7], 'C': 1 - params[6] - params[7], 'D': 0.0},
        'D': {'A': params[9], 'B': params[10], 'C': 0.0, 'D': 1 - params[9] - params[10]}
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