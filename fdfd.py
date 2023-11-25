import random

chance_2 = 90
chance_4 = 10
if chance_2 + chance_4 != 100:
    raise ValueError("Error chances")
lst_with_chances = [2 * chance_2, 4 * chance_4,]