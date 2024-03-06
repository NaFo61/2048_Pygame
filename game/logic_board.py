import board

import random


class LogicBoard(board.Board):
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
                        print(self.collected_g)
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
                        print(self.collected_g)
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