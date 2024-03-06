import pygame

import logic_board


class Game(logic_board.LogicBoard):
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