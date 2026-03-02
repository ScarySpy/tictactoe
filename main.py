import argparse
import time
from source import *


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

if __name__ == "__main__":
    main()
