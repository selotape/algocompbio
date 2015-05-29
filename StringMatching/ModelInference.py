from pprint import PrettyPrinter
from collections import defaultdict

from Viterbi import viterbi




# ##CONSTANTS###
DEFAULT_MARGIN = 0.005
VITERBI = 'viterbi'
BAUM_WELCH = 'baum-welch'

pprint = PrettyPrinter(indent=4).pprint


def sufficient_transition_statistics(states, path):
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


def sufficient_emission_statistics(states, alphabet, path, X):
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

    while last_logprob != current_logprob:
        last_logprob = current_logprob

        Nt = sufficient_transition_statistics(states, last_path)
        Ne = sufficient_emission_statistics(states, alphabet, last_path, X)
        current_logprob, current_path = viterbi(X, states, S, Nt, Ne)

        print current_logprob, current_path

    return Ne, Nt


def baum_welch_inference(X, S, E, T, sigma):
    pass


def infer_model(method, X, S, E, T, alphabet, states, sigma=DEFAULT_MARGIN):

    if ('viterbi' == method):
        E, T = viterbi_inference(X, S, E, T, alphabet, states)
    elif 'baum-welch' == method:
        E, T = baum_welch_inference(X, S, E, T, sigma)
    else:
        raise NotImplementedError("algorithm " + method + " is yet to be invented.")
    return E, T


def test_inferences():
    method = VITERBI

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
















