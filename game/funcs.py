import style


def get_color_cell(cell_value):
    settings = {
        0: style.CELL_COLOR_0,
        2: style.CELL_COLOR_2,
        4: style.CELL_COLOR_4,
        8: style.CELL_COLOR_8,
        16: style.CELL_COLOR_16,
        32: style.CELL_COLOR_32,
        64: style.CELL_COLOR_64,
        128: style.CELL_COLOR_128,
        256: style.CELL_COLOR_256,
        512: style.CELL_COLOR_512,
        1024: style.CELL_COLOR_1024,
        2048: style.CELL_COLOR_2048,
        "G": style.CELL_COLOR_G,
    }
    return settings.get(cell_value)


def get_color_fontsize_text(cell_value, level):
    match cell_value:
        case 2:
            return style.TEXT_COLOR_2, (
                80 if level == 1 else 60 if level == 2 else 40
            )
        case 4:
            return style.TEXT_COLOR_4, (
                80 if level == 1 else 60 if level == 2 else 40
            )
        case 8:
            return style.TEXT_COLOR_8, (
                80 if level == 1 else 60 if level == 2 else 60
            )
        case 16:
            return style.TEXT_COLOR_16, (
                75 if level == 1 else 60 if level == 2 else 40
            )
        case 32:
            return style.TEXT_COLOR_32, (
                75 if level == 1 else 60 if level == 2 else 40
            )
        case 64:
            return style.TEXT_COLOR_64, (
                75 if level == 1 else 60 if level == 2 else 40
            )
        case 128:
            return style.TEXT_COLOR_128, (
                65 if level == 1 else 45 if level == 2 else 35
            )
        case 256:
            return style.TEXT_COLOR_256, (
                65 if level == 1 else 45 if level == 2 else 35
            )
        case 512:
            return style.TEXT_COLOR_512, (
                65 if level == 1 else 45 if level == 2 else 35
            )
        case 1024:
            return style.TEXT_COLOR_1024, (
                55 if level == 1 else 35 if level == 2 else 25
            )
        case 2048:
            return style.TEXT_COLOR_2048, (
                55 if level == 1 else 35 if level == 2 else 25
            )
        case "G":
            return style.TEXT_COLOR_G, (
                80 if level == 1 else 60 if level == 2 else 60
            )


def generate_settings(level):
    """Функция, возвращающая настройки игры"""
    settings = {
        1: {
            "level": 1,
            "value": 4,
            "cell_size": 90,
            "margin": 8,
        },
        2: {
            "level": 2,
            "value": 6,
            "cell_size": 57.33,
            "margin": 8,
        },
        3: {
            "level": 3,
            "value": 8,
            "cell_size": 41,
            "margin": 8,
        },
    }
    return settings[level]
