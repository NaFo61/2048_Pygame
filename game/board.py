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
        print(f"self.collected_g: {self.collected_g}")

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