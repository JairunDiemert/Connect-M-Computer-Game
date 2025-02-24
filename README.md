# Connect M Game

This is a Python implementation of the Connect M game using adversarial search with alpha-beta pruning. In this game, a human player competes against the computer by dropping disks into a grid. The objective is to connect M disks contiguously either horizontally, vertically, or diagonally.

## Requirements

- Python 3.x

## Files

- `connectM_game.py`: Contains the game logic and implementation of the adversarial search algorithm.
- `main.py`: Contains the command-line interface (CLI) for the game.
- `README.md`: This file.
- `REPORT.md`: Contains the project report outlining the design and implementation details.

## How to Run

Open a terminal and navigate to the project directory. Run the following command:

python3 main.py <N> <M> <H>

Where:
- `<N>` is the board size (number of rows and columns, between 3 and 10).
- `<M>` is the number of contiguous disks required to win (greater than 1 and no higher than N).
- `<H>` is a flag indicating who makes the first move: `1` for human and `0` for computer.

### Example

To start a game on a 5x5 board where 4 contiguous disks are needed to win and the human moves first, run:

python3 main.py 5 4 1

Enjoy the game!
