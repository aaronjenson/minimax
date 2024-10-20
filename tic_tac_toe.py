from dataclasses import dataclass
from typing import Self, override

from minimax.base import MinimaxBase


@dataclass
class TicTacToe(MinimaxBase):
    """
    Tic Tac Toe game

    state is stored as a single string representing the board
    each char is a cell, starting at the top going left to right
    """
    board: str = '         '

    @override
    def players(self) -> list[str]:
        return ['x', 'o']

    def turn(self) -> int:
        return len(self.board.replace(' ', ''))

    @override
    def whose_turn(self) -> str:
        return self.players()[self.turn() % 2]

    @override
    def actions(self) -> list[int]:
        return [i for i, c in enumerate(self.board) if c == ' ']

    @override
    def transition(self, action: int) -> list[(Self, float)]:
        return [(TicTacToe(
            self.board[:action] +
            self.whose_turn() +
            self.board[action + 1:]),
            1)]

    def get_chains(self) -> list[str]:
        """
        helper for winner and static_evaluate, gets all possible 3-in-a-rows
        """
        rows = []
        rows.append(self.board[:3])
        rows.append(self.board[3:6])
        rows.append(self.board[6:])
        rows.append(self.board[::3])
        rows.append(self.board[1::3])
        rows.append(self.board[2::3])
        rows.append(self.board[::4])
        rows.append(self.board[2:7:2])
        return rows

    @override
    def winner(self) -> str | None:
        rows = self.get_chains()
        if 'xxx' in rows:
            return 'x'
        if 'ooo' in rows:
            return 'o'
        if ' ' not in self.board:
            return 'tie'
        return None

    @override
    def static_evaluate(self) -> float:
        rows = self.get_chains()
        score = 0
        for row in rows:
            if 'x' in row and 'o' in row:
                continue
            score += row.count('x') ** 2
            score -= row.count('o') ** 2
        return dict(x=score, o=-score)

    def __str__(self) -> str:
        return ('\n' + '-' * (3 * 2 - 1) + '\n').join(
            ['|'.join(self.board[i:i+3]) for i in range(0, 8, 3)])
