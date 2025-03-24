from __future__ import annotations
import numpy as np
from typing import List


class MoveNodeDTO:
    def __init__(self, next_state, init_loc: tuple[int, int], next_loc: tuple[int, int]):
        self.next_state = next_state
        self.init_loc = init_loc
        self.next_loc = next_loc
        self.next_nodes: List[MoveNodeDTO] = []


class StateNodeDTO:
    def __init__(self, father: StateNodeDTO | None, state: np.ndarray, value: int, is_leaf: bool = False):
        self.id = None
        self.father = father
        self.state = state
        self.value = value
        self.is_leaf = is_leaf


SCORE_DICT = {
    1: np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-15, -10, -10, -10, -10, -10, -10, -15],
        [-18, -12, -12, -12, -12, -12, -12, -18],
        [-21, -14, -14, -14, -14, -14, -14, -21],
        [-24, -16, -16, -16, -16, -16, -16, -24],
        [-27, -18, -18, -18, -18, -18, -18, -27],
        [-30, -20, -20, -20, -20, -20, -20, -30],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ], dtype=int),
    2: np.array([
        [-64, -48, -48, -48, -48, -48, -48, -64],
        [-48, -32, -32, -32, -32, -32, -32, -48],
        [-48, -32, -32, -32, -32, -32, -32, -48],
        [-48, -32, -32, -32, -32, -32, -32, -48],
        [-48, -32, -32, -32, -32, -32, -32, -48],
        [-48, -32, -32, -32, -32, -32, -32, -48],
        [-48, -32, -32, -32, -32, -32, -32, -48],
        [-64, -48, -48, -48, -48, -48, -48, -64],
    ], dtype=int),
    4: np.array([
        [64, 48, 48, 48, 48, 48, 48, 64],
        [48, 32, 32, 32, 32, 32, 32, 48],
        [48, 32, 32, 32, 32, 32, 32, 48],
        [48, 32, 32, 32, 32, 32, 32, 48],
        [48, 32, 32, 32, 32, 32, 32, 48],
        [48, 32, 32, 32, 32, 32, 32, 48],
        [48, 32, 32, 32, 32, 32, 32, 48],
        [64, 48, 48, 48, 48, 48, 48, 64],
    ], dtype=int),
    5: np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [30, 20, 20, 20, 20, 20, 20, 30],
        [27, 18, 18, 18, 18, 18, 18, 27],
        [24, 16, 16, 16, 16, 16, 16, 24],
        [21, 14, 14, 14, 14, 14, 14, 21],
        [18, 12, 12, 12, 12, 12, 12, 18],
        [15, 10, 10, 10, 10, 10, 10, 15],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ], dtype=int),
}