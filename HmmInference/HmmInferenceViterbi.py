from collections import defaultdict

from BioCommon.Consts import *
from BioCommon.Helper import header_printer
from BioCommon.Helper import printer
from StringAlignments.Viterbi import viterbi


def sufficient_transition_statistics(states, path):
    # init
    Nt = {}
    for state in states:
        Nt[state] = defaultdict(int)

    # calculate
    for current, next in zip(path, path[1:]):
        Nt[current][next] += 1

    for a in states:
        for b in states:
            Nt[a][b] += PSEUDO_COUNT

    # normalize
    for a in states:
        total_appearances = sum(Nt[a].values())

        for b in states:
            if total_appearances:
                Nt[a][b] = float(Nt[a][b]) / total_appearances
            else:  # when the state is unobserved we'll arbitrarily assign equal transition probabilities
                Nt[a][b] = 1.0 / len(states)
        Nt[a] = dict(Nt[a])

    return Nt


def sufficient_emission_statistics(states, alphabet, path, X):
    # init
    Ne = {}
    for state in states:
        Ne[state] = defaultdict(int)

    # calculate
    for state, emit in zip(path, X):
        Ne[state][emit] += 1

    for state in states:
        for c in alphabet:
            Ne += PSEUDO_COUNT

    # normalize
    for state in states:
        total_appearances = sum(Ne[state].values())
        for char in alphabet:
            if total_appearances:
                Ne[state][char] = float(Ne[state][char]) / total_appearances
            else:  # when the state is unobserved we'll arbitrarily assign equal transition probabilities
                Ne[state][char] = 1.0 / len(alphabet)
        Ne[state] = dict(Ne[state])

    return Ne


def viterbi_inference(X, S, E, T, alphabet, states):
    current_logprob, last_path = viterbi(X, states, S, T, E)
    last_logprob, current_path = 0, []

    header_printer(X)
    while last_logprob != current_logprob:  # TODO - instead of equality, change stop condition to rely on the required diff
        printer(T, E, current_logprob)

        last_logprob = current_logprob

        T = sufficient_transition_statistics(states, last_path)
        E = sufficient_emission_statistics(states, alphabet, last_path, X)
        current_logprob, current_path = viterbi(X, states, S, T, E)

    printer(T, E, current_logprob)
    return T, E, current_logprob