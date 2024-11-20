from enum import Enum
import numpy as np


class SquareType(Enum):
    """
    1. bit taş olup olmadığını
    2. bit taşın 1. oyuncuya ait olup olmadığını
    3. bit taşın dama olup olmadığını gösterir
    """
    O = 0b00000000      # 0 -> taş yok
    w = 0b00000001      # 1 -> taş var, 2. oyuncu(siyah), piyon
    W = 0b00000101      # 5 -> taş var, 2. oyuncu(siyah), dama
    m = 0b00000011      # 3 -> taş var, 1. oyuncu(beyaz), piyon
    M = 0b00000111      # 7 -> tav var, 1. oyuncu(beyaz), dama


STATE = np.array([
            [SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value],
            [SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value],
            [SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value],
            [SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value],
            [SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value],
            [SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value],
            [SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value],
            [SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value],
        ])


def encode_state(state):
    number = 0
    for y in range(8):
        for x in range(8):
            number = number | int(state[y][x])
            number = number << 3
    number = number >> 3
    return number


def decode_state(number):
    arr = np.zeros((8, 8), dtype=int)
    for y in range(7, -1, -1):
        for x in range(7, -1, -1):
            arr[y][x] = 7 & number
            number = number >> 3
    return arr


state_code = encode_state(STATE)
print(f"STATE:\n{STATE}")
print(f"Encoded: {state_code}")
decoded_state = decode_state(state_code)
print(f"Decoded:\n{decoded_state}")

print("sdfgsdfg")

