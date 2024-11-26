"""
    Bu modülün amacı: bir durumdan türeyebilecek diğer durumları bulmaktır.

    Algoritması diyagram olarak verilmiştir.

    Sadece beyaz taşlar üzerinden hesaplama yapar, dolayısıyla oyuncu sırasının değişmesi durumunda,
    state in simetrisi referans alınır.
"""

# from back_end.dto import Board, SquareType, MoveNode
from typing import List, Dict
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


# taşların tipleri...
class PieceType(Enum):
    w = 0b00000001
    W = 0b00000101
    m = 0b00000011
    M = 0b00000111


class MoveNode:
    def __init__(self, next_state, init_loc: tuple[int, int], next_loc: tuple[int, int]):
        self.next_state = next_state
        self.init_loc = init_loc
        self.next_loc = next_loc
        self.next_nodes: List[MoveNode] = []


SCORE_DICT = {
    SquareType.O.value: np.zeros((8, 8), dtype=int),
    SquareType.w.value: np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-15, -10, -10, -10, -10, -10, -10, -15],
        [-18, -12, -12, -12, -12, -12, -12, -18],
        [-21, -14, -14, -14, -14, -14, -14, -21],
        [-24, -16, -16, -16, -16, -16, -16, -24],
        [-27, -18, -18, -18, -18, -18, -18, -27],
        [-30, -20, -20, -20, -20, -20, -20, -30],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ], dtype=int),
    SquareType.W.value: np.array([
        [-64, -48, -48, -48, -48, -48, -48, -64],
        [-48, -32, -32, -32, -32, -32, -32, -48],
        [-48, -32, -32, -32, -32, -32, -32, -48],
        [-48, -32, -32, -32, -32, -32, -32, -48],
        [-48, -32, -32, -32, -32, -32, -32, -48],
        [-48, -32, -32, -32, -32, -32, -32, -48],
        [-48, -32, -32, -32, -32, -32, -32, -48],
        [-64, -48, -48, -48, -48, -48, -48, -64],
    ], dtype=int),
    SquareType.m.value: np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [30, 20, 20, 20, 20, 20, 20, 30],
        [27, 18, 18, 18, 18, 18, 18, 27],
        [24, 16, 16, 16, 16, 16, 16, 24],
        [21, 14, 14, 14, 14, 14, 14, 21],
        [18, 12, 12, 12, 12, 12, 12, 18],
        [15, 10, 10, 10, 10, 10, 10, 15],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ], dtype=int),
    SquareType.M.value: np.array([
        [64, 48, 48, 48, 48, 48, 48, 64],
        [48, 32, 32, 32, 32, 32, 32, 48],
        [48, 32, 32, 32, 32, 32, 32, 48],
        [48, 32, 32, 32, 32, 32, 32, 48],
        [48, 32, 32, 32, 32, 32, 32, 48],
        [48, 32, 32, 32, 32, 32, 32, 48],
        [48, 32, 32, 32, 32, 32, 32, 48],
        [64, 48, 48, 48, 48, 48, 48, 64],
    ], dtype=int),
}


class Board:

    def __init__(self, state=None):
        if not state:
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
            # self.state = np.array([
            #     [SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value],
            #     [SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value],
            #     [SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value, SquareType.w.value],
            #     [SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value],
            #     [SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value],
            #     [SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value],
            #     [SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value, SquareType.m.value],
            #     [SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value, SquareType.O.value],
            # ], dtype=int)
        else:
            self.state = state
        self.moves: Dict[tuple[int, int], List[MoveNode]] = {}

    def update_state(self, state: np.ndarray):
        if state.shape != (8, 8):
            raise ValueError("[-] State must be an 8x8 np.ndarray.")
        self.state = state

    def update_moves(self):
        moves: Dict[tuple[int, int]: List[MoveNode]]

        indexes_of_selectable_pieces = self.__select_stones_that_have_to_move()
        if len(indexes_of_selectable_pieces) == 0:
            indexes_of_selectable_pieces = self.__select_stones_that_can_move()
            if len(indexes_of_selectable_pieces) == 0:
                print(self.state)
                raise ValueError(f"[-] player hasn't a move, this is an unexpected state!")
            else:
                """ Normal hamle yapmak gerekiyor """
                self.moves = self.__find_normal_moves(indexes_of_selectable_pieces)
        else:
            """ Taş yemek gerekiyor"""
            self.moves = self.__find_mandatory_moves(indexes_of_selectable_pieces)

    """ Taş yeme zorunluluğu olan taşların konumlarını bulur """
    def __select_stones_that_have_to_move(self) -> List[tuple[int, int]]:
        state = self.state
        indexes_of_selectable_pieces: List[tuple[int, int]] = []
        for y in range(8):
            for x in range(8):
                if state[y][x] == SquareType.m:
                    if (Board.__can_kill_left(state, x, y)
                            or Board.__can_kill_up(state, x, y)
                            or Board.__can_kill_right(state, x, y)):
                        indexes_of_selectable_pieces.append((x, y))
                elif state[y][x] == SquareType.M:
                    if (self.__can_kill_left_long(state, x, y)
                            or self.__can_kill_down_long(state, x, y)
                            or self.__can_kill_right_long(state, x, y)
                            or self.__can_kill_up_long(state, x, y)):
                        indexes_of_selectable_pieces.append((x, y))
        return indexes_of_selectable_pieces

    """ Hamle yapabilen taşların konumlarını bulur """
    def __select_stones_that_can_move(self) -> List[tuple[int, int]]:
        state = self.state
        indexes_of_selectable_pieces: List[tuple[int, int]] = []
        for y in range(8):
            for x in range(8):
                if state[y][x] == SquareType.m or state[y][x] == SquareType.M:
                    if self.__left_is_free(x, y) or self.__up_is_free(x, y) or self.__right_is_free(x, y):
                        indexes_of_selectable_pieces.append((x, y))
                elif state[y][x] == SquareType.M and self.__down_is_free(x, y):
                    indexes_of_selectable_pieces.append((x, y))
        return indexes_of_selectable_pieces

    def __find_normal_moves(self, stones_can_move: List[tuple[int, int]]) -> Dict[tuple[int, int], List[MoveNode]]:
        moves: Dict[tuple[int, int], List[MoveNode]] = {}
        for x, y in stones_can_move:
            moves[(x, y)] = []
            if self.state[y][x] == SquareType.m:
                """ Normal taş hamleleri """
                if self.__left_is_free(x, y):
                    next_state = self.state.copy()
                    next_state[y][x] = SquareType.O
                    next_state[y][x - 1] = SquareType.m
                    move = MoveNode(next_state, (x, y), (x - 1, y))
                    moves[(x, y)].append(move)
                if self.__up_is_free(x, y):
                    next_state = self.state.copy()
                    next_state[y][x] = SquareType.O
                    if y == 1:
                        next_state[0][x] = SquareType.M
                    else:
                        next_state[y - 1][x] = SquareType.m
                    move = MoveNode(next_state, (x, y), (x, y - 1))
                    moves[(x, y)].append(move)
                if self.__right_is_free(x, y):
                    next_state = self.state.copy()
                    next_state[y][x] = SquareType.O
                    next_state[y][x + 1] = SquareType.m
                    move = MoveNode(next_state, (x, y), (x + 1, y))
                    moves[(x, y)].append(move)
            elif self.state[y][x] == SquareType.M:
                """ Dama hamleleri """
                moves[(x, y)] = (self.__left_is_free_long(x, y)
                                 + self.__up_is_free_long(x, y)
                                 + self.__right_is_free_long(x, y)
                                 + self.__down_is_free_long(x, y))
        return moves

    def __find_mandatory_moves(self, stones_can_move: List[tuple[int, int]]) -> Dict[tuple[int, int], List[MoveNode]]:
        moves: Dict[tuple[int, int], List[MoveNode]] = {}
        max_depth = 0
        for x, y in stones_can_move:
            moves[(x, y)] = []
            # listeyi filtrele, en çok taş yenecek hamleler kalsın
            if self.state[y][x] == SquareType.m:
                """ Normal taş hamleleri """
                """ 
                    bir taş, birden fazla taş yiyebilir ve bu farklı hamlelerle yapılabilir, bana lazım olan şey:
                    Birden fazla taş yeme durumu haritalanmalı, ve kaç taş yediği dönmeli
                    Haritalandırma: taşın hareket ettiği konumlar ve oluşan ara geçiş durumları
                    List[Sınıf->attack map/move etc...] 
                """
                new_moves, depth = Board.__get_attack_moves(self.state, x, y)
                if depth == max_depth:
                    moves[(x, y)] = new_moves
                elif depth > max_depth:
                    max_depth = depth
                    moves.clear()
                    moves[(x, y)] = new_moves

            elif self.state[y][x] == SquareType.M:
                """ Dama hamleleri """
                new_moves, depth = Board.__get_attack_moves_long(self.state, x, y)
                if depth == max_depth:
                    moves[(x, y)] = new_moves
                elif depth > max_depth:
                    max_depth = depth
                    moves.clear()
                    moves[(x, y)] = new_moves

        return moves

    @staticmethod
    def __get_attack_moves(state: np.ndarray, x: int, y: int, depth = 0) -> (List[MoveNode], int):
        moves: List[MoveNode] = []
        max_depth = depth
        if Board.__can_kill_left(state, x, y):
            next_state = state.copy()
            next_state[y][x] = SquareType.O
            next_state[y][x - 1] = SquareType.O
            next_state[y][x - 2] = SquareType.m
            node = MoveNode(next_state, (x, y), (x - 2, y))
            node.next_nodes, current_depth = Board.__get_attack_moves(next_state, x - 2, y, depth + 1)
            if current_depth == max_depth:
                moves.append(node)
            elif current_depth > max_depth:
                max_depth = current_depth
                moves.clear()
                moves.append(node)

        if Board.__can_kill_up(state, x, y):
            next_state = state.copy()
            next_state[y][x] = SquareType.O
            next_state[y - 1][x] = SquareType.O
            if y == 2:
                """ Burada taş son kareye ulaşıp dama olur, dolayısıyla zincir hamle sonlanır """
                next_state[0][x] = SquareType.M
                node = MoveNode(next_state, (x, y), (x, 0))
                moves.append(node)
                return moves, depth + 1
            next_state[y - 2][x] = SquareType.m
            node = MoveNode(next_state, (x, y), (x, y - 2))
            node.next_nodes, current_depth = Board.__get_attack_moves(next_state, x, y - 2, depth + 1)
            if current_depth == max_depth:
                moves.append(node)
            elif current_depth > max_depth:
                max_depth = current_depth
                moves.clear()
                moves.append(node)

        if Board.__can_kill_right(state, x, y):
            next_state = state.copy()
            next_state[y][x] = SquareType.O
            next_state[y][x + 1] = SquareType.O
            next_state[y][x + 2] = SquareType.m
            node = MoveNode(next_state, (x, y), (x + 2, y))
            node.next_nodes, current_depth = Board.__get_attack_moves(next_state, x + 2, y, depth + 1)
            if current_depth == max_depth:
                moves.append(node)
            elif current_depth > max_depth:
                max_depth = current_depth
                moves.clear()
                moves.append(node)

        return moves, max_depth

    @staticmethod
    def __get_attack_moves_long(state: np.ndarray, x: int, y: int, depth = 0) -> (List[MoveNode], int):
        moves: List[MoveNode] = []
        max_depth = depth

        """ sola dorğu taş yeme hamelleri """
        enemy_loc = Board.__can_kill_left_long(state, x, y)
        if enemy_loc:
            next_x, next_y = enemy_loc
            while next_x > 0:
                next_x -= 1
                if state[next_y][next_x] != SquareType.O:
                    break
                next_state = state.copy()
                next_state[y][x] = SquareType.O
                next_state[enemy_loc[1]][enemy_loc[0]] = SquareType.O
                next_state[next_y][next_x] = SquareType.M
                node = MoveNode(next_state, (x, y), (next_x, next_y))
                node.next_nodes, current_depth = Board.__get_attack_moves_long(next_state, next_x, next_y, depth + 1)
                if current_depth == max_depth:
                    moves.append(node)
                elif current_depth > max_depth:
                    max_depth = current_depth
                    moves.clear()
                    moves.append(node)

        """ yukarı doğru taş yeme hamleleri """
        enemy_loc = Board.__can_kill_up_long(state, x, y)
        if enemy_loc:
            next_x, next_y = enemy_loc
            while next_y > 0:
                next_y -= 1
                if state[next_y][next_x] != SquareType.O:
                    break
                next_state = state.copy()
                next_state[y][x] = SquareType.O
                next_state[enemy_loc[1]][enemy_loc[0]] = SquareType.O
                next_state[next_y][next_x] = SquareType.M
                node = MoveNode(next_state, (x, y), (next_x, next_y))
                node.next_nodes, current_depth = Board.__get_attack_moves_long(next_state, next_x, next_y, depth + 1)
                if current_depth == max_depth:
                    moves.append(node)
                elif current_depth > max_depth:
                    max_depth = current_depth
                    moves.clear()
                    moves.append(node)

        """ Sağa doğru taş yeme hamleleri """
        enemy_loc = Board.__can_kill_right_long(state, x, y)
        if enemy_loc:
            next_x, next_y = enemy_loc
            while next_x < 7:
                next_x += 1
                if state[next_y][next_x] != SquareType.O:
                    break
                next_state = state.copy()
                next_state[y][x] = SquareType.O
                next_state[enemy_loc[1]][enemy_loc[0]] = SquareType.O
                next_state[next_y][next_x] = SquareType.M
                node = MoveNode(next_state, (x, y), (next_x, next_y))
                node.next_nodes, current_depth = Board.__get_attack_moves_long(next_state, next_x, next_y, depth + 1)
                if current_depth == max_depth:
                    moves.append(node)
                elif current_depth > max_depth:
                    max_depth = current_depth
                    moves.clear()
                    moves.append(node)

        """ Aşağı doğru taş yeme hamleleri """
        enemy_loc = Board.__can_kill_down_long(state, x, y)
        if enemy_loc:
            next_x, next_y = enemy_loc
            while next_y < 7:
                next_y += 1
                if state[next_y][next_x] != SquareType.O:
                    break
                next_state = state.copy()
                next_state[y][x] = SquareType.O
                next_state[enemy_loc[1]][enemy_loc[0]] = SquareType.O
                next_state[next_y][next_x] = SquareType.M
                node = MoveNode(next_state, (x, y), (next_x, next_y))
                node.next_nodes, current_depth = Board.__get_attack_moves_long(next_state, next_x, next_y, depth + 1)
                if current_depth == max_depth:
                    moves.append(node)
                elif current_depth > max_depth:
                    max_depth = current_depth
                    moves.clear()
                    moves.append(node)

        return moves, max_depth

    def __left_is_free(self, x: int, y: int) -> bool:
        if x >= 1 and self.state[y][x - 1] == SquareType.O:
            return True
        return False

    def __up_is_free(self, x: int, y: int) -> bool:
        if y >= 1 and self.state[y - 1][x] == SquareType.O:
            return True
        return False

    def __right_is_free(self, x: int, y: int) -> bool:
        if x <= 6 and self.state[y][x + 1] == SquareType.O:
            return True
        return False

    def __down_is_free(self, x: int, y: int) -> bool:
        if y <= 6 and self.state[y + 1][x] == SquareType.O:
            return True
        return False

    def __left_is_free_long(self, x: int, y: int) -> List[MoveNode]:
        moves: List[MoveNode] = []
        final_x = x
        while self.__left_is_free(x, y):
            next_state = self.state.copy()
            next_state[y][final_x] = SquareType.O
            x -= 1
            next_state[y][x] = SquareType.M
            moves.append(MoveNode(next_state, (final_x, y), (x, y)))
        return moves

    def __up_is_free_long(self, x: int, y: int) -> List[MoveNode]:
        moves: List[MoveNode] = []
        final_y = y
        while self.__up_is_free(x, y):
            next_state = self.state.copy()
            next_state[final_y][x] = SquareType.O
            y -= 1
            next_state[y][x] = SquareType.M
            moves.append(MoveNode(next_state, (x, final_y), (x, y)))
        return moves

    def __right_is_free_long(self, x: int, y: int) -> List[MoveNode]:
        moves: List[MoveNode] = []
        final_x = x
        while self.__right_is_free(x, y):
            next_state = self.state.copy()
            next_state[y][final_x] = SquareType.O
            x += 1
            next_state[y][x] = SquareType.M
            moves.append(MoveNode(next_state, (final_x, y), (x, y)))
        return moves

    def __down_is_free_long(self, x: int, y: int) -> List[MoveNode]:
        moves: List[MoveNode] = []
        final_y = y
        while self.__down_is_free(x, y):
            next_state = self.state.copy()
            next_state[final_y][x] = SquareType.O
            y += 1
            next_state[y][x] = SquareType.M
            moves.append(MoveNode(next_state, (x, final_y), (x, y)))
        return moves

    @staticmethod
    def __can_kill_left(state, x: int, y: int) -> bool:
        """ Seçilen taşın solunda düşman taş var ve onun solu boş """
        """ 0b....01 2. oyuncunun taşı demek... """
        if x >= 2 and state[y][x - 2] == SquareType.O and state[y][x - 1].value | 0b100 == 0b101:
            return True
        return False

    @staticmethod
    def __can_kill_up(state, x: int, y: int) -> bool:
        """ Seçilen taşın yukarısında düşman taş var ve onun yukarısı boş """
        if y >= 2 and state[y - 2][x] == SquareType.O and state[y - 1][x].value | 0b100 == 0b101:
            return True
        return False

    @staticmethod
    def __can_kill_right(state, x: int, y: int):
        """ Seçilen taşın sağında düşman taş var ve onun sağı boş """
        if x <= 5 and state[y][x + 2] == SquareType.O and state[y][x + 1].value | 0b100 == 0b101:
            return True
        return False

    @staticmethod
    def __can_kill_left_long(state, x: int, y: int) -> tuple[int, int] | None:
        """ İlk soldan başlayarak sondan bir önceki sol kadar taş yeme durumunu kontrol eder """
        if x >= 2:
            if state[y][x - 2] == SquareType.O and state[y][x - 1].value | 0b100 == 0b101:
                return x - 1, y
            if state[y][x - 1] == SquareType.O:
                """ Solda taş yoksa bir soldan tekrar aynı süreç başlar """
                return Board.__can_kill_left_long(state, x - 1, y)

    @staticmethod
    def __can_kill_up_long(state, x: int, y: int) -> tuple[int, int] | None:
        """ İlk aşağıdan başlayarak sondan bir önceki aşağıya kadar taş yeme durumunu kontrol eder """
        if y >= 2:
            if state[y - 2][x] == SquareType.O and state[y - 1][x].value | 0b100 == 0b101:
                return x, y - 1
            if state[y - 1][x] == SquareType.O:
                """ Aşağıda taş yoksa bir aşağıdan tekrar aynı süreç başlar """
                return Board.__can_kill_up_long(state, x, y - 1)

    @staticmethod
    def __can_kill_right_long(state, x: int, y: int) -> tuple[int, int] | None:
        """ İlk sağdan başlayarak sondan bir önceki sağa kadar taş yeme durumunu kontrol eder """
        if x <= 5:
            if state[y][x + 2] == SquareType.O and state[y][x + 1].value | 0b100 == 0b101:
                return x + 1, y
            if state[y][x + 1] == SquareType.O:
                """ Sağda taş yoksa bir sağdan tekrar aynı süreç başlar """
                return Board.__can_kill_right_long(state, x + 1, y)

    @staticmethod
    def __can_kill_down_long(state, x: int, y: int) -> tuple[int, int] | None:
        """ İlk yukarıdan başlayarak sondan bir önceki yukarıya kadar taş yeme durumunu kontrol eder """
        if y <= 5:
            if state[y + 2][x] == SquareType.O and state[y + 1][x].value | 0b100 == 0b101:
                return x, y + 1
            if state[y + 1][x] == SquareType.O:
                """ Yukarıda taş yoksa bir yukarıdan tekrar aynı süreç başlar """
                return Board.__can_kill_down_long(state, x, y + 1)

    def reverse_state(self):
        self.state = np.flip(self.state)


""" Board dan hamleleri al, durumları türet, hamleleri puanla, """
class StateManager:

    @staticmethod
    def get_final_states(board: Board) -> List[tuple[int, np.ndarray]]:
        final_states = []
        for root_nodes in board.moves.values():
            for root_node in root_nodes:
                final_states += StateManager.__get_last_states(root_node)
        """ Stateleri puanlandır """
        final_states: List[tuple[int, np.ndarray]] = StateManager.__calculate_scores_of_states(final_states)
        final_states = sorted(final_states, key=lambda x: x[0])
        return final_states

    @staticmethod
    def __get_last_states(move: MoveNode):
        state_list = []
        if len(move.next_nodes) == 0:
            state_list.append(move.next_state)
            return state_list
        for node in move.next_nodes:
            state_list += StateManager.__get_last_states(node)
        return state_list

    @staticmethod
    def __calculate_scores_of_states(final_states: List[np.ndarray]) -> List[tuple[int, np.ndarray]]:
        result: List[tuple[int, np.ndarray]] = []
        convert_to_int = np.vectorize(lambda x: x.value)
        for final_state in final_states:
            final_state_int = convert_to_int(final_state)
            score_state = np.zeros((8, 8), dtype=int)
            for y in range(8):
                for x in range(8):
                    score_state[y][x] = SCORE_DICT[final_state_int[y][x]][y][x]
            result.append((score_state.sum(), final_state))
        return result




