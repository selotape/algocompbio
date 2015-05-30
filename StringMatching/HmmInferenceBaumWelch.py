from Viterbi import forward_viterbi
from Viterbi import backward_viterbi


def sufficient_transition_statistics_baumwelch(states, F, B, T, E, X):
    # init
    E_Nt = {}
    for a in states:
        E_Nt[a] = {}
        for b in states:
            E_Nt[a][b] = 0


    # calculate
    for j in states:
        for l in states:
            E_Nt[j][l] = T[j][l] * sum(F[i][j] * E[l][X[i + 1] * B[i + 1][l]] for i in len(X)) / (
            sum(F[len(X)][j_] for j_ in states))


    # normalize (OR SHOULD YOU???)
    for j in states:
        for l in states:
            E_Nt[j][l] = E_Nt[j][l] / sum(E_Nt[j][i] for i in states)

    return E_Nt


def sufficient_emission_statistics_baumwelch(states, alphabet, F, B, T, E, X):
    pass


def baum_welch_inference(X, S, E, T, sigma, alphabet, states):
    # calculate likelihood

    last_likelihood = 0
    current_likelihood = 0

    while (
            current_likelihood - last_likelihood > sigma ):  # TODO - instead of equality, change stop condition to rely on the required diff
        last_likelihood = current_likelihood

        F = forward_viterbi(X, S, E, T)
        B = backward_viterbi(X, S, E, T)

        Nt = sufficient_transition_statistics_baumwelch(states, F, B, T, E, X)
        Ne = sufficient_emission_statistics_baumwelch(states, alphabet, F, B, T, E, X)

        # calc current_likelihood

        T = Nt
        E = Ne

    pass
