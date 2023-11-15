import random
import sys
import time

import pygame

import style
import funcs


class Board:
    def __init__(self, settings):
        self.left = 50
        self.top = 200

        self.level = settings.get("level")
        self.value = settings.get("value")
        self.cell_size = settings.get("cell_size")
        self.margin = settings.get("margin")
        self.board = [[0 for _ in range(self.value)] for _ in range(self.value)]

    def render(self, screen):
        """Метод, который отображает все поле"""
        self.render_decoration(screen)

        for i in range(self.value):
            for j in range(self.value):
                self.render_cell(screen, i, j)

    def render_decoration(self, screen):
        pygame.draw.rect(screen, style.RECT, (50, 200, 400, 400), 0, 15)

    def render_cell(self, screen, i, j):
        cell_value = self.board[i][j]
        flag = cell_value != 0
        color = funcs.get_color_cell(cell_value)

        rect = pygame.Rect(
            self.left + self.margin * (j + 1) + j * self.cell_size,
            self.top + self.margin * (i + 1) + i * self.cell_size,
            self.cell_size,
            self.cell_size,
        )

        self.draw_cell_rect(screen, rect, color)

        if flag:
            self.render_cell_text(screen, cell_value, i, j)

    def draw_cell_rect(self, screen, rect, color):
        """Рисует ячейку"""
        border_color = pygame.Color(color)

        pygame.draw.rect(screen, border_color, rect, 0, 5)

    def render_cell_text(self, screen, cell_value, i, j):
        """Отображение текста ячейки"""

        color, font_size = funcs.get_color_fonsize_text(cell_value, self.level)
        font = pygame.font.Font(None, font_size)
        text_rendered = font.render(str(cell_value), True, color)

        text_width, text_height = font.size(str(cell_value))

        text_x = self.left + self.margin * (j + 1) + j * self.cell_size + (self.cell_size - text_width) // 2
        text_y = self.top + self.margin * (i + 1) + i * self.cell_size + (self.cell_size - text_height) // 2

        screen.blit(text_rendered, (text_x, text_y))


class Login:
    def check_empty_cells(self):
        return not all(all(line) for line in self.board)

    def fill_random_cells(self):
        number = random.choice((2, 4))
        empty_cells = [(i, j) for i in range(self.value) for j in range(self.value) if self.board[i][j] == 0]
        rd_empty_cell = random.choice(empty_cells)
        row, col = rd_empty_cell
        self.board[row][col] = number

    def move_left(self):
        self.board = [[i for i in line if i] + [0] * line.count(0) for line in self.board]
        for i in range(self.value):
            for j in range(self.value - 1):
                if self.board[i][j] == self.board[i][j + 1] and self.board[i][j + 1] != 0:
                    self.board[i][j] = self.board[i][j] * 2
                    self.board[i].pop(j + 1)
                    self.board[i].append(0)

    def move_right(self):
        self.board = [[0] * line.count(0) + [i for i in line if i] for line in self.board]
        for i in range(self.value):
            for j in range(3, 0, -1):
                if self.board[i][j] == self.board[i][j - 1] and self.board[i][j] != 0:
                    self.board[i][j] *= 2
                    self.board[i].pop(j - 1)
                    self.board[i].insert(0, 0)

    def move_up(self):
        self.board = [list(line) for line in zip(*self.board)]
        self.board = [[i for i in line if i] + [0] * line.count(0) for line in self.board]
        for i in range(self.value):
            for j in range(self.value - 1):
                if self.board[i][j] == self.board[i][j + 1] and self.board[i][j + 1] != 0:
                    self.board[i][j] = self.board[i][j] * 2
                    self.board[i].pop(j + 1)
                    self.board[i].append(0)
        self.board = [list(line) for line in zip(*self.board)]

    def move_down(self):
        self.board = [list(line) for line in zip(*self.board)]
        self.board = [[0] * line.count(0) + [i for i in line if i] for line in self.board]
        for i in range(self.value):
            for j in range(3, 0, -1):
                if self.board[i][j] == self.board[i][j - 1] and self.board[i][j] != 0:
                    self.board[i][j] *= 2
                    self.board[i].pop(j - 1)
                    self.board[i].insert(0, 0)
        self.board = [list(line) for line in zip(*self.board)]


class Game(Board, Login):
    def __init__(self, screen, screen_size, settings):
        width, height = screen_size

        super().__init__(settings)

    def move(self, key):
        is_empty_cells = self.check_empty_cells()
        if is_empty_cells:
            match key:
                case pygame.K_LEFT:
                    self.move_left()
                case pygame.K_RIGHT:
                    self.move_right()
                case pygame.K_UP:
                    self.move_up()
                case pygame.K_DOWN:
                    self.move_down()
            self.fill_random_cells()


def start_page(screen, screen_size):
    width, height = screen_size

    screen.fill(style.BACKGROUND_COLOR)

    # <==== Надпись ====>
    font = pygame.font.SysFont("bahnschrift", 60)
    text = font.render("2048", True, style.S_TITLE)

    text_x = width // 2 - text.get_width() // 2
    text_y = height // 3 - text.get_height() // 2

    screen.blit(text, (text_x, text_y))
    # <==== Надпись ====>

    # <==== Играть ====>
    button_x_1 = width // 2
    button_y_1 = height // 2

    pygame.draw.rect(
        screen,
        style.S_BUTTON,
        (button_x_1 - 100, button_y_1 - 25, 200, 50),
        0,
        15,
    )

    font = pygame.font.SysFont("bahnschrift", 40)
    text = font.render("Играть", True, style.S_BUTTON_TEXT)

    button_x_text_1 = width // 2 - text.get_width() // 2
    button_y_text_1 = height // 2 - text.get_height() // 2

    screen.blit(text, (button_x_text_1, button_y_text_1))
    # <==== Играть ====>

    # <==== Рекорды ====>
    button_x_2 = width // 2
    button_y_2 = height // 2 + 80

    pygame.draw.rect(
        screen,
        style.S_BUTTON,
        (button_x_2 - 100, button_y_2 - 25, 200, 50),
        0,
        15,
    )

    font = pygame.font.SysFont("bahnschrift", 40)
    text = font.render("Рекорды", True, style.S_BUTTON_TEXT)

    button_x_text_2 = width // 2 - text.get_width() // 2
    button_y_text_2 = height // 2 + 80 - text.get_height() // 2

    screen.blit(text, (button_x_text_2, button_y_text_2))
    # <==== Рекорды ====>

    # <==== Правила ====>
    button_x_3 = width // 2
    button_y_3 = height // 2 + 160

    pygame.draw.rect(
        screen,
        style.S_BUTTON,
        (button_x_3 - 100, button_y_3 - 25, 200, 50),
        0,
        15,
    )

    font = pygame.font.SysFont("bahnschrift", 40)
    text = font.render("Правила", True, style.S_BUTTON_TEXT)

    button_x_text_3 = width // 2 - text.get_width() // 2
    button_y_text_3 = height // 2 + 160 - text.get_height() // 2

    screen.blit(text, (button_x_text_3, button_y_text_3))
    # <==== Правила ====>

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                x, y = pos
                if (
                        button_x_1 - 100 < x < button_x_1 + 100
                        and button_y_1 - 25 < y < button_y_1 + 25
                ):
                    return
                elif (
                        button_x_2 - 100 < x < button_x_2 + 100
                        and button_y_2 - 25 < y < button_y_2 + 25
                ):
                    ...
                elif (
                        button_x_3 - 100 < x < button_x_3 + 100
                        and button_y_3 - 25 < y < button_y_3 + 25
                ):
                    rules_page(screen, screen_size)
        pygame.display.flip()


def rules_page(screen, screen_size):
    width, height = screen_size

    screen.fill(style.BACKGROUND_COLOR)

    # <==== Надпись ====>
    font = pygame.font.SysFont("bahnschrift", 60)
    text = font.render("Правила", True, style.S_TITLE)

    text_x = width // 2 - text.get_width() // 2
    text_y = height // 8 - text.get_height() // 2

    screen.blit(text, (text_x, text_y))
    # <==== Надпись ====>

    # <==== Назад ====>
    button_x_1 = width // 2
    button_y_1 = height - height // 8

    pygame.draw.rect(
        screen,
        style.S_BUTTON,
        (button_x_1 - 100, button_y_1 - 25, 200, 50),
        0,
        15,
    )

    font = pygame.font.SysFont("bahnschrift", 40)
    text = font.render("Назад", True, style.S_BUTTON_TEXT)

    button_x_text_1 = width // 2 - text.get_width() // 2
    button_y_text_1 = height - height // 8 - text.get_height() // 2

    screen.blit(text, (button_x_text_1, button_y_text_1))
    # <==== Назад ====>

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                x, y = pos
                if (
                        button_x_1 - 100 < x < button_x_1 + 100
                        and button_y_1 - 25 < y < button_y_1 + 25
                ):
                    start_page(screen, screen_size)
        pygame.display.flip()


def terminate():
    """Выход из приложения"""
    pygame.quit()
    sys.exit()


def main():
    pygame.init()
    SCREEN_SIZE = (500, 650)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("2048")

    LEVEL = 1
    settings = funcs.generate_settings(LEVEL)

    start_page(screen, SCREEN_SIZE)
    print('Прошло дальше')

    board = Game(screen, SCREEN_SIZE, settings)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key in (
                        pygame.K_LEFT,
                        pygame.K_RIGHT,
                        pygame.K_UP,
                        pygame.K_DOWN,
                ):
                    board.move(event.key)
        screen.fill(style.BACKGROUND_COLOR)
        board.render(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
