from .base import MinimaxBase


def uniform_transition(*states) -> list:
    """
    helper for transition function using a uniform distribution or
    deterministic transitions. Pass the possible states as arguments (unpack a
    list with *your_list before passing it in).
    """
    prob = 1 / len(states)
    return [(s, prob) for s in states]


def simulate_game(state: MinimaxBase, depth: int = 3):
    turn = 0
    while not state.winner():
        print(f"turn {turn}")
        state = state.move(state.best_action(depth))
        print(state)
        turn += 1
    print(f"winner: {state.winner()}")
