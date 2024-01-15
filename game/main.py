import random
import datetime
import sys

import pygame

import funcs
import load
import style


class Board:
    def __init__(self, screen_size, settings):
        self.left = 50
        self.top = 150

        self.screen_size = screen_size

        self.points = 0

        self.level = settings.get("level")
        self.value = settings.get("value")
        self.cell_size = settings.get("cell_size")
        self.margin = settings.get("margin")
        self.board = [
            [0 for _ in range(self.value)] for _ in range(self.value)
        ]
        self.collected_g = 0

        # Шансы на выпадение чисел
        self.chances = {
            "2": 90,  # Шанс на выпадение числа <2>
            "4": 10,  # Шанс на выпадение числа <4>
            "G": 25,  # Шанс на появление гема
        }

        self.ulta_delete_active = False

    def get_board(self):
        print("x", self.board)

    def check_valid_cell(self, cell):
        i, j = cell
        print(self.board, cell)
        return True if self.board[i][j] != 0 else False

    def check_money_for_ulta(self, need_money):
        collected_g = self.collected_g
        return collected_g >= need_money

    def render_cells(self, screen):
        """Метод, который отображает все поле"""
        for i in range(self.value):
            for j in range(self.value):
                self.render_cell(screen, i, j)

    def render_decoration(self, screen, draw_back_button=False, draw_ulta_red=False):
        width, height = self.screen_size

        # <===== Надпись размер поля =====>
        font = pygame.font.SysFont("spendthrift", 35)
        text = font.render(
            f"{self.value} x {self.value}", True, style.S_BUTTON_TEXT
        )

        button_x_text = width // 2 - text.get_width() // 2
        button_y_text = 130 - text.get_height() // 2

        screen.blit(text, (button_x_text, button_y_text))
        # <===== Надпись размер поля =====>

        # <===== Твой баланс =====>
        pygame.draw.rect(screen, style.S_TABLE_SCORE, (40, 10, 150, 60), 0, 5)
        pygame.draw.rect(
            screen, style.S_TABLE_SCORE_BORDER, (40, 10, 150, 60), 5, 5
        )
        font = pygame.font.SysFont("spendthrift", 30)
        text = font.render("Баланс", True, style.S_TABLE_SCORE_TEXT)

        button_x_text = 115 - text.get_width() // 2
        button_y_text = 28 - text.get_height() // 2

        screen.blit(text, (button_x_text, button_y_text))

        font = pygame.font.SysFont("spendthrift", 30)
        col_text = font.render(
            f"{self.collected_g}", True, style.S_TABLE_SCORE_TEXT_VALUE
        )

        button_x_text = 115 - col_text.get_width() // 2
        button_y_text = 48 - col_text.get_height() // 2

        screen.blit(col_text, (button_x_text, button_y_text))

        # Дальше G
        font = pygame.font.SysFont("spendthrift", 30)
        g_text = font.render("G", True, style.S_TABLE_SCORE_TEXT_VALUE_G)

        button_x_text = (
                115 + col_text.get_width() - len(str(self.collected_g)) * 4
        )
        button_y_text = 48 - g_text.get_height() // 2

        screen.blit(g_text, (button_x_text, button_y_text))
        # <===== Твой баланс =====>

        # <===== Ульта удаление =====>
        if draw_ulta_red:
            ulta_delete = pygame.draw.rect(
                screen, style.S_TABLE_SCORE, (90, 75, 50, 50), 0, 5
            )
            pygame.draw.rect(
                screen, style.S_TABLE_SCORE_BORDER, (90, 75, 50, 50), 5, 5
            )

            image = pygame.transform.scale(
                load.load_image("ulta_delete_click.png", (255, 255, 255)),
                (40, 40),
            )

            screen.blit(image, (ulta_delete.x + 5, ulta_delete.y + 5))
        else:
            ulta_delete = pygame.draw.rect(
                screen, style.S_TABLE_SCORE, (90, 75, 50, 50), 0, 5
            )
            pygame.draw.rect(
                screen, style.S_TABLE_SCORE_BORDER, (90, 75, 50, 50), 5, 5
            )

            image = pygame.transform.scale(
                load.load_image("ulta_delete.png", (255, 255, 255)),
                (40, 40),
            )

            screen.blit(image, (ulta_delete.x + 5, ulta_delete.y + 5))

        # <===== Ульта удаление =====>

        # <===== Твои очки =====>
        pygame.draw.rect(screen, style.S_TABLE_SCORE, (250, 10, 100, 50), 0, 5)
        pygame.draw.rect(
            screen, style.S_TABLE_SCORE_BORDER, (250, 10, 100, 50), 5, 5
        )
        font = pygame.font.SysFont("spendthrift", 20)
        text = font.render("Счет", True, style.S_TABLE_SCORE_TEXT)

        button_x_text = 300 - text.get_width() // 2
        button_y_text = 25 - text.get_height() // 2

        screen.blit(text, (button_x_text, button_y_text))

        font = pygame.font.SysFont("spendthrift", 30)
        text = font.render(
            str(self.points), True, style.S_TABLE_SCORE_TEXT_VALUE
        )

        button_x_text = 300 - text.get_width() // 2
        button_y_text = 40 - text.get_height() // 2

        screen.blit(text, (button_x_text, button_y_text))
        # <===== Твои очки =====>

        # <===== Лучшие очки =====>
        pygame.draw.rect(screen, style.S_TABLE_SCORE, (360, 10, 100, 50), 0, 5)
        pygame.draw.rect(
            screen, style.S_TABLE_SCORE_BORDER, (360, 10, 100, 50), 5, 5
        )
        font = pygame.font.SysFont("spendthrift", 20)
        text = font.render("Лучший", True, style.S_TABLE_SCORE_TEXT)

        button_x_text = 410 - text.get_width() // 2
        button_y_text = 25 - text.get_height() // 2

        screen.blit(text, (button_x_text, button_y_text))
        # <===== Лучшие очки =====>

        # Прямоугольник для клеточек
        pygame.draw.rect(
            screen, style.RECT, (self.left, self.top, 400, 400), 0, 15
        )

        if draw_back_button:
            # <==== Назад ====>
            button_x = width // 2
            button_y = height - height // 12

            pygame.draw.rect(
                screen,
                style.S_BUTTON,
                (button_x - 100, button_y - 25, 200, 50),
                0,
                15,
            )

            font = pygame.font.SysFont("spendthrift", 40)
            text = font.render("Назад", True, style.S_BUTTON_TEXT)

            button_x_text = width // 2 - text.get_width() // 2
            button_y_text = height - height // 12 - text.get_height() // 2

            screen.blit(text, (button_x_text, button_y_text))
            # <==== Назад ====>

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

    @staticmethod
    def draw_cell_rect(screen, rect, color):
        """Рисует ячейку"""
        border_color = pygame.Color(color)

        pygame.draw.rect(screen, border_color, rect, 0, 5)

    def render_cell_text(self, screen, cell_value, i, j):
        """Отображение текста ячейки"""

        color, font_size = funcs.get_color_fontsize_text(
            cell_value, self.level
        )
        font = pygame.font.Font(None, font_size)
        text_rendered = font.render(str(cell_value), True, color)

        text_width, text_height = font.size(str(cell_value))

        text_x = (
                self.left
                + self.margin * (j + 1)
                + j * self.cell_size
                + (self.cell_size - text_width) // 2
        )
        text_y = (
                self.top
                + self.margin * (i + 1)
                + i * self.cell_size
                + (self.cell_size - text_height) // 2
        )

        screen.blit(text_rendered, (text_x, text_y))


class LogicBoard(Board):
    def __init__(self, screen_size, settings):
        super().__init__(screen_size, settings)

    def delete_cell(self, cell):
        if cell is not None:
            i, j = cell
            self.board[i][j] = 0

    def buy_ulta(self, need_money):
        self.collected_g -= need_money

    def check_empty_cells(self):
        return not all(all(line) for line in self.board)

    def find_empty_cells(self):
        empty_cells = [
            (i, j)
            for i in range(self.value)
            for j in range(self.value)
            if self.board[i][j] == 0
        ]
        return empty_cells

    def spawn_number(self):
        chances = list(self.chances.items())[:2]
        lst_with_chances = [
            int(number) for number, chance in chances for _ in range(chance)
        ]
        number = random.choice(lst_with_chances)
        # Поиск пустых ячеек
        empty_cells = self.find_empty_cells()
        # Выбор случайной пустой ячейки для числа
        rd_empty_cell = random.choice(empty_cells)
        row, col = rd_empty_cell
        self.board[row][col] = number

    def spawn_gem(self):
        # Поиск пустых ячеек
        empty_cells = self.find_empty_cells()
        # Выбор случайной пустой ячейки для числа
        rd_empty_cell = random.choice(empty_cells)
        row, col = rd_empty_cell
        self.board[row][col] = "G"

    def fill_random_cells(self):
        # Проверка, что сумма шансов равна 100
        if sum(list(self.chances.values())[:2]) != 100:
            raise ValueError("Error: Chances do not add up to 100")
        self.spawn_number()

        is_spawn_g = random.randint(1, 100) in range(
            1, self.chances.get("G") + 1
        )
        if is_spawn_g:
            self.spawn_gem()

    def move_left(self):
        board = []
        for line in self.board:
            inds_g = [i for i, v in enumerate(line) if v == "G"]
            for ind_g in inds_g:
                if ind_g != len(line) - 1:
                    if [i for i in line[ind_g + 1:] if i and i != "G"]:
                        line[ind_g] = 0
                        self.collected_g += 1
            new_line = [i for i in line if i] + [0] * line.count(0)
            board.append(new_line)
        self.board = board

        for i in range(self.value):
            for j in range(self.value - 1):
                if (
                        self.board[i][j] == self.board[i][j + 1]
                        and self.board[i][j + 1] != 0
                ):
                    if self.board[i][j] != "G":
                        result_of_cell = self.board[i][j] * 2
                        self.board[i][j] = result_of_cell
                        self.board[i].pop(j + 1)
                        self.board[i].append(0)
                        self.points += result_of_cell
                    else:
                        result_of_cell = "G"
                        self.board[i][j] = result_of_cell

    def move_right(self):
        board = []
        for line in self.board:
            inds_g = [i for i, v in enumerate(line) if v == "G"]
            for ind_g in inds_g:
                if True:
                    if [i for i in line[:ind_g] if i and i != "G"]:
                        line[ind_g] = 0
                        self.collected_g += 1
            new_line = [0] * line.count(0) + [i for i in line if i]
            board.append(new_line)
        self.board = board

        for i in range(self.value):
            for j in range(self.value - 1, 0, -1):
                if (
                        self.board[i][j] == self.board[i][j - 1]
                        and self.board[i][j] != 0
                ):
                    if self.board[i][j] != "G":
                        result_of_cell = self.board[i][j] * 2
                        self.board[i][j] = result_of_cell
                        self.board[i].pop(j - 1)
                        self.board[i].insert(0, 0)
                        self.points += result_of_cell
                    else:
                        result_of_cell = "G"
                        self.board[i][j] = result_of_cell

    def move_up(self):
        self.board = [list(line) for line in zip(*self.board)]
        board = []
        for line in self.board:
            inds_g = [i for i, v in enumerate(line) if v == "G"]
            for ind_g in inds_g:
                if ind_g != len(line) - 1:
                    if [i for i in line[ind_g + 1:] if i and i != "G"]:
                        line[ind_g] = 0
                        self.collected_g += 1
            new_line = [i for i in line if i] + [0] * line.count(0)
            board.append(new_line)
        self.board = board
        for i in range(self.value):
            for j in range(self.value - 1):
                if (
                        self.board[i][j] == self.board[i][j + 1]
                        and self.board[i][j + 1] != 0
                ):
                    if self.board[i][j] != "G":
                        result_of_cell = self.board[i][j] * 2
                        self.board[i][j] = result_of_cell
                        self.board[i].pop(j + 1)
                        self.board[i].append(0)
                        self.points += result_of_cell
                    else:
                        result_of_cell = "G"
                        self.board[i][j] = result_of_cell
        self.board = [list(line) for line in zip(*self.board)]

    def move_down(self):
        self.board = [list(line) for line in zip(*self.board)]
        board = []
        for line in self.board:
            inds_g = [i for i, v in enumerate(line) if v == "G"]
            for ind_g in inds_g:
                if True:
                    if [i for i in line[:ind_g] if i and i != "G"]:
                        line[ind_g] = 0
                        self.collected_g += 1
            new_line = [0] * line.count(0) + [i for i in line if i]
            board.append(new_line)
        self.board = board
        for i in range(self.value):
            for j in range(self.value - 1, 0, -1):
                if (
                        self.board[i][j] == self.board[i][j - 1]
                        and self.board[i][j] != 0
                ):
                    if self.board[i][j] != "G":
                        result_of_cell = self.board[i][j] * 2
                        self.board[i][j] = result_of_cell
                        self.board[i].pop(j - 1)
                        self.board[i].insert(0, 0)
                        self.points += result_of_cell
                    else:
                        result_of_cell = "G"
                        self.board[i][j] = result_of_cell
        self.board = [list(line) for line in zip(*self.board)]


class Game(LogicBoard):
    def __init__(self, screen_size, settings):
        super().__init__(screen_size, settings)

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


class App(Game):
    def __init__(self, screen):
        self.screen = screen
        self.screen_size = screen.get_size()
        self.level = 1
        self.settings = funcs.generate_settings(self.level)

        self.move_sounds = [
            pygame.mixer.Sound(f"../data/move_music_{i}.wav")
            for i in range(1, 4)
        ]
        self.click_sound = pygame.mixer.Sound(f"../data/click_music.wav")

        self.start_page(screen)

    def get_cell(self, x, y):
        print(self.settings)
        """Определение ячейки по координатам клика"""
        left = self.settings.get("left")
        top = self.settings.get("top")
        cell_size = self.settings.get("cell_size")
        margin = self.settings.get("margin")
        value = self.settings.get("value")
        if (
                x < left
                or x > left + cell_size * value + margin * (value + 1)
                or y < top
                or y > top + cell_size * value + margin * (value + 1)
        ):
            return None
        return (
            (y - top) // (cell_size + margin),
            (x - left) // (cell_size + margin),
        )

    def get_click(self, x, y):
        """Определение клика"""
        cell = self.get_cell(x, y)
        return cell

    def update_settings(self, level):
        self.level = level
        self.settings = funcs.generate_settings(level)

    def game_page(self, screen):
        super().__init__(self.screen_size, self.settings)

        width, height = self.screen_size

        screen.fill(style.BACKGROUND_COLOR)
        board = Game(self.screen_size, self.settings)
        board.render_decoration(screen, True)

        ulta_red = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key in (
                            pygame.K_LEFT,
                            pygame.K_RIGHT,
                            pygame.K_UP,
                            pygame.K_DOWN,
                    ):
                        random.choice(self.move_sounds).play()
                        board.move(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    x, y = pos
                    if 250 - 100 < x < 250 + 100 and 596 - 25 < y < 596 + 25:
                        self.click_sound.play()
                        self.choice_page(screen)
                    if 90 < x < 140 and 75 < y < 125:
                        self.ulta_delete_active = True
                    elif self.ulta_delete_active:
                        cell = self.get_click(x, y)
                        if board.check_valid_cell(cell):
                            need_money = 10
                            if board.check_money_for_ulta(need_money):
                                board.buy_ulta(10)
                                self.ulta_delete_active = False
                                board.delete_cell(cell)

                if event.type == pygame.MOUSEMOTION:
                    pos = event.pos
                    x, y = pos

                    button_x = width // 2
                    button_y = height - height // 12
                    font = pygame.font.SysFont("spendthrift", 40)
                    text = font.render("Назад", True, style.S_BUTTON_TEXT)

                    button_x_text = width // 2 - text.get_width() // 2
                    button_y_text = (
                            height - height // 12 - text.get_height() // 2
                    )
                    if 150 < x < 350 and 571 < y < 621:
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON_HOVER,
                            (button_x - 100, button_y - 25, 200, 50),
                            0,
                            15,
                        )
                        screen.blit(text, (button_x_text, button_y_text))
                    else:
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON,
                            (button_x - 100, button_y - 25, 200, 50),
                            0,
                            15,
                        )
                        screen.blit(text, (button_x_text, button_y_text))
                    if 90 < x < 140 and 75 < y < 125:
                        ulta_red = True

                        pygame.draw.rect(
                            screen,
                            style.S_TABLE_SCORE,
                            (90, 125, 50, 20),
                            0,
                            5,
                        )
                        font = pygame.font.SysFont("spendthrift", 25)
                        text = font.render(
                            "10", True, style.S_TABLE_SCORE_TEXT
                        )

                        button_x_text = 115 - text.get_width() // 2
                        button_y_text = 135 - text.get_height() // 2

                        screen.blit(text, (button_x_text, button_y_text))
                    else:
                        ulta_red = False

                        pygame.draw.rect(
                            screen,
                            style.BACKGROUND_COLOR,
                            (90, 125, 50, 20),
                            0,
                            5,
                        )

            self.render_decoration(screen, draw_ulta_red=ulta_red)
            board.render_cells(screen)
            pygame.display.flip()

    def start_page(self, screen):
        width, height = self.screen_size

        screen.fill(style.BACKGROUND_COLOR)

        # <==== Играть ====>
        button_x_1 = width // 2
        button_y_1 = height // 2

        play_button_rect = pygame.Rect(
            button_x_1 - 100,
            button_y_1 - 25,
            200,
            50,
        )

        pygame.draw.rect(
            screen,
            style.S_BUTTON,
            play_button_rect,
            0,
            15,
        )

        font = pygame.font.SysFont("spendthrift", 40)
        text_play = font.render("Играть", True, style.S_BUTTON_TEXT)

        button_x_text_1 = width // 2 - text_play.get_width() // 2
        button_y_text_1 = height // 2 - text_play.get_height() // 2

        screen.blit(text_play, (button_x_text_1, button_y_text_1))
        # <==== Играть ====>

        # <==== Рекорды ====>
        button_x_2 = width // 2
        button_y_2 = height // 2 + 80

        records_button_rect = pygame.Rect(
            button_x_2 - 100, button_y_2 - 25, 200, 50
        )

        pygame.draw.rect(
            screen,
            style.S_BUTTON,
            records_button_rect,
            0,
            15,
        )

        font = pygame.font.SysFont("spendthrift", 40)
        text_records = font.render("Рекорды", True, style.S_BUTTON_TEXT)

        button_x_text_2 = width // 2 - text_records.get_width() // 2
        button_y_text_2 = height // 2 + 80 - text_records.get_height() // 2

        screen.blit(text_records, (button_x_text_2, button_y_text_2))
        # <==== Рекорды ====>

        # <==== Правила ====>
        button_x_3 = width // 2
        button_y_3 = height // 2 + 160

        rules_button_rect = pygame.Rect(
            button_x_3 - 100, button_y_3 - 25, 200, 50
        )

        pygame.draw.rect(
            screen,
            style.S_BUTTON,
            rules_button_rect,
            0,
            15,
        )

        font = pygame.font.SysFont("spendthrift", 40)
        text_rules = font.render("Правила", True, style.S_BUTTON_TEXT)

        button_x_text_3 = width // 2 - text_rules.get_width() // 2
        button_y_text_3 = height // 2 + 160 - text_rules.get_height() // 2

        screen.blit(text_rules, (button_x_text_3, button_y_text_3))
        # <==== Правила ====>

        while True:
            color_index = datetime.datetime.now().second % 7
            color = [
                (255, 0, 0),
                (255, 165, 0),
                (255, 255, 0),
                (0, 255, 0),
                (0, 0, 255),
                (75, 0, 130),
                (148, 0, 211),
            ][color_index]

            # Пересоздание текста с новым цветом
            font_title = pygame.font.SysFont("spendthrift", 150)
            text_title = font_title.render("2048", True, color)
            text_x = width // 2 - text_title.get_width() // 2
            text_y = height // 3 - text_title.get_height() // 2

            screen.blit(text_title, (text_x, text_y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    x, y = pos
                    if play_button_rect.collidepoint(x, y):
                        self.click_sound.play()
                        self.choice_page(screen)
                    elif records_button_rect.collidepoint(x, y):
                        self.click_sound.play()
                        # Handle records button click
                        ...
                    elif rules_button_rect.collidepoint(x, y):
                        self.click_sound.play()
                        self.rules_page(screen)
                if event.type == pygame.MOUSEMOTION:
                    pos = event.pos
                    x, y = pos
                    if play_button_rect.collidepoint(x, y):
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON_HOVER,
                            play_button_rect,
                            0,
                            15,
                        )
                        screen.blit(
                            text_play, (button_x_text_1, button_y_text_1)
                        )
                    else:
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON,
                            play_button_rect,
                            0,
                            15,
                        )
                        screen.blit(
                            text_play, (button_x_text_1, button_y_text_1)
                        )

                    if records_button_rect.collidepoint(x, y):
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON_HOVER,
                            records_button_rect,
                            0,
                            15,
                        )
                        screen.blit(
                            text_records, (button_x_text_2, button_y_text_2)
                        )
                    else:
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON,
                            records_button_rect,
                            0,
                            15,
                        )
                        screen.blit(
                            text_records, (button_x_text_2, button_y_text_2)
                        )

                    if rules_button_rect.collidepoint(x, y):
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON_HOVER,
                            rules_button_rect,
                            0,
                            15,
                        )
                        screen.blit(
                            text_rules, (button_x_text_3, button_y_text_3)
                        )
                    else:
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON,
                            rules_button_rect,
                            0,
                            15,
                        )
                        screen.blit(
                            text_rules, (button_x_text_3, button_y_text_3)
                        )

            pygame.display.flip()

    def choice_page(self, screen):
        """
        Change the level.

        Args:
            screen (pygame.Surface): The game screen.

        Returns:
            None
        """
        width, height = self.screen_size

        screen.fill(style.BACKGROUND_COLOR)

        # <==== Надпись ====>
        font_title = pygame.font.SysFont("spendthrift", 60)
        text_title = font_title.render(
            "Выбери размер поля", True, style.S_MAIN_TITLE
        )

        text_x = width // 2 - text_title.get_width() // 2
        text_y = height // 8 - text_title.get_height() // 2

        screen.blit(text_title, (text_x, text_y))
        # <==== Надпись ====>

        font = pygame.font.SysFont("spendthrift", 40)  # Шрифт для кнопок

        # <==== 4 x 4 ====>
        button_x_1 = width // 2
        button_y_1 = height // 3

        button_4_x_4 = pygame.Rect(button_x_1 - 125, button_y_1 - 25, 250, 50)

        pygame.draw.rect(
            screen,
            style.S_BUTTON,
            button_4_x_4,
            0,
            15,
        )

        text_4_x_4 = font.render("4 x 4", True, style.S_BUTTON_TEXT)

        button_x_text_1 = width // 2 - text_4_x_4.get_width() // 2
        button_y_text_1 = height // 3 - text_4_x_4.get_height() // 2

        screen.blit(text_4_x_4, (button_x_text_1, button_y_text_1))
        # <==== 4 x 4 ====>

        # <==== 6 x 6 ====>
        button_x_2 = width // 2
        button_y_2 = height // 3 + 100

        button_6_x_6 = pygame.Rect(button_x_2 - 125, button_y_2 - 25, 250, 50)

        pygame.draw.rect(
            screen,
            style.S_BUTTON,
            button_6_x_6,
            0,
            15,
        )

        text_6_x_6 = font.render("6 x 6", True, style.S_BUTTON_TEXT)

        button_x_text_2 = width // 2 - text_6_x_6.get_width() // 2
        button_y_text_2 = height // 3 + 100 - text_6_x_6.get_height() // 2

        screen.blit(text_6_x_6, (button_x_text_2, button_y_text_2))
        # <==== 6 x 6 ====>

        # <==== Правила ====>
        button_x_3 = width // 2
        button_y_3 = height // 3 + 200

        button_8_x_8 = pygame.Rect(button_x_3 - 125, button_y_3 - 25, 250, 50)

        pygame.draw.rect(
            screen,
            style.S_BUTTON,
            button_8_x_8,
            0,
            15,
        )

        text_8_x_8 = font.render("8 x 8", True, style.S_BUTTON_TEXT)

        button_x_text_3 = width // 2 - text_8_x_8.get_width() // 2
        button_y_text_3 = height // 3 + 200 - text_8_x_8.get_height() // 2

        screen.blit(text_8_x_8, (button_x_text_3, button_y_text_3))
        # <==== 8 x 8 ====>

        # <==== Назад ====>
        button_back_x = width // 2
        button_back_y = height - height // 8

        button_back = pygame.Rect(
            button_back_x - 100, button_back_y - 25, 200, 50
        )

        pygame.draw.rect(
            screen,
            style.S_BUTTON,
            button_back,
            0,
            15,
        )

        text_back = font.render("Назад", True, style.S_BUTTON_TEXT)

        button_back_x_text = width // 2 - text_back.get_width() // 2
        button_back_y_text = height - height // 8 - text_back.get_height() // 2

        screen.blit(text_back, (button_back_x_text, button_back_y_text))
        # <==== Назад ====>

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    x, y = pos
                    if button_4_x_4.collidepoint(x, y):
                        self.click_sound.play()
                        self.update_settings(1)
                        self.game_page(screen)
                    if button_6_x_6.collidepoint(x, y):
                        self.click_sound.play()
                        self.update_settings(2)
                        self.game_page(screen)
                    if button_8_x_8.collidepoint(x, y):
                        self.click_sound.play()
                        self.update_settings(3)
                        self.game_page(screen)
                    if button_back.collidepoint(x, y):
                        self.click_sound.play()
                        self.start_page(screen)
                if event.type == pygame.MOUSEMOTION:
                    pos = event.pos
                    x, y = pos
                    if button_4_x_4.collidepoint(x, y):
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON_HOVER,
                            button_4_x_4,
                            0,
                            15,
                        )
                        screen.blit(
                            text_4_x_4, (button_x_text_1, button_y_text_1)
                        )
                    else:
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON,
                            button_4_x_4,
                            0,
                            15,
                        )
                        screen.blit(
                            text_4_x_4, (button_x_text_1, button_y_text_1)
                        )

                    if button_6_x_6.collidepoint(x, y):
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON_HOVER,
                            button_6_x_6,
                            0,
                            15,
                        )
                        screen.blit(
                            text_6_x_6, (button_x_text_2, button_y_text_2)
                        )
                    else:
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON,
                            button_6_x_6,
                            0,
                            15,
                        )
                        screen.blit(
                            text_6_x_6, (button_x_text_2, button_y_text_2)
                        )

                    if button_8_x_8.collidepoint(x, y):
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON_HOVER,
                            button_8_x_8,
                            0,
                            15,
                        )
                        screen.blit(
                            text_8_x_8, (button_x_text_3, button_y_text_3)
                        )
                    else:
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON,
                            button_8_x_8,
                            0,
                            15,
                        )
                        screen.blit(
                            text_8_x_8, (button_x_text_3, button_y_text_3)
                        )
                    if button_back.collidepoint(x, y):
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON_HOVER,
                            button_back,
                            0,
                            15,
                        )

                        screen.blit(
                            text_back, (button_back_x_text, button_back_y_text)
                        )
                    else:
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON,
                            button_back,
                            0,
                            15,
                        )
                        screen.blit(
                            text_back, (button_back_x_text, button_back_y_text)
                        )

            pygame.display.flip()

    def rules_page(self, screen):
        """
        Display the rules page.

        Args:
            screen (pygame.Surface): The game screen.

        Returns:
            None
        """
        width, height = self.screen_size

        screen.fill(style.BACKGROUND_COLOR)

        # <==== Надпись ====>
        font = pygame.font.SysFont("spendthrift", 60)
        text = font.render("Правила", True, style.S_MAIN_TITLE)

        text_x = width // 2 - text.get_width() // 2
        text_y = height // 8 - text.get_height() // 2

        screen.blit(text, (text_x, text_y))
        # <==== Надпись ====>

        # <==== Правила игры ====>
        rule_font_title = pygame.font.SysFont("spendthrift", 35)
        rule_font_text = pygame.font.SysFont("spendthrift", 15)
        rule_text_1 = rule_font_title.render("Цель игры:", True, style.S_TITLE)
        rule_text_2 = rule_font_text.render(
            "Получить плитку со значением 2048.", True, style.S_TEXT
        )
        rule_text_3 = rule_font_title.render(
            "Управление:", True, style.S_TITLE
        )
        rule_text_4 = rule_font_text.render(
            "Используйте стрелки для перемещения всех плиток.",
            True,
            style.S_TEXT,
        )
        rule_text_5 = rule_font_text.render(
            "Плитки с одинаковыми значениями сливаются вместе.",
            True,
            style.S_TEXT,
        )
        rule_text_6 = rule_font_title.render("Проигрыш:", True, style.S_TITLE)
        rule_text_7 = rule_font_text.render(
            "Когда пустых клеток на поле не останется.", True, style.S_TEXT
        )

        rule_text_y = height // 4

        screen.blit(
            rule_text_1,
            (width // 2 - rule_text_1.get_width() // 2, rule_text_y),
        )
        screen.blit(
            rule_text_2,
            (width // 2 - rule_text_2.get_width() // 2, rule_text_y + 40),
        )
        screen.blit(
            rule_text_3,
            (width // 2 - rule_text_3.get_width() // 2, rule_text_y + 100),
        )
        screen.blit(
            rule_text_4,
            (width // 2 - rule_text_4.get_width() // 2, rule_text_y + 140),
        )
        screen.blit(
            rule_text_5,
            (width // 2 - rule_text_5.get_width() // 2, rule_text_y + 180),
        )
        screen.blit(
            rule_text_6,
            (width // 2 - rule_text_6.get_width() // 2, rule_text_y + 240),
        )
        screen.blit(
            rule_text_7,
            (width // 2 - rule_text_7.get_width() // 2, rule_text_y + 280),
        )
        # <==== Правила игры ====>

        # <==== Назад ====>
        button_x_1 = width // 2
        button_y_1 = height - height // 8

        button_back = pygame.Rect(button_x_1 - 100, button_y_1 - 25, 200, 50)

        pygame.draw.rect(
            screen,
            style.S_BUTTON,
            button_back,
            0,
            15,
        )

        font = pygame.font.SysFont("spendthrift", 40)
        text = font.render("Назад", True, style.S_BUTTON_TEXT)

        button_x_text_1 = width // 2 - text.get_width() // 2
        button_y_text_1 = height - height // 8 - text.get_height() // 2

        screen.blit(text, (button_x_text_1, button_y_text_1))
        # <==== Назад ====>

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    x, y = pos
                    if button_back.collidepoint(x, y):
                        self.click_sound.play()
                        self.start_page(screen)
                if event.type == pygame.MOUSEMOTION:
                    pos = event.pos
                    x, y = pos
                    if button_back.collidepoint(x, y):
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON_HOVER,
                            button_back,
                            0,
                            15,
                        )
                        screen.blit(text, (button_x_text_1, button_y_text_1))
                    else:
                        pygame.draw.rect(
                            screen,
                            style.S_BUTTON,
                            button_back,
                            0,
                            15,
                        )
                        screen.blit(text, (button_x_text_1, button_y_text_1))
            pygame.display.flip()

    @staticmethod
    def terminate():
        """Выход из приложения"""
        pygame.quit()
        sys.exit()


def main():
    pygame.init()
    screen_size = (500, 650)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("2048")

    App(screen)


if __name__ == "__main__":
    main()
