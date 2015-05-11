__author__ = 'Wikipedia'


def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]

    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            (prob, state) = max((V[t - 1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)
            V[t][y] = prob
            newpath[y] = path[state] + [y]

        # Don't need to remember the old paths
        path = newpath
    n = 0  # if only one element is observed max is sought in the initialization values
    if len(obs) != 1:
        n = t
    print_dptable(V)
    (prob, state) = max((V[n][y], y) for y in states)
    return (prob, path[state])


# Don't study this, it just prints a table of the steps.
def print_dptable(V):
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for y in V[0]:
        s += "%.5s: " % y
        s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
        s += "\n"
    print(s)


def example():
    # states = ('Healthy', 'Fever')
    states = ('Transmit0', 'Transmit1', 'Background0', 'Background1')

    # observations = ('normal', 'cold', 'dizzy')
    observations = '11011000'

    # start_probability = {'Healthy': 0.6, 'Fever': 0.4}
    start_probability = {'Transmit0': 0.5, 'Transmit1': 0.5, 'Background0': 0.0, 'Background1': 0.0}


    # transition_probability = {
    # 'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},
    # 'Fever' : {'Healthy': 0.4, 'Fever': 0.6}
    #    }

    transition_probability = {
        'Transmit0': {'Transmit0': 0.9 * 0.7, 'Transmit1': 0.9 * 0.3, 'Background0': 0.1, 'Background1': 0.0},
        'Transmit1': {'Transmit0': 0.9 * 0.1, 'Transmit1': 0.9 * 0.9, 'Background0': 0.0, 'Background1': 0.1},
        'Background0': {'Transmit0': 0.8 * 0.7, 'Transmit1': 0.8 * 0.3, 'Background0': 0.2, 'Background1': 0.0},
        'Background1': {'Transmit0': 0.8 * 0.1, 'Transmit1': 0.8 * 0.9, 'Background0': 0.0, 'Background1': 0.2}
    }


    # emission_probability = {
    #    'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
    #    'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
    #    }
    emission_probability = {
        'Transmit0': {'0': 0.8, '1': 0.2},
        'Transmit1': {'0': 0.2, '1': 0.8},
        'Background0': {'0': 0.5, '1': 0.5},
        'Background1': {'0': 0.5, '1': 0.5}
    }

    return viterbi(observations,
                   states,
                   start_probability,
                   transition_probability,
                   emission_probability)


print(example())

