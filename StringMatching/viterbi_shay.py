from collections import defaultdict
import math

__author__ = 'ronvis'


def create_defaultdict_of_int():
    return defaultdict(int)


def my_log(x):
    return math.log(x) if x > 0 else float('-inf')


def viterbi(obs, states, start_p, trans_p, emit_p):
    V = defaultdict(dict)
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        V[1][y] = my_log(start_p[y]) + my_log(emit_p[y][obs[0]])
        path[y] = [y]

    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        newpath = {}

        for y in states:
            (prob, state) = max((V[t][y0] + my_log(trans_p[y0][y]) + my_log(emit_p[y][obs[t]]), y0) for y0 in states)
            V[t + 1][y] = prob
            newpath[y] = path[state] + [y]

        # Don't need to remember the old paths
        path = newpath

    # print_dptable(V)
    (prob, state) = max((V[len(obs)][y], y) for y in states)
    best_path = path[state]
    # print (prob, best_path)
    transitions = defaultdict(create_defaultdict_of_int)
    emissions = defaultdict(create_defaultdict_of_int)
    for i in range(0, len(best_path)):
        if i < len(best_path) - 1:
            transitions[best_path[i]][best_path[i + 1]] += 1
        emissions[best_path[i]][obs[i]] += 1
    return (transitions, emissions, prob)


def forward(obs, states, start_p, trans_p, emit_p):
    V = defaultdict(dict)

    # Initialize base cases (t == 0)
    for y in states:
        V[1][y] = my_log(start_p[y]) + my_log(emit_p[y][obs[0]])

    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        for y in states:
            max_a = max(V[t][y0] + my_log(trans_p[y0][y]) for y0 in states)

            sum = 0
            for y0 in states:
                sum += math.exp(V[t][y0] + my_log(trans_p[y0][y]) - max_a)

            prob = my_log(sum) + max_a + my_log(emit_p[y][obs[t]])
            V[t + 1][y] = prob

    # print_dptable(V)
    likelihood = math.fsum(math.exp(x) for x in V[len(obs)].itervalues())
    return (V, likelihood)


def backward(obs, states, start_p, trans_p, emit_p):
    V = defaultdict(dict)

    # Initialize base cases (t == n)
    for y in states:
        V[len(obs)][y] = math.log(1)  # my_log(emit_p[y][obs[-1]])

    # Run Viterbi for t < n
    for t in reversed(range(1, len(obs))):
        for y in states:
            max_a = max(V[t + 1][y0] + my_log(trans_p[y][y0]) + my_log(emit_p[y0][obs[t]]) for y0 in states)

            sum = 0
            for y0 in states:
                sum += math.exp(V[t + 1][y0] + my_log(trans_p[y][y0]) + my_log(emit_p[y0][obs[t]]) - max_a)

            prob = my_log(sum) + max_a
            V[t][y] = prob

    # print_dptable(V)
    likelihood = math.fsum(math.exp(y) * start_p[x] * emit_p[x][obs[0]] for x, y in V[1].iteritems())
    return (V, likelihood)

