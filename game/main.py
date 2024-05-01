import pygame
from sqlalchemy_utils import database_exists, create_database

import app
import db.tables
import db.config
import db.connect


def main():
    pygame.init()
    screen_size = (500, 650)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("2048")

    engine = db.connect.SessionLocal().get_bind()
    if not database_exists(engine.url):
        create_database(engine.url)
        print("База данных успешно создана.")
    db.tables.metadata.create_all(engine)

    app.App(screen)


if __name__ == "__main__":
    main()
