import pathlib
import random
import typing as tp
import pygame
from pygame.locals import *
Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]
class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        pass
        x, y = self.cols, self.rows
        gr = [[0] * x for _ in range(y)]
        if randomize:
            for i in range(y):
                for j in range(x):
                    if random.randint(0, 1):
                        gr[i][j] = 1
        return gr

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        pass
        y, x = cell
        neighbours = []
        coords = (
            (y - 1, x - 1),
            (y - 1, x),
            (y - 1, x + 1),
            (y, x - 1),
            (y, x + 1),
            (y + 1, x - 1),
            (y + 1, x),
            (y + 1, x + 1),
        )
        for i, j in coords:
            if 0 <= j < self.cols and 0 <= i < self.rows:
                neighbours.append(self.curr_generation[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        pass
        x, y = self.cols, self.rows
        gr = self.curr_generation
        gr1 = [[0] * x for _ in range(y)]
        for i in range(y):
            for j in range(x):
                t = GameOfLife.get_neighbours(self, (i, j)).count(1)
                if gr[i][j]:
                    if t == 2 or t == 3:
                        gr1[i][j] = 1
                    else:
                        gr1[i][j] = 0
                else:
                    if t == 3:
                        gr1[i][j] = 1
                    else:
                        gr1[i][j] = 0
        return gr1

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        pass
        self.prev_generation, self.curr_generation = self.curr_generation, self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        pass
        if self.max_generations and self.generations >= self.max_generations:
            return True
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        pass
        if self.prev_generation == self.curr_generation:
            return False
        return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        pass
        with open(filename, "r") as f:
            gr = []
            for line in f.readlines():
                if line.rstrip():
                    gr.append(list(map(int, list(line.rstrip()))))
        game = GameOfLife((len(gr), len(gr[0])), False)
        print(game.curr_generation)
        for i in range(game.rows):
            for j in range(game.cols):
                game.curr_generation[i][j] = gr[i][j]
                game.prev_generation[i][j] = gr[i][j]
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        pass
        with open(filename, "w") as f:
            for row in self.curr_generation:
                f.write("".join(map(str, row)) + "\n")