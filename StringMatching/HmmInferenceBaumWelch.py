from pprint import PrettyPrinter

from Helper import init_dict_matrix
from Helper import MIN_INF, log0
from viterbi_shay import forward
from viterbi_shay import backward

# TODO - remove after debug print are removed.
pprint = PrettyPrinter(indent=4).pprint


def sufficient_transition_statistics(states, F, B, T, E, X):
    E_Nt = init_dict_matrix(states, states, 0)

    # calculate
    for j in states:
        for l in states:
            E_Nt[j][l] = T[j][l] * sum((F[i][j] * E[l][X[i + 1]] * B[i + 1][l]) for i in range(1, len(X) - 1))
    # normalize
    for j in states:
        column_sum = sum(E_Nt[j][i] for i in states)
        for l in states:
            E_Nt[j][l] = E_Nt[j][l] / column_sum

    return E_Nt


def sufficient_emission_statistics(states, alphabet, F, B, T, E, X):
    E_Ne = init_dict_matrix(states, alphabet, 0)

    indices = {c: [] for c in alphabet}
    for i in range(len(X)):
        # indices[X[i]].append(i)
        indices[X[i]].append(i + 1)

    for j in states:
        for c in alphabet:
            E_Ne[j][c] = sum(F[i][j] * B[i][j] for i in indices[c])

    # normalize
    for j in states:
        column_sum = sum(E_Ne[j][c] for c in alphabet)
        for c in alphabet:
            E_Ne[j][c] = E_Ne[j][c] / column_sum

    return E_Ne

def baum_welch_inference(X, S, E, T, sigma, alphabet, states):
    F, forward_likelihood = forward(X, states, S, T, E)
    B, backward_likelihood = backward(X, states, S, T, E)

    last_log_likelihood = MIN_INF
    current_log_likelihood = log0(forward_likelihood)

    while ( current_log_likelihood - last_log_likelihood > sigma ):
        Nt = sufficient_transition_statistics(states, F, B, T, E, X)
        Ne = sufficient_emission_statistics(states, alphabet, F, B, T, E, X)

        T = Nt
        E = Ne

        F, forward_likelihood = forward(X, states, S, T, E)
        B, backward_likelihood = backward(X, states, S, T, E)

        last_log_likelihood = current_log_likelihood
        current_log_likelihood = log0(forward_likelihood)

        print 'Transissions:'
        pprint(T)
        print 'Emissions:'
        pprint(E)
        print 'last_log_likelihood:', last_log_likelihood
        print 'current_log_likelihood:', current_log_likelihood
        print '===================================='
        exit()

    return E, T


