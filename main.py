import argparse
import os
import sys
import time
import random
from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich import box

console = Console()


class Grid:
    def __init__(self, render_x, color_x, render_o, color_o):
        self.render_x = render_x
        self.color_x = color_x
        self.render_o = render_o
        self.color_o = color_o
        self.cells = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.dgrid = [0, "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.g_notation = []
        self.turns = 0
        self.err = None

    def reset(self):
        self.cells = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.dgrid = [0, "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.g_notation = []
        self.turns = 0
        self.err = None

    def update(self, choice, player):
        if choice is not None and 0 < choice < 10:
            if not isinstance(self.cells[choice], str):
                if player == "x":
                    self.cells[choice] = player
                    self.dgrid[choice] = (
                        f"[{self.color_x}]{self.render_x}[/{self.color_x}]"
                    )
                else:
                    self.cells[choice] = player
                    self.dgrid[choice] = (
                        f"[{self.color_o}]{self.render_o}[/{self.color_o}]"
                    )
                self.turns += 1
                self.g_notation.append({"player": player, "move": choice})
                self.err = None
                return True
            else:
                self.err = "prc"
        elif choice is None:
            self.err = "inv"
        else:
            self.err = "orng"
        return False

    def check_win(self, p_m, board=None):
        b = board or self.cells
        combos = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9],
            [1, 5, 9],
            [3, 5, 7],
        ]
        for c in combos:
            if b[c[0]] == p_m and b[c[1]] == p_m and b[c[2]] == p_m:
                return True
        return False

    def is_tie(self):
        for i in range(1, 10):
            if not isinstance(self.cells[i], str):
                return False
        return True

    def display(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        console.print("[bold cyan]Tic-Tac-Toe[/bold cyan]")
        console.print("v1.0.0\n")
        table = Table(
            show_header=False,
            show_edge=True,
            box=box.SQUARE,
            show_lines=True,
            width=19,
            expand=False,
        )
        table.add_column(justify="center", vertical="middle", width=5)
        table.add_column(justify="center", vertical="middle", width=5)
        table.add_column(justify="center", vertical="middle", width=5)
        table.add_row(str(self.dgrid[1]), str(self.dgrid[2]), str(self.dgrid[3]))
        table.add_row(str(self.dgrid[4]), str(self.dgrid[5]), str(self.dgrid[6]))
        table.add_row(str(self.dgrid[7]), str(self.dgrid[8]), str(self.dgrid[9]))
        console.print(table)
        notation_text = Text("\nNotation: ", style="dim")
        for v in self.g_notation:
            style = self.color_x if v["player"] == "x" else self.color_o
            notation_text.append(str(v["move"]), style=style)
        console.print(notation_text)
        if self.err:
            msgs = {
                "prc": "[bold red][!] Marker preoccupied",
                "orng": "[bold red][!] Marker out of range",
                "inv": "[bold red][!] Marker invalid",
            }
            console.print(f"\n{msgs.get(self.err)}")


def main():
    parser = argparse.ArgumentParser(
        prog="tic-tac-toe",
        description="Terminal Tic-Tac-Toe. Play 1v1 or vs a bot. Customize symbols and colors via flags or environment variables.",
        epilog="Examples:\n  python project.py --gamemode bot2 --player1-color green\n  PLAYER1_COLOR=green python project.py",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--version", action="version", version="tic-tac-toe 1.0.0")
    parser.add_argument(
        "--player1-symbol",
        metavar="SYMBOL",
        default=None,
        help="Player 1 symbol. (Default: x)",
    )
    parser.add_argument(
        "--player2-symbol",
        metavar="SYMBOL",
        default=None,
        help="Player 2 / AI symbol. (Default: o)",
    )
    parser.add_argument(
        "--player1-color",
        metavar="COLOR",
        default=None,
        help="Color name for Player 1 symbol. (Default: red)",
    )
    parser.add_argument(
        "--player2-color",
        metavar="COLOR",
        default=None,
        help="Color name for Player 2 / AI symbol. (Default: blue)",
    )
    parser.add_argument(
        "--gamemode",
        metavar="MODE",
        choices=["1v1", "bot1", "bot2"],
        default=None,
        help="Game mode: 1v1, bot1, bot2. (Default: 1v1)",
    )
    parser.add_argument(
        "--reversed",
        action="store_true",
        help="Start with Player 2.",
    )
    parser.add_argument(
        "--infinite-games",
        action="store_true",
        help="Automatically start a new game after one finishes.",
    )
    parser.add_argument(
        "--replay",
        metavar="NOTATION",
        help="Replay a game from a notation string.",
    )
    parser.add_argument(
        "--replay-delay",
        type=float,
        default=1.0,
        help="Delay between moves in seconds during replay.",
    )
    args = parser.parse_args()

    r_x = get_config(args.player1_symbol, "PLAYER1_SYMBOL", "x")
    r_o = get_config(args.player2_symbol, "PLAYER2_SYMBOL", "o")
    c_x = get_config(args.player1_color, "PLAYER1_COLOR", "red")
    c_o = get_config(args.player2_color, "PLAYER2_COLOR", "blue")
    gm = get_config(args.gamemode, "GAMEMODE", "1v1")
    rev = get_bool(args.reversed, "REVERSED")
    inf = get_bool(args.infinite_games, "INFINITE_GAMES")

    game_grid = Grid(r_x, c_x, r_o, c_o)

    if args.replay:
        for move_char in args.replay:
            if not move_char.isdigit():
                continue
            game_grid.display()
            time.sleep(args.replay_delay)
            cond_x = (game_grid.turns % 2 == 0) if not rev else (game_grid.turns % 2 != 0)
            game_grid.update(int(move_char), "x" if cond_x else "o")
        game_grid.display()
        if game_grid.check_win("x"):
            console.print(f"\n[{c_x}]{r_x}[/{c_x}] [bold green]wins![/bold green]")
        elif game_grid.check_win("o"):
            console.print(f"\n[{c_o}]{r_o}[/{c_o}] [bold green]wins![/bold green]")
        elif game_grid.is_tie():
            console.print("\n[bold yellow]Tie![/bold yellow]")
        return

    try:
        while True:
            game_grid.display()
            cond_x = (
                (game_grid.turns % 2 == 0)
                if not rev
                else (game_grid.turns % 2 != 0)
            )
            cond_o = not cond_x

            if cond_x:
                console.print(f"\n[?] [{c_x}]{r_x}[/{c_x}], select a marker.")
                try:
                    inp = console.input("[bold yellow]~ [/bold yellow]").strip()
                    choice = int(inp) if (inp and inp.isdigit()) else None
                except EOFError:
                    break
                game_grid.update(choice, "x")
            elif cond_o and gm == "1v1":
                console.print(f"\n[?] [{c_o}]{r_o}[/{c_o}], select a marker.")
                try:
                    inp = console.input("[bold yellow]~ [/bold yellow]").strip()
                    choice = int(inp) if (inp and inp.isdigit()) else None
                except EOFError:
                    break
                game_grid.update(choice, "o")
            elif cond_o:
                move = get_bot_move(
                    game_grid.cells, "simple" if gm == "bot1" else "minmax"
                )
                game_grid.update(move, "o")

            winner_found = False
            win_char = ""
            if game_grid.check_win("x"):
                game_grid.display()
                console.print(f"\n[{c_x}]{r_x}[/{c_x}] [bold green]wins![/bold green]")
                winner_found, win_char = True, "X"
            elif game_grid.check_win("o"):
                game_grid.display()
                console.print(f"\n[{c_o}]{r_o}[/{c_o}] [bold green]wins![/bold green]")
                winner_found, win_char = True, "O"
            elif game_grid.is_tie():
                game_grid.display()
                console.print("\n[bold yellow]Tie![/bold yellow]")
                winner_found, win_char = True, ""

            if winner_found:
                notation = "".join([str(e["move"]) for e in game_grid.g_notation])
                try:
                    with open("games.txt", "a") as f:
                        f.write(f"- {notation}{win_char}\n")
                except:
                    pass
                if not inf:
                    break
                time.sleep(1)
                game_grid.reset()
    except KeyboardInterrupt:
        console.print("\n[bold magenta]Game exited.[/bold magenta]")


def get_config(cli, env, default):
    return cli or os.getenv(env) or default


def get_bool(cli, env):
    return cli or (os.getenv(env, "false").lower() == "true")


def get_bot_move(cells, algo):
    moves = [i for i in range(1, 10) if not isinstance(cells[i], str)]
    if not moves:
        return None
    if algo == "simple":
        return random.choice(moves)

    best_val, best_move = -float("inf"), moves[0]
    for i in moves:
        trial = list(cells)
        trial[i] = "o"
        score = minimax(trial, 0, False)
        if score > best_val:
            best_val, best_move = score, i
    return best_move


def minimax(b, depth, is_max):
    def check(p, board):
        c = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9],
            [1, 5, 9],
            [3, 5, 7],
        ]
        return any(
            board[idx[0]] == p and board[idx[1]] == p and board[idx[2]] == p
            for idx in c
        )

    if check("o", b):
        return 10
    if check("x", b):
        return -10
    moves = [i for i in range(1, 10) if not isinstance(b[i], str)]
    if not moves:
        return 0

    if is_max:
        best = -float("inf")
        for i in moves:
            b2 = list(b)
            b2[i] = "o"
            best = max(best, minimax(b2, depth + 1, False))
        return best
    else:
        best = float("inf")
        for i in moves:
            b2 = list(b)
            b2[i] = "x"
            best = min(best, minimax(b2, depth + 1, True))
        return best


if __name__ == "__main__":
    main()

