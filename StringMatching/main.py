from collections import defaultdict
import math
from pprint import pprint
import sys

__author__ = 'User'

epsilon = 0.0000000001


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


def sum_of_dict(transitions):
    s = 0
    for d in transitions.itervalues():
        for x in d.itervalues():
            s += x
    return s


def baum_welch(observations, states, start_probability, transition_probability, emission_probability):
    (f, forward_likelihood) = forward(observations,
                                      states,
                                      start_probability,
                                      transition_probability,
                                      emission_probability)

    (b, backward_likelihood) = backward(observations,
                                        states,
                                        start_probability,
                                        transition_probability,
                                        emission_probability)

    pprint(f)
    pprint(b)
    exit()

    assert forward_likelihood - backward_likelihood < epsilon
    log_likelihood = math.log(forward_likelihood)

    transitions = defaultdict(create_defaultdict_of_int)
    emissions = defaultdict(create_defaultdict_of_int)
    for i in range(0, len(observations)):
        for state in states:
            if i < len(observations) - 1:
                for to_state in states:
                    transitions[state][to_state] += \
                        math.exp(
                            my_log(transition_probability[state][to_state]) + f[i + 1][state] + b[i + 2][to_state] +
                            my_log(emission_probability[to_state][observations[i + 1]])
                            - log_likelihood)  # observation index starts from 0, f and b start from 1
            emissions[state][observations[i]] += math.exp(f[i + 1][state] + b[i + 1][state] - log_likelihood)
    assert sum_of_dict(emissions) - len(observations) < epsilon
    assert sum_of_dict(transitions) - len(observations) - 1 < epsilon
    return (transitions, emissions, log_likelihood)


def print_dptable(V):
    s = "    " + " ".join(("%7d" % i) for i in V.iterkeys()) + "\n"
    for y in V[1]:
        s += "%.10s: " % y
        s += " ".join("%.7s" % ("%f" % math.exp(v[y])) for v in V.itervalues())
        s += "\n"
    print(s)


states = ('A', 'B', "C", "D")

observations = sys.argv[1]

start_probability = {'A': 0.5, 'B': 0.5, 'C': 0, 'D': 0}

transition_probability = {
    "A": {'A': 1 - float(sys.argv[3]) - float(sys.argv[4]), 'B': float(sys.argv[3]), "C": float(sys.argv[4]), "D": 0},
    "B": {'A': float(sys.argv[6]), 'B': 1 - float(sys.argv[6]) - float(sys.argv[7]), "C": 0, "D": float(sys.argv[7])},
    "C": {'A': float(sys.argv[9]), 'B': float(sys.argv[10]), "C": 1 - float(sys.argv[9]) - float(sys.argv[10]), "D": 0},
    "D": {'A': float(sys.argv[12]), 'B': float(sys.argv[13]), "C": 0,
          "D": 1 - float(sys.argv[12]) - float(sys.argv[13])},
}

emission_probability = {
    "A": {'0': float(sys.argv[5]), '1': 1 - float(sys.argv[5])},
    "B": {'0': float(sys.argv[8]), '1': 1 - float(sys.argv[8])},
    "C": {'0': float(sys.argv[11]), '1': 1 - float(sys.argv[11])},
    "D": {'0': float(sys.argv[14]), '1': 1 - float(sys.argv[14])},
}

if sys.argv[2] == 'Viterbi':
    alg = viterbi
elif sys.argv[2] == 'BaumWelch':
    alg = baum_welch
else:
    print 'Unsupported algorithm'
    exit(1)

old_score = float('-inf')
print observations
print '-------------------------------------------------------------------------------'
print "A->B A->C A->0  : B->A B->D B->0  : C->A C->B C->0  : D->A D->B D->0  :  score"
while True:
    (transitions, emissions, score) = alg(observations,
                                          states,
                                          start_probability,
                                          transition_probability,
                                          emission_probability)

    print "%.2f %.2f %.2f  : %.2f %.2f %.2f  : %.2f %.2f %.2f  : %.2f %.2f %.2f  : %.4f" % \
          (transition_probability['A']['B'], transition_probability['A']['C'], emission_probability['A']['0'],
           transition_probability['B']['A'], transition_probability['B']['D'], emission_probability['B']['0'],
           transition_probability['C']['A'], transition_probability['C']['B'], emission_probability['C']['0'],
           transition_probability['D']['A'], transition_probability['D']['B'], emission_probability['D']['0'], score)

    for state in states:
        # emissions:
        sum = math.fsum(emissions[state].itervalues())
        for c in ['0', '1']:
            emission_probability[state][c] = emissions[state][c] / sum if sum > 0 else 0

        # transmitions:
        sum = math.fsum(transitions[state].itervalues())
        for to_state in states:
            transition_probability[state][to_state] = transitions[state][to_state] / sum if sum > 0 else 0

    if score - old_score < 0.001:
        print 'Done.'
        break
    else:
        old_score = score



