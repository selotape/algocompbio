__author__ = 'ronvis'

# ##CONSTANTS###
DEFAULT_MARGIN = 0.005


def viterbiInference(X, E, T):
    pass


def baumWelchInference(X, E, T, sigma):
    pass


def inferModel(X, method, E, T, sigma=DEFAULT_MARGIN):
    if 'viterbi' == method:
        (E, T) = viterbiInference(X, E, T)
    elif 'baum-welch' == method:
        (E, T) = baumWelchInference(X, E, T, sigma)
    else:
        raise NotImplementedError("This algorithm is yet to be invented.")




