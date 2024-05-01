import os
import sys
import pathlib

import pygame


def load_image(name, color=None):
    base_dir = pathlib.Path(__file__)
    fullname = base_dir.parent / "data" / "image" / name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color is not None:
        if color == -1:
            color = image.get_at((0, 0))
        image.set_colorkey(color)
    return image