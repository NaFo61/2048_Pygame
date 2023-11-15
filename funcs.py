import style

def get_color_cell(cell_value):
    settings = {
        0: style.COLOR_0,
        2: style.COLOR_2,
        4: style.COLOR_4,
        8: style.COLOR_8,
        16: style.COLOR_16,
        32: style.COLOR_32,
        64: style.COLOR_64,
        128: style.COLOR_128,
        256: style.COLOR_256,
        512: style.COLOR_512,
        1024: style.COLOR_1024,
        2048: style.COLOR_2048,
    }
    return settings.get(cell_value)


def get_color_fonsize_text(cell_value, level):
    match cell_value:
        case 2:
            return (121, 112, 99), (80 if level == 1 else 60 if level == 2 else 40)
        case 4:
            return (121, 112, 99), (80 if level == 1 else 60 if level == 2 else 40)
        case 8:
            return (255, 245, 224), (80 if level == 1 else 60 if level == 2 else 40)
        case 16:
            return (255, 245, 224), (75 if level == 1 else 60 if level == 2 else 40)
        case 32:
            return (255, 245, 224), (75 if level == 1 else 60 if level == 2 else 40)
        case 64:
            return (255, 245, 224), (75 if level == 1 else 60 if level == 2 else 40)
        case 128:
            return (255, 245, 224), (65 if level == 1 else 45 if level == 2 else 35)
        case 256:
            return (255, 245, 224), (65 if level == 1 else 45 if level == 2 else 35)
        case 512:
            return (255, 245, 224), (65 if level == 1 else 45 if level == 2 else 35)
        case 1024:
            return (255, 245, 224), (55 if level == 1 else 35 if level == 2 else 25)
        case 2048:
            return (255, 245, 224), (55 if level == 1 else 35 if level == 2 else 25)

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
        }
    }
    return settings[level]