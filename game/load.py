import os
import sys

import pygame


def load_image(name, color=None):
    fullname = fr"..\{os.path.join("data", name)}"
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color is not None:
        if color == -1:
            color = image.get_at((0, 0))
        image.set_colorkey(color)
    return image