def uniform_transition(*states) -> list:
    """
    helper for transition function using a uniform distribution or
    deterministic transitions. Pass the possible states as arguments (unpack a
    list with *your_list before passing it in).
    """
    prob = 1 / len(states)
    return [(s, prob) for s in states]
