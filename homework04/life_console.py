import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.addch(0, 0, "+")
        screen.addch(0, self.life.cols + 1, "+")
        screen.addch(self.life.rows + 1, 0, "+")
        screen.addch(self.life.rows + 1, self.life.cols + 1, "+")

        for i in range(1, self.life.cols + 1):
            screen.addch(0, i, "-")
            screen.addch(self.life.rows + 1, i, "-")

        for i in range(1, self.life.rows + 1):
            screen.addch(i, 0, "|")
            screen.addch(i, self.life.cols + 1, "|")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addch(i + 1, j + 1, "*")
                else:
                    screen.addch(i + 1, j + 1, " ")

    def run(self) -> None:
        screen = curses.initscr()

        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)

        try:
            running = True
            while running and self.life.is_changing and not self.life.is_max_generations_exceeded:
                screen.clear()

                self.draw_borders(screen)

                self.draw_grid(screen)

                info = f" Поколение: {self.life.generations} (Q для выхода) "
                screen.addstr(self.life.rows + 2, 0, info)

                screen.refresh()

                self.life.step()

                curses.napms(100)

                screen.nodelay(True)
                key = screen.getch()
                if key == ord("q") or key == ord("Q"):
                    running = False

        finally:
            curses.nocbreak()
            screen.keypad(False)
            curses.echo()
            curses.endwin()
