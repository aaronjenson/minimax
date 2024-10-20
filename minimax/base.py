from abc import ABC, abstractmethod
from collections.abc import Hashable
import random
from typing import Self


class MinimaxBase(ABC):
    """
    The base class for a game that can be played using the minimax algorithm.

    To play a game using minimax, subclass this and implement all the abstract
    methods. Subclasses should be immutable and each method must be
    deterministic.

    When subclassing, include in the subclass all state necessary to represent
    the current state of the game, and nothing more. Methods that implement
    state transitions will return new objects with different state, rather
    than modifying the state of self.

    It is suggested to make subclasses a dataclass. Because of the
    immutability and deterministic methods, many expensive methods can also be
    cached.
    """

    @abstractmethod
    def players(self) -> list[Hashable]:
        """
        get the list of all players of the game

        Players can be represented by any hashable type.

        This list must not change throughout the course of a game. That is,
        any series of valid actions performed with the `transition` method
        should not produce a state where the result of this method has changed.

        If a game has players drop out early, such as elimination type games,
        these players should still be included in this list even after they
        have lost. You can represent their loss by ensuring that their
        evaluation is low and they are not returned by `whose_turn`.

        NOTE: this method is not currently required, but the rules above must
        still be adhered to in other methods.
        """
        pass

    @abstractmethod
    def whose_turn(self) -> Hashable:
        """
        get the player that will take the next action

        This must return one of the players in the list returned by the
        players method.
        """
        pass

    @abstractmethod
    def actions(self) -> list[any]:
        """
        get the allowed actions for the current player at the current state

        Actions can be represented by any type.

        Any action returned by this list should have at least one possible
        next state returned by `transition`.
        """
        pass

    @abstractmethod
    def transition(self, action: any) -> list[(Self, float)]:
        """
        get the probability distribution of next states from the current state
        and given action

        The distribution is returned as a list of tuples, each tuple consisting
        of a state and probability pair. The state should be a new instance of
        the same class. The probabilities of all states returned should add to
        one.

        This method should always return at least one next state, so long as it
        is given an action that was returned by `actions` and the game is not
        over. Actions that have no next states should not be returned by
        `actions`.
        """
        pass

    @abstractmethod
    def winner(self) -> any:
        """
        get the winner if the game has been won, or None

        Returning a falsey value from this function indicates that the game is
        still ongoing. If a truthy value is returned that means the game is
        over and no more actions are possible.

        It is not required to return values consistent with the `players`
        method. Ties or other ends to a game with no winner must still return
        a truthy value, else minimax will attempt to continue to search past
        that state.
        """
        pass

    @abstractmethod
    def static_evaluate(self) -> dict[Hashable, float]:
        """
        get the evaluation for each player at the current state

        The evaluation is returned as a dict mapping players to numerical
        evaluations. A higher evaluation is better for the player.

        Every player returned by `players` must have an evaluation at each
        state. This is still required in two player games, even though these
        evaluations will likely just be opposites.

        This method should not do any searching of potential future states.
        The values returned by this method will be used with minimax to search
        through future states, so any searching here will result in deeper
        searches than intended. This method should just return the best
        reasonable estimation of each player's score given only the current
        state.

        This function will be called many times when searching for the best
        action. It should not take a long time to run.
        """
        pass

    def best_action(self, depth: int = 3) -> any:
        """
        chooses the best action for the current player using minimax

        Returns the best action from the list returned by `actions`, searching
        up to the given depth to determine the optimal move.

        Depth is increased by any player taking an action. So, in a game such
        as tic-tac-toe, a move by x and a move by o is a depth of 2.
        """
        return self.dynamic_evaluate(depth)[1]

    def dynamic_evaluate(self, depth: int = 3) -> (dict[Hashable, float], any):
        """
        uses minimax to evaluate the current state for all players and find the
        best action available for the current player
        """
        if depth == 0 or self.winner():
            return self.static_evaluate(), None

        evals = []

        for action in self.actions():
            expected = dict()
            for state, prob in self.transition(action):
                evaluation = state.dynamic_evaluate(depth - 1)[0]
                expected = {p: e * prob +
                            expected.get(p, 0) for p, e in evaluation.items()}
            evals.append((expected, action))

        return max(evals, key=lambda e: e[0][self.whose_turn()])

    def move(self, action: any) -> Self:
        states, weights = zip(*self.transition(action))
        return random.choices(states, weights=weights)[0]
