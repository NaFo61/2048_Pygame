import pygame

import app


def main():
    pygame.init()
    screen_size = (500, 650)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("2048")

    app.App(screen)


if __name__ == "__main__":
    main()
