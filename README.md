# TICTACTOE TERM
*This project was developed as my final requirement for Harvard's CS50P (Introduction to Programming with Python).*

#### Description:
TicTacToe Term is a modern CLI implementation of the classic Tic-Tac-Toe game. While simple in spirit, the project aims to be highly customizable and versatile, demonstrating several advanced concepts including Object-Oriented Programming (OOP), recursive algorithms, CLI argument parsing, and the use of external libraries.

# Usage
## Gameplay
Running the script with `python project.py` and no flags will clear the screen and output the following:

```text
Tic-Tac-Toe
v1.0.0
                                                ┌─────┬─────┬─────┐
                                                │  1  │  2  │  3  │
                                                ├─────┼─────┼─────┤
                                                │  4  │  5  │  6  │
                                                ├─────┼─────┼─────┤
                                                │  7  │  8  │  9  │
                                                └─────┴─────┴─────┘
                                                Notation:

[?] x, select a marker.
~
```

The output displays a grid of numbers 1–9, a 'notation' line, and a prompt. Each number represents a position in the grid as outlined above. These numbers are the expected inputs. Each input will mark a position in the grid for the current player if:
- The input is a valid integer;
- The position is within the valid range;
- The position is not already marked.

Otherwise, relevant errors will be shown and the player will be prompted again.

Each move is recorded in the notation line, where each digit represents a specific move. Moves are appended until a winner is found, at which point the last character will indicate the winner of the game (`X` for Player 1, `O` for Player 2). If the final notation ends in a digit, the game is a tie. Examples of valid game notations include: `23456987O`, `1234567X`, and `158234697`.

At the end of the game, the final notation is appended to a `games.txt` file.

> [!NOTE]
> Notations can be a maximum of 9 digits long (one per grid position) and follow an alternating move pattern: `XOXOXOXOX` or `OXOXOXOXO` if reversed. 

> [!TIP]
> Due to the nature of the game, if a match has a winner, the last move will always belong to the winner. Therefore, the preceding move will always be from the loser, following the alternating pattern.

> [!CAUTION]
> Notations from unfinished games will not be saved to `games.txt`.

## Customization
The application is designed to be heavily customizable via command-line arguments and environment variables. Running `python project.py --help` (or using the `-h` flag) provides useful usage information, including:

```
usage: tic-tac-toe [-h] [--version]
                   [--player1-symbol SYMBOL]
                   [--player2-symbol SYMBOL]
                   [--player1-color COLOR]
                   [--player2-color COLOR]
                   [--gamemode MODE]
                   [--reversed]
                   [--infinite-games]
                   [--replay NOTATION]
                   [--replay-delay REPLAY_DELAY]
```

Each flag corresponds to an equivalent environment variable as mapped below:

| Flag | Environment Variable |
| :--- | :--- |
| --player1-symbol | PLAYER1_SYMBOL |
| --player2-symbol | PLAYER2_SYMBOL |
| --player1-color | PLAYER1_COLOR |
| --player2-color | PLAYER2_COLOR |
| --gamemode | GAMEMODE |
| --reversed | REVERSED |
| --infinite-games | INFINITE_GAMES |

Flags take precedence over environment variables, and environment variables take precedence over defaults (Flags → Env Var → Default).

### Symbols
The `player1-symbol` and `player2-symbol` flags (and their corresponding environment variables) change the symbols for Player 1 (default `x`) and Player 2 (default `o`). Both can be set to any string; however, using a single character is recommended.

### Colors
The `player1-color` and `player2-color` flags (and their corresponding environment variables) change the colors for Player 1 (default `red`) and Player 2 (default `blue`). Both can be set to any color supported by [Rich](https://rich.readthedocs.io/en/stable/appendix/colors.html). The color selection affects both the symbols in the grid and the in-game notation.

### Gamemode
The `gamemode` flag and its corresponding environment variable change the gameplay mode. Three modes are supported:
1. `1v1` (default): Two humans playing on the same keyboard.
2. `bot1` (random): A human vs. a bot that makes random moves.
3. `bot2` (minimax): A human vs. a bot that uses a sophisticated algorithm to remain practically unbeatable.

### Order
The `reversed` flag and its corresponding environment variable determine who moves first. Including the `--reversed` flag will activate this setting. For the environment variable `REVERSED`, it must be set to the exact string `"true"` (case-insensitive). If activated, Player 2 (or the bot) will start the game.

### Persistence
The `infinite-games` flag and its corresponding environment variable determine if the script exits after a match finishes. Similar to the previous option, simply including the `--infinite-games` flag will activate it. For the environment variable `INFINITE_GAMES`, it must be set to the exact string `"true"` (case-insensitive). If activated, the board resets after each match and automatically starts a new one.

### Replay
The `replay` and `replay-delay` flags have no corresponding environment variables. The `replay` flag can be used with any notation to replay the game. `replay-delay` determines the delay between each move in seconds, default is `1`. 

---

> [!NOTE]
> To allow for granular control, the script does not prevent you from setting identical symbols or colors for both players. It also does not prevent you from choosing a symbol that is too large for the grid.

> [!NOTE]
> The algorithm for `bot2` (minimax) yields deterministic output, whereas `bot1` is entirely random.

> [!IMPORTANT]
> You can use `Ctrl+C` or `Ctrl+D` to exit the script manually.

> [!CAUTION]
> `replay`, by design, takes any notation, even invalid ones. Use with caution.

> [!TIP]
> Any [Rich style](https://rich.readthedocs.io/en/latest/style.html) (e.g., `"bold underline green"`) can be passed to the color variables.

---

# Design
This project is structured according to the specifications at [https://cs50.harvard.edu/python/project/](https://cs50.harvard.edu/python/project/), consisting of four files:
- `project.py`: The main program file.
- `test_project.py`: A set of tests for the main project (using `pytest`).
- `requirements.txt`: Lists the external library used ([Rich](https://rich.readthedocs.io/en/latest/index.html)).
- `README.md`: This file!

The entirety of the main program is contained within `project.py`, which houses the `Grid` class and the `main()` function. The Rich library is utilized throughout for aesthetics.

The `Grid` class handles state management via a 1D array, input validation, win logic through hardcoded combinations, and rendering.

Two AI opponents are implemented: `simple` (`bot1`), which picks cells randomly, and `minimax` (`bot2`), which employs a recursive search algorithm to simulate every possible future move. By assigning scores to every outcome, `bot2` determines and plays the mathematically optimal move.

The main() function contains the primary game loop. It handles turn-swapping between X (Player 1) and O (Player 2), processes user input, bot moves, or automated game replays, logs each action, and depending on the `--infinite-games` flag, resets the board to start a new match.

