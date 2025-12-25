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
        # Создание сетки заданного размера
        grid = [[0] * self.cols for _ in range(self.rows)]

        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = random.randint(0, 1)

        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Получение списка соседей для клетки
        row, col = cell
        neighbours = []

        # Проверяем все 8 соседних клеток
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue  # Пропускаем саму клетку

                neighbor_row = row + i
                neighbor_col = col + j

                # Проверяем границы
                if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols:
                    neighbours.append(self.curr_generation[neighbor_row][neighbor_col])

        return neighbours

    def get_next_generation(self) -> Grid:
        # Создание сетки для следующего поколения
        next_grid = [[0] * self.cols for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                neighbours = self.get_neighbours((i, j))
                live_neighbours = sum(neighbours)
                current_cell = self.curr_generation[i][j]

                # Правила игры "Жизнь"
                if current_cell == 1:
                    # Живая клетка
                    if live_neighbours == 2 or live_neighbours == 3:
                        next_grid[i][j] = 1  # Остается живой
                    else:
                        next_grid[i][j] = 0  # Умирает
                else:
                    # Мертвая клетка
                    if live_neighbours == 3:
                        next_grid[i][j] = 1  # Оживает
                    else:
                        next_grid[i][j] = 0  # Остается мертвой

        return next_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = [row[:] for row in self.curr_generation]  # Глубокое копирование
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []

        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    row = [int(cell) for cell in line]
                    grid.append(row)

        if not grid:
            raise ValueError("Файл пуст")

        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0

        # Создаем игру с пустой сеткой
        game = GameOfLife((rows, cols), randomize=False)

        # Заполняем сетку данными из файла
        for i in range(rows):
            for j in range(cols):
                game.curr_generation[i][j] = grid[i][j]

        # Инициализируем предыдущее поколение
        game.prev_generation = [row[:] for row in game.curr_generation]

        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, 'w') as f:
            for row in self.curr_generation:
                line = ''.join(str(cell) for cell in row)
                f.write(line + '\n')