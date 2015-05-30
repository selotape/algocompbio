__author__ = 'ronvis'
from collections import defaultdict

from Viterbi import viterbi


def sufficient_transition_statistics_viterbi(states, path):
    # init
    Nt = {}
    for state in states:
        Nt[state] = defaultdict(int)

    # calculate
    for current, next in zip(path, path[1:]):
        Nt[current][next] += 1


    # normalize
    for a in states:
        total_appearances = sum(Nt[a].values())

        for b in states:
            if total_appearances:
                Nt[a][b] = float(Nt[a][b]) / total_appearances
            else:  # when the state is unobserved we'll arbitrarily assign equal transition probabilities
                Nt[a][b] = 1.0 / len(states)
        Nt[a] = dict(Nt[a])

    # print 'path:', path
    # print 'Nt', Nt
    return Nt


def sufficient_emission_statistics_viterbi(states, alphabet, path, X):
    # init
    Ne = {}
    for state in states:
        Ne[state] = defaultdict(int)

    # calculate
    for state, emit in zip(path, X):
        Ne[state][emit] += 1

    # normalize
    for state in states:
        total_appearances = sum(Ne[state].values())
        for char in alphabet:
            if total_appearances:
                Ne[state][char] = float(Ne[state][char]) / total_appearances
            else:  # when the state is unobserved we'll arbitrarily assign equal transition probabilities
                Ne[state][char] = 1.0 / len(alphabet)
        Ne[state] = dict(Ne[state])

    # print 'path:', path
    # print 'X:', X
    # print 'Ne', Ne
    return Ne


def viterbi_inference(X, S, E, T, alphabet, states):
    last_logprob, last_path = viterbi(X, states, S, T, E)
    print last_logprob, last_path
    current_logprob, current_path = 0, []

    while last_logprob != current_logprob:  # TODO - instead of equality, change stop condition to rely on the required diff
        last_logprob = current_logprob

        Nt = sufficient_transition_statistics_viterbi(states, last_path)
        Ne = sufficient_emission_statistics_viterbi(states, alphabet, last_path, X)
        current_logprob, current_path = viterbi(X, states, S, Nt, Ne)

        print current_logprob, current_path

    return Ne, Nt