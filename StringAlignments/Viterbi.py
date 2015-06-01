from math import fsum, exp
from collections import defaultdict

from BioCommon.Helper import log0



# NOTE - assumes trans_p & emit_p contain no zeros
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = log0(start_p[y] * emit_p[y][obs[0]])
        path[y] = [y]

    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            (logprob, state) = max((V[t - 1][y0] + log0(trans_p[y0][y]) + log0(emit_p[y][obs[t]]), y0) for y0 in states)
            V[t][y] = logprob
            newpath[y] = path[state] + [y]

        # Don't need to remember the old paths
        path = newpath

    # print_dptable(V)
    (logprob, state) = max((V[t][y], y) for y in states)
    return (logprob, path[state])


def forward(obs, states, start_p, trans_p, emit_p):
    V = defaultdict(dict)

    # Initialize base cases (t == 0)
    for y in states:
        V[1][y] = log0(start_p[y]) + log0(emit_p[y][obs[0]])

    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        for y in states:
            max_a = max(V[t][y0] + log0(trans_p[y0][y]) for y0 in states)

            sum = 0
            for y0 in states:
                sum += exp(V[t][y0] + log0(trans_p[y0][y]) - max_a)

            prob = log0(sum) + max_a + log0(emit_p[y][obs[t]])
            V[t + 1][y] = prob

    # print_dptable(V)
    likelihood = fsum(exp(x) for x in V[len(obs)].itervalues())
    return dict(V), likelihood


def backward(obs, states, start_p, trans_p, emit_p):
    V = defaultdict(dict)

    # Initialize base cases (t == n)
    for y in states:
        V[len(obs)][y] = log0(1)

    # Run Viterbi for t < n
    for t in reversed(range(1, len(obs))):
        for y in states:
            max_a = max(V[t + 1][y0] + log0(trans_p[y][y0]) + log0(emit_p[y0][obs[t]]) for y0 in states)

            sum = 0
            for y0 in states:
                sum += exp(V[t + 1][y0] + log0(trans_p[y][y0]) + log0(emit_p[y0][obs[t]]) - max_a)

            prob = log0(sum) + max_a
            V[t][y] = prob

    # print_dptable(V)
    likelihood = fsum(exp(y) * start_p[x] * emit_p[x][obs[0]] for x, y in V[1].iteritems())
    return dict(V), likelihood


def noise_and_null_viterbi(obs, states, start_p, trans_p, emit_p, total_emits):
    V = [{}]

    # Initialize base cases.
    for y in states:
        V[0][y] = [0 for m in range(total_emits + 1)]
        for u in range(0, total_emits + 1):
            V[0][y][u] = start_p[y] * pow(emit_p[y]['s'], u)

    # now I have a matrix initialized
    for t in range(0, len(obs)):
        V.append({})
        for y in states:
            V[t][y] = [0 for m in range(total_emits + 1)]
            for u in range(0, total_emits + 1):
                best_with_sigma = 0
                best_with_noise = 0
                # best_with_transmission  =  max(  trans_p[][]*  for p in range(u))
                best_with_transmission = None

                V[t][y][u] = max(best_with_noise, best_with_sigma, best_with_transmission)
    return 0


def example_viterbi():
    observations = '11011000'

    start_probability = {'Trns0': 0.499999, 'Trns1': 0.499999, 'Bckg0': 0.000001, 'Bckg1': 0.000001}

    transition_probability = {
        'Trns0': {'Trns0': 0.9 * 0.7, 'Trns1': 0.9 * 0.3, 'Bckg0': 0.099999, 'Bckg1': 0.000001},
        'Trns1': {'Trns0': 0.9 * 0.1, 'Trns1': 0.9 * 0.9, 'Bckg0': 0.000001, 'Bckg1': 0.1},
        'Bckg0': {'Trns0': 0.8 * 0.7, 'Trns1': 0.8 * 0.3, 'Bckg0': 0.199999, 'Bckg1': 0.000001},
        'Bckg1': {'Trns0': 0.8 * 0.1, 'Trns1': 0.8 * 0.9, 'Bckg0': 0.000001, 'Bckg1': 0.199999}
    }

    emission_probability = {
        'Trns0': {'0': 0.8, '1': 0.2},
        'Trns1': {'0': 0.2, '1': 0.8},
        'Bckg0': {'0': 0.5, '1': 0.5},
        'Bckg1': {'0': 0.5, '1': 0.5}
    }

    return viterbi(observations,
                   emission_probability.keys(),
                   start_probability,
                   transition_probability,
                   emission_probability)


def example_forward():
    observations = '11011000'

    start_probability = {'Trns0': 0.499999, 'Trns1': 0.499999, 'Bckg0': 0.000001, 'Bckg1': 0.000001}

    transition_probability = {
        'Trns0': {'Trns0': 0.9 * 0.7, 'Trns1': 0.9 * 0.3, 'Bckg0': 0.099999, 'Bckg1': 0.000001},
        'Trns1': {'Trns0': 0.9 * 0.1, 'Trns1': 0.9 * 0.9, 'Bckg0': 0.000001, 'Bckg1': 0.1},
        'Bckg0': {'Trns0': 0.8 * 0.7, 'Trns1': 0.8 * 0.3, 'Bckg0': 0.199999, 'Bckg1': 0.000001},
        'Bckg1': {'Trns0': 0.8 * 0.1, 'Trns1': 0.8 * 0.9, 'Bckg0': 0.000001, 'Bckg1': 0.199999}
    }

    emission_probability = {
        'Trns0': {'0': 0.8, '1': 0.2},
        'Trns1': {'0': 0.2, '1': 0.8},
        'Bckg0': {'0': 0.5, '1': 0.5},
        'Bckg1': {'0': 0.5, '1': 0.5}
    }

    return forward(observations,
                           emission_probability.keys(),
                           start_probability,
                           transition_probability,
                           emission_probability)


def example_sigmaI():
    observations = '1101s000'

    start_probability = {'Trns0': 0.499999, 'Trns1': 0.499999, 'Bckg0': 0.000001, 'Bckg1': 0.000001}

    transition_probability = {
        'Trns0': {'Trns0': 0.9 * 0.7, 'Trns1': 0.9 * 0.3, 'Bckg0': 0.099999, 'Bckg1': 0.000001},
        'Trns1': {'Trns0': 0.9 * 0.1, 'Trns1': 0.9 * 0.9, 'Bckg0': 0.000001, 'Bckg1': 0.1},
        'Bckg0': {'Trns0': 0.8 * 0.7, 'Trns1': 0.8 * 0.3, 'Bckg0': 0.199999, 'Bckg1': 0.000001},
        'Bckg1': {'Trns0': 0.8 * 0.1, 'Trns1': 0.8 * 0.9, 'Bckg0': 0.000001, 'Bckg1': 0.199999}
    }

    emission_probability = {
        'Trns0': {'0': 0.75, '1': 0.2, 's': 0.05},
        'Trns1': {'0': 0.2, '1': 0.75, 's': 0.05},
        'Bckg0': {'0': 0.5, '1': 0.499999, 's': 0.000001},
        'Bckg1': {'0': 0.5, '1': 0.499999, 's': 0.000001}
    }

    return viterbi(observations,
                   emission_probability.keys(),
                   start_probability,
                   transition_probability,
                   emission_probability)


def example_sigmaII():
    observations = '1101000'

    start_probability = {'Trns0': 0.499999, 'Trns1': 0.499999, 'Bckg0': 0.000001, 'Bckg1': 0.000001}

    transition_probability = {
        'Trns0': {'Trns0': 0.9 * 0.7, 'Trns1': 0.9 * 0.3, 'Bckg0': 0.099999, 'Bckg1': 0.000001},
        'Trns1': {'Trns0': 0.9 * 0.1, 'Trns1': 0.9 * 0.9, 'Bckg0': 0.000001, 'Bckg1': 0.1},
        'Bckg0': {'Trns0': 0.8 * 0.7, 'Trns1': 0.8 * 0.3, 'Bckg0': 0.199999, 'Bckg1': 0.000001},
        'Bckg1': {'Trns0': 0.8 * 0.1, 'Trns1': 0.8 * 0.9, 'Bckg0': 0.000001, 'Bckg1': 0.199999}
    }

    emission_probability = {
        'Trns0': {'0': 0.75, '1': 0.2, 's': 0.05},
        'Trns1': {'0': 0.2, '1': 0.75, 's': 0.05},
        'Bckg0': {'0': 0.5, '1': 0.499999, 's': 0.000001},
        'Bckg1': {'0': 0.5, '1': 0.499999, 's': 0.000001}
    }

    return noise_and_null_viterbi(observations,
                                  emission_probability.keys(),
                                  start_probability,
                                  transition_probability,
                                  emission_probability,
                                  8)


if __name__ == "__main__":
    print("result: " + str(example_viterbi()))

