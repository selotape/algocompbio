__author__ = 'Wikipedia'
from math import log, fsum, exp


# NOTE - assumes trans_p & emit_p contain no zeros
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = log(start_p[y] * emit_p[y][obs[0]])
        path[y] = [y]


    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            (logprob, state) = max((V[t - 1][y0] + log(trans_p[y0][y]) + log(emit_p[y][obs[t]]), y0) for y0 in states)
            V[t][y] = logprob
            newpath[y] = path[state] + [y]

        # Don't need to remember the old paths
        path = newpath

    print_dptable(V)
    (logprob, state) = max((V[t][y], y) for y in states)
    return (logprob, path[state])


def forward_viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    # Initialize base cases.
    for y in states:
        V[0][y] = log(start_p[y]) + log(emit_p[y][obs[0]])

    # Run Forward for t > 0
    for t in range(1, len(obs)):
        V.append({})

        for y in states:
            a_max = max(V[t - 1][y0] + log(trans_p[y0][y]) for y0 in states)
            b_sum = sum(exp(V[t - 1][y0] + log(trans_p[y0][y]) - a_max) for y0 in states)
            V[t][y] = log(b_sum) + a_max + log(emit_p[y][obs[t]])

    print '=== log scale==='
    print_dptable(V)

    # V_exp = V
    # print '===prob scale==='
    # for t in range(0, len(obs)):
    # for y in states:
    #         V_exp[t][y] = exp(V[t][y])
    # print_dptable(V_exp)


    prob = fsum([exp(x) for x in V[t].values()])
    return prob


# Don't study this, it just prints a table of the steps.
def print_dptable(V):
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for y in V[0]:
        s += "%.5s: " % y
        s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
        s += "\n"
    print(s)


def example():

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


print("result: " + str(example()))

