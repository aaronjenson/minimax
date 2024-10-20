# MiniMax

## A generic expecti-minimax implementation

### Setup

```bash
# clone project
# in cloned directory
python3 -m venv venv
```

### Usage

#### Defining a game

MiniMax can play games that fit within these restrictions:

* Turn-based
  * At any given time, it must be only one player's turn to take an action
* Finite action space
  * At each turn, there must be a finite set of actions that the agent can take
* Statically evaluatable
  * At any point in the game, a player must be able to be assigned a numeric
    score that they are trying to maximize
* Predictable (in expectation)
  * Any randomness must follow a known probability distribution

In `minimax/base.py`, there are several abstract methods of the `MinimaxBase`
class that must be implemented by a subclass for MiniMax to play the game.
Documentation is provided via docstring comments on these methods. These
comments also describe the restrictions listed above in greater detail. See 
`tic_tac_toe.py` in the root dir of this project for an example of how to
implement these methods.

A game that implements the necessary methods and inherits from MinimaxBase,
it will have a `best_move` method availble which takes a depth parameter
and return the best move it finds after searching to the given depth.
