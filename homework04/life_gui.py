import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed

        self.width = life.cols * cell_size
        self.height = life.rows * cell_size

        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                rect = (
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

                if self.life.curr_generation[y][x] == 1:
                    pygame.draw.rect(self.screen, pygame.Color("green"), rect)
                else:
                    pygame.draw.rect(self.screen, pygame.Color("white"), rect)

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")

        paused = False
        running = True

        while running and self.life.is_changing and not self.life.is_max_generations_exceeded:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                        print(f"Игра {'на паузе' if paused else 'продолжается'}")
                    elif event.key == pygame.K_r:
                        self.life.curr_generation = self.life.create_grid(randomize=True)
                        self.life.generations = 1
                        print("Сетка перезапущена")
                    elif event.key == pygame.K_c:
                        self.life.curr_generation = self.life.create_grid(randomize=False)
                        self.life.generations = 1
                        print("Сетка очищена")
                elif event.type == pygame.MOUSEBUTTONDOWN and paused:
                    x, y = event.pos
                    cell_x = x // self.cell_size
                    cell_y = y // self.cell_size

                    if 0 <= cell_x < self.life.cols and 0 <= cell_y < self.life.rows:
                        if self.life.curr_generation[cell_y][cell_x] == 1:
                            self.life.curr_generation[cell_y][cell_x] = 0
                        else:
                            self.life.curr_generation[cell_y][cell_x] = 1

            self.screen.fill(pygame.Color("white"))

            self.draw_grid()
            self.draw_lines()

            if not paused:
                self.life.step()
                font = pygame.font.SysFont(None, 24)
                gen_text = font.render(f"Поколение: {self.life.generations}", True, pygame.Color("blue"))
                self.screen.blit(gen_text, (10, 10))

            if paused:
                font = pygame.font.SysFont(None, 24)
                text = font.render("ПАУЗА (ПРОБЕЛ: продолжить, R: рестарт, C: очистить)", True, pygame.Color("red"))
                self.screen.blit(text, (10, 10))

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()
