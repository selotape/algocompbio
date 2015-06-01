from pprint import PrettyPrinter
import math

from BioCommon.Helper import init_dict_matrix
from BioCommon.Helper import MIN_INF, log0
from BioCommon.Helper import printer, header_printer
from StringAlignments.Viterbi import forward
from StringAlignments.Viterbi import backward









# TODO - remove after debug print are removed.
pprint = PrettyPrinter(indent=4).pprint


def sufficient_statistics(states, alphabet, F, B, T, E, X, log_likelihood):
    E_Ne = init_dict_matrix(states, alphabet, 0)
    E_Nt = init_dict_matrix(states, states, 0)

    # calculate
    for i in range(0, len(X)):
        for state in states:
            if i < len(X) - 1:
                for to_state in states:
                    E_Nt[state][to_state] += \
                        math.exp(
                            log0(T[state][to_state]) + F[i + 1][state] + B[i + 2][to_state] +
                            log0(E[to_state][X[i + 1]])
                            - log_likelihood)  # observation index starts from 0, f and b start from 1
            E_Ne[state][X[i]] += math.exp(F[i + 1][state] + B[i + 1][state] - log_likelihood)

    # normalize
    for state in states:
        # emissions:
        sum = math.fsum(E_Ne[state].itervalues())
        for c in ['0', '1']:
            E_Ne[state][c] = E_Ne[state][c] / sum if sum > 0 else 0

        # transmitions:
        sum = math.fsum(E_Nt[state].itervalues())
        for to_state in states:
            E_Nt[state][to_state] = E_Nt[state][to_state] / sum if sum > 0 else 0

    return E_Nt, E_Ne


def baum_welch_inference(X, S, E, T, sigma, alphabet, states):
    F, forward_likelihood = forward(X, states, S, T, E)
    B, backward_likelihood = backward(X, states, S, T, E)

    last_log_likelihood = MIN_INF
    current_log_likelihood = MIN_INF + 1

    header_printer(X)
    while ( current_log_likelihood - last_log_likelihood > sigma ):
        last_log_likelihood = current_log_likelihood

        F, forward_likelihood = forward(X, states, S, T, E)
        B, backward_likelihood = backward(X, states, S, T, E)

        current_log_likelihood = log0(forward_likelihood)
        printer(T, E, current_log_likelihood)

        T, E = sufficient_statistics(states, alphabet, F, B, T, E, X, current_log_likelihood)

    printer(T, E, current_log_likelihood)
    return E, T


