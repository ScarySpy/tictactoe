import os
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
