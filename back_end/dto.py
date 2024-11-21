from enum import Enum
from tkinter import Listbox
from typing import List, Dict
import numpy as np

# dama üzerinde her bir kare için tipler...
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


# taşların tipleri...
class PieceType(Enum):
    w = 0b00000001
    W = 0b00000101
    m = 0b00000011
    M = 0b00000111


class Board:

    def __init__(self):
        self.state = np.array([
            [SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O],
            [SquareType.w, SquareType.w, SquareType.w, SquareType.w, SquareType.w, SquareType.w, SquareType.w, SquareType.w],
            [SquareType.w, SquareType.w, SquareType.w, SquareType.w, SquareType.w, SquareType.w, SquareType.w, SquareType.w],
            [SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O],
            [SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O],
            [SquareType.m, SquareType.m, SquareType.m, SquareType.m, SquareType.m, SquareType.m, SquareType.m, SquareType.m],
            [SquareType.m, SquareType.m, SquareType.m, SquareType.m, SquareType.m, SquareType.m, SquareType.m, SquareType.m],
            [SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O],
        ], dtype=Enum)
        self.indexes_of_selectable_pieces = set()

    def update_state(self, state: np.ndarray):
        if state.shape != (8, 8):
            raise ValueError("[-] State must be an 8x8 np.ndarray.")
        self.state = state