"""
    Bu modülün amacı: bir durumdan türeyebilecek diğer durumları bulmaktır.

    Algoritması diyagram olarak verilmiştir.

    Sadece beyaz taşlar üzerinden hesaplama yapar, dolayısıyla oyuncu sırasının değişmesi durumunda,
    state in simetrisi referans alınır.
"""
from __future__ import annotations

# from back_end.dto import Board, SquareType, MoveNode
from typing import List, Dict, Tuple
from enum import Enum
import numpy as np


class MoveNode:
    def __init__(self, next_state, init_loc: tuple[int, int], next_loc: tuple[int, int]):
        self.next_state = next_state
        self.init_loc = init_loc
        self.next_loc = next_loc
        self.next_nodes: List[MoveNode] = []


class StateNode:
    def __init__(self, value: int, state: np.ndarray, father: StateNode | None = None):
        self.value = value
        self.state = state
        self.father = father


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


class Board:
    def __init__(self, state: np.array, turn_on_first_player: bool):
        self.turn_on_first_player = turn_on_first_player
        self.state = state
        self.moves: Dict[tuple[int, int], List[MoveNode]] = {}
        if turn_on_first_player:
            self.is_enemy = lambda n: n < 3
            self.super_piece = 4
            self.piece = 5
        else:
            self.is_enemy = lambda n: n > 3
            self.super_piece = 2
            self.piece = 1

    def update_state(self, state: np.ndarray):
        self.state = state

    def update_moves(self):
        moves: Dict[tuple[int, int]: List[MoveNode]]
        indexes_of_pieces: np.ndarray
        indexes_of_super_pieces: np.ndarray
        if self.turn_on_first_player:
            indexes_of_pieces = np.argwhere(self.state == 5)
            indexes_of_super_pieces = np.argwhere(self.state == 4)
        else:
            indexes_of_pieces = np.argwhere(self.state == 1)
            indexes_of_super_pieces = np.argwhere(self.state == 2)
        # TODO burada oyuncunun taşı kalıp kalmadığını kontrol edebilirsin
        indexes_of_pieces_that_have_to_move, indexes_of_super_pieces_that_have_to_move = (
            self.__select_stones_that_have_to_move(indexes_of_pieces, indexes_of_super_pieces))
        if len(indexes_of_pieces_that_have_to_move) == 0 and len(indexes_of_super_pieces_that_have_to_move) == 0:
            self.moves = self.__find_normal_moves(indexes_of_pieces, indexes_of_super_pieces)
        else:
            """ Taş yemek gerekiyor"""
            self.moves = self.__find_mandatory_moves(indexes_of_pieces_that_have_to_move, indexes_of_super_pieces_that_have_to_move)

    def load_next_state(self, state):
        self.state = state
        self.turn_on_first_player = not self.turn_on_first_player
        if self.turn_on_first_player:
            self.is_enemy = lambda n: n < 3
            self.super_piece = 4
            self.piece = 5
        else:
            self.is_enemy = lambda n: n > 3
            self.super_piece = 2
            self.piece = 1

    """ Taş yeme zorunluluğu olan taşların konumlarını bulur """
    def __select_stones_that_have_to_move(self, indexes_of_pieces: np.ndarray, indexes_of_super_pieces: np.ndarray)\
            -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        state = self.state
        indexes_of_pieces_that_have_to_move: List[tuple[int, int]] = []
        for y, x in indexes_of_pieces:
            if self.turn_on_first_player:
                # state[y][x] = 5 dir
                if (self.__can_kill_left(state, x, y)
                        or self.__can_kill_up(state, x, y)
                        or self.__can_kill_right(state, x, y)):
                    indexes_of_pieces_that_have_to_move.append((x, y))
            else:
                # state[y][x] = 1 dir
                if (self.__can_kill_left(state, x, y)
                        or self.__can_kill_down(state, x, y)
                        or self.__can_kill_right(state, x, y)):
                    indexes_of_pieces_that_have_to_move.append((x, y))
        indexes_of_super_pieces_that_have_to_move: List[tuple[int, int]] = []
        for y, x in indexes_of_super_pieces:
            # state[y][x] = 2 ya da 4 tür
            if (self.__can_kill_left_long(state, x, y)
                    or self.__can_kill_down_long(state, x, y)
                    or self.__can_kill_right_long(state, x, y)
                    or self.__can_kill_up_long(state, x, y)):
                indexes_of_super_pieces_that_have_to_move.append((x, y))
        return indexes_of_pieces_that_have_to_move, indexes_of_super_pieces_that_have_to_move

    def __find_normal_moves(self, indexes_of_pieces: np.ndarray, indexes_of_super_pieces: np.ndarray)\
            -> Dict[tuple[int, int], List[MoveNode]]:
        moves: Dict[tuple[int, int], List[MoveNode]] = {}
        """ Normal taşın normal hamleleri, """
        for y, x in indexes_of_pieces:
            x, y = int(x), int(y)
            moves[(x, y)] = []
            if self.__left_is_free(x, y):
                move = self.__get_normal_move((x, y), (x - 1, y))
                moves[(x, y)].append(move)
            if self.__right_is_free(x, y):
                move = self.__get_normal_move((x, y), (x + 1, y))
                moves[(x, y)].append(move)
            if self.turn_on_first_player and self.__up_is_free(x, y):
                next_state = self.state.copy()
                next_state[y][x] = 3
                if y == 1:
                    next_state[0][x] = 4
                else:
                    next_state[y - 1][x] = 5
                move = MoveNode(next_state, (x, y), (x, y - 1))
                moves[(x, y)].append(move)
            if not self.turn_on_first_player and self.__down_is_free(x, y):
                next_state = self.state.copy()
                next_state[y][x] = 3
                if y == 6:
                    next_state[7][x] = 2
                else:
                    next_state[y + 1][x] = 1
                move = MoveNode(next_state, (x, y), (x, y + 1))
                moves[(x, y)].append(move)
        """ Dama taşının normal hamleleri """
        for y, x in indexes_of_super_pieces:
            x, y = int(x), int(y)
            moves[(x, y)] = []
            moves[(x, y)] = (self.__left_is_free_long(x, y)
                             + self.__up_is_free_long(x, y)
                             + self.__right_is_free_long(x, y)
                             + self.__down_is_free_long(x, y))

        return moves

    def __get_normal_move(self, init_loc: tuple[int, int], next_loc: tuple[int, int]) -> MoveNode:
        next_state = self.state.copy()
        next_state[next_loc[1]][next_loc[0]] = next_state[init_loc[1]][init_loc[0]]
        next_state[init_loc[1]][init_loc[0]] = 3
        return MoveNode(next_state, init_loc, next_loc)

    def __find_mandatory_moves(self,
                               indexes_of_pieces_that_have_to_move: List[tuple[int, int]],
                               indexes_of_super_pieces_that_have_to_move: List[tuple[int, int]]) \
            -> Dict[tuple[int, int], List[MoveNode]]:

        moves: Dict[tuple[int, int], List[MoveNode]] = {}
        max_depth = 0

        for x, y in indexes_of_pieces_that_have_to_move:
            """ Normal taş hamleleri """
            # moves[(x, y)] = []
            """ 
                bir taş, birden fazla taş yiyebilir ve bu farklı hamlelerle yapılabilir, bana lazım olan şey:
                Birden fazla taş yeme durumu haritalanmalı, ve kaç taş yediği dönmeli
                Haritalandırma: taşın hareket ettiği konumlar ve oluşan ara geçiş durumları
                List[Sınıf->attack map/move etc...] 
            """
            new_moves, depth = self.__get_attack_moves(self.state, x, y)
            if depth == max_depth:
                moves[(x, y)] = new_moves
            elif depth > max_depth:
                max_depth = depth
                moves.clear()
                moves[(x, y)] = new_moves

        for x, y in indexes_of_super_pieces_that_have_to_move:
            """ Dama hamleleri """
            # moves[(x, y)] = []
            new_moves, depth = self.__get_attack_moves_long(self.state, x, y)
            if depth == max_depth:
                moves[(x, y)] = new_moves
            elif depth > max_depth:
                max_depth = depth
                moves.clear()
                moves[(x, y)] = new_moves

        return moves

    def __get_attack_moves(self, state: np.ndarray, x: int, y: int, depth = 0) -> (List[MoveNode], int):
        moves: List[MoveNode] = []
        max_depth = depth
        if self.__can_kill_left(state, x, y):
            next_state = state.copy()
            next_state[y][x] = 3
            next_state[y][x - 1] = 3
            next_state[y][x - 2] = self.piece
            node = MoveNode(next_state, (x, y), (x - 2, y))
            node.next_nodes, current_depth = self.__get_attack_moves(next_state, x - 2, y, depth + 1)
            if current_depth == max_depth:
                moves.append(node)
            elif current_depth > max_depth:
                max_depth = current_depth
                moves.clear()
                moves.append(node)

        if self.turn_on_first_player and self.__can_kill_up(state, x, y):
            next_state = state.copy()
            next_state[y][x] = 3
            next_state[y - 1][x] = 3
            if y == 2:
                """ Normal taş en yukarıya ulaştığında dama olur """
                next_state[0][x] = self.super_piece
                node = MoveNode(next_state, (x, y), (x, 0))
                moves.append(node)
                return moves, depth + 1
            next_state[y - 2][x] = self.piece
            node = MoveNode(next_state, (x, y), (x, y - 2))
            node.next_nodes, current_depth = self.__get_attack_moves(next_state, x, y - 2, depth + 1)
            if current_depth == max_depth:
                moves.append(node)
            elif current_depth > max_depth:
                max_depth = current_depth
                moves.clear()
                moves.append(node)

        if self.__can_kill_right(state, x, y):
            next_state = state.copy()
            next_state[y][x] = 3
            next_state[y][x + 1] = 3
            next_state[y][x + 2] = self.piece
            node = MoveNode(next_state, (x, y), (x + 2, y))
            node.next_nodes, current_depth = self.__get_attack_moves(next_state, x + 2, y, depth + 1)
            if current_depth == max_depth:
                moves.append(node)
            elif current_depth > max_depth:
                max_depth = current_depth
                moves.clear()
                moves.append(node)

        if not self.turn_on_first_player and self.__can_kill_down(state, x, y):
            next_state = state.copy()
            next_state[y][x] = 3
            next_state[y + 1][x] = 3
            if y == 5:
                """ Normal taş en aşağıya ulaştığında dama olur """
                next_state[7][x] = self.super_piece
                node = MoveNode(next_state, (x, y), (x, 7))
                moves.append(node)
                return moves, depth + 1
            next_state[y + 2][x] = self.piece
            node = MoveNode(next_state, (x, y), (x, y + 2))
            node.next_nodes, current_depth = self.__get_attack_moves(next_state, x, y + 2, depth + 1)
            if current_depth == max_depth:
                moves.append(node)
            elif current_depth > max_depth:
                max_depth = current_depth
                moves.clear()
                moves.append(node)

        return moves, max_depth

    def __get_attack_moves_long(self, state: np.ndarray, x: int, y: int, depth = 0) -> (List[MoveNode], int):
        moves: List[MoveNode] = []
        max_depth = depth

        """ sola dorğu taş yeme hamelleri """
        enemy_loc = self.__can_kill_left_long(state, x, y)
        if enemy_loc:
            next_x, next_y = enemy_loc
            while next_x > 0:
                next_x -= 1
                if state[next_y][next_x] != 3:
                    break
                next_state = state.copy()
                next_state[y][x] = 3
                next_state[enemy_loc[1]][enemy_loc[0]] = 3
                next_state[next_y][next_x] = self.super_piece
                node = MoveNode(next_state, (x, y), (next_x, next_y))
                node.next_nodes, current_depth = self.__get_attack_moves_long(next_state, next_x, next_y, depth + 1)
                if current_depth == max_depth:
                    moves.append(node)
                elif current_depth > max_depth:
                    max_depth = current_depth
                    moves.clear()
                    moves.append(node)

        """ yukarı doğru taş yeme hamleleri """
        enemy_loc = self.__can_kill_up_long(state, x, y)
        if enemy_loc:
            next_x, next_y = enemy_loc
            while next_y > 0:
                next_y -= 1
                if state[next_y][next_x] != 3:
                    break
                next_state = state.copy()
                next_state[y][x] = 3
                next_state[enemy_loc[1]][enemy_loc[0]] = 3
                next_state[next_y][next_x] = self.super_piece
                node = MoveNode(next_state, (x, y), (next_x, next_y))
                node.next_nodes, current_depth = self.__get_attack_moves_long(next_state, next_x, next_y, depth + 1)
                if current_depth == max_depth:
                    moves.append(node)
                elif current_depth > max_depth:
                    max_depth = current_depth
                    moves.clear()
                    moves.append(node)

        """ Sağa doğru taş yeme hamleleri """
        enemy_loc = self.__can_kill_right_long(state, x, y)
        if enemy_loc:
            next_x, next_y = enemy_loc
            while next_x < 7:
                next_x += 1
                if state[next_y][next_x] != 3:
                    break
                next_state = state.copy()
                next_state[y][x] = 3
                next_state[enemy_loc[1]][enemy_loc[0]] = 3
                next_state[next_y][next_x] = self.super_piece
                node = MoveNode(next_state, (x, y), (next_x, next_y))
                node.next_nodes, current_depth = self.__get_attack_moves_long(next_state, next_x, next_y, depth + 1)
                if current_depth == max_depth:
                    moves.append(node)
                elif current_depth > max_depth:
                    max_depth = current_depth
                    moves.clear()
                    moves.append(node)

        """ Aşağı doğru taş yeme hamleleri """
        enemy_loc = self.__can_kill_down_long(state, x, y)
        if enemy_loc:
            next_x, next_y = enemy_loc
            while next_y < 7:
                next_y += 1
                if state[next_y][next_x] != 3:
                    break
                next_state = state.copy()
                next_state[y][x] = 3
                next_state[enemy_loc[1]][enemy_loc[0]] = 3
                next_state[next_y][next_x] = self.super_piece
                node = MoveNode(next_state, (x, y), (next_x, next_y))
                node.next_nodes, current_depth = self.__get_attack_moves_long(next_state, next_x, next_y, depth + 1)
                if current_depth == max_depth:
                    moves.append(node)
                elif current_depth > max_depth:
                    max_depth = current_depth
                    moves.clear()
                    moves.append(node)

        return moves, max_depth

    def __left_is_free(self, x: int, y: int) -> bool:
        if x >= 1 and self.state[y][x - 1] == 3:
            return True
        return False

    def __up_is_free(self, x: int, y: int) -> bool:
        if y >= 1 and self.state[y - 1][x] == 3:
            return True
        return False

    def __right_is_free(self, x: int, y: int) -> bool:
        if x <= 6 and self.state[y][x + 1] == 3:
            return True
        return False

    def __down_is_free(self, x: int, y: int) -> bool:
        if y <= 6 and self.state[y + 1][x] == 3:
            return True
        return False

    def __left_is_free_long(self, x: int, y: int) -> List[MoveNode]:
        moves: List[MoveNode] = []
        next_x = x
        while self.__left_is_free(next_x, y):
            next_x -= 1
            move = self.__is_free_long((x, y), (next_x, y))
            moves.append(move)
        return moves

    def __up_is_free_long(self, x: int, y: int) -> List[MoveNode]:
        moves: List[MoveNode] = []
        next_y = y
        while self.__up_is_free(x, next_y):
            next_y -= 1
            move = self.__is_free_long((x, y), (x, next_y))
            moves.append(move)
        return moves

    def __right_is_free_long(self, x: int, y: int) -> List[MoveNode]:
        moves: List[MoveNode] = []
        next_x = x
        while self.__right_is_free(next_x, y):
            next_x += 1
            move = self.__is_free_long((x, y), (next_x, y))
            moves.append(move)
        return moves

    def __down_is_free_long(self, x: int, y: int) -> List[MoveNode]:
        moves: List[MoveNode] = []
        next_y = y
        while self.__down_is_free(x, next_y):
            next_y += 1
            move = self.__is_free_long((x, y), (x, next_y))
            moves.append(move)
        return moves

    def __is_free_long(self, init_loc:  tuple[int, int], next_loc:  tuple[int, int]) -> MoveNode:
        next_state = self.state.copy()
        next_state[init_loc[1]][init_loc[0]] = 3
        next_state[next_loc[1]][next_loc[0]] = self.super_piece
        return MoveNode(next_state, init_loc, next_loc)

    def __can_kill_left(self, state, x: int, y: int) -> bool:
        """ Seçilen taşın solunda düşman taş var ve onun solu boş """
        if x >= 2 and state[y][x - 2] == 3 and self.is_enemy(state[y][x - 1]):
            return True
        return False

    def __can_kill_up(self, state, x: int, y: int) -> bool:
        """ Seçilen taşın yukarısında düşman taş var ve onun yukarısı boş """
        """ Sadece 1. oyuncu tarafından çağrılacak !!! """
        if y >= 2 and state[y - 2][x] == 3 and self.is_enemy(state[y - 1][x]):
            return True
        return False

    def __can_kill_right(self, state, x: int, y: int):
        """ Seçilen taşın sağında düşman taş var ve onun sağı boş """
        if x <= 5 and state[y][x + 2] == 3 and self.is_enemy(state[y][x + 1]):
            return True
        return False

    def __can_kill_down(self, state, x: int, y: int) -> bool:
        """ Seçilen taşın aşağısında düşman taş var ve onun yukarısı boş """
        """ Sadece 2. oyuncu tarafından çağrılacak !!! """
        if y <= 5 and state[y + 2][x] == 3 and self.is_enemy(state[y + 1][x]):
                return True
        return False

    def __can_kill_left_long(self, state, x: int, y: int) -> tuple[int, int] | None:
        """ İlk soldan başlayarak sondan bir önceki sol kadar taş yeme durumunu kontrol eder """
        if x >= 2:
            if state[y][x - 2] == 3 and self.is_enemy(state[y][x - 1]):
                return x - 1, y
            if state[y][x - 1] == 3:
                """ Solda taş yoksa bir soldan tekrar aynı süreç başlar """
                return self.__can_kill_left_long(state, x - 1, y)

    def __can_kill_up_long(self, state, x: int, y: int) -> tuple[int, int] | None:
        """ İlk aşağıdan başlayarak sondan bir önceki aşağıya kadar taş yeme durumunu kontrol eder """
        if y >= 2:
            if state[y - 2][x] == 3 and self.is_enemy(state[y - 1][x]):
                return x, y - 1
            if state[y - 1][x] == 3:
                """ Aşağıda taş yoksa bir aşağıdan tekrar aynı süreç başlar """
                return self.__can_kill_up_long(state, x, y - 1)

    def __can_kill_right_long(self, state, x: int, y: int) -> tuple[int, int] | None:
        """ İlk sağdan başlayarak sondan bir önceki sağa kadar taş yeme durumunu kontrol eder """
        if x <= 5:
            if state[y][x + 2] == 3 and self.is_enemy(state[y][x + 1]):
                return x + 1, y
            if state[y][x + 1] == 3:
                """ Sağda taş yoksa bir sağdan tekrar aynı süreç başlar """
                return self.__can_kill_right_long(state, x + 1, y)

    def __can_kill_down_long(self, state, x: int, y: int) -> tuple[int, int] | None:
        """ İlk yukarıdan başlayarak sondan bir önceki yukarıya kadar taş yeme durumunu kontrol eder """
        if y <= 5:
            if state[y + 2][x] == 3 and self.is_enemy(state[y + 1][x]):
                return x, y + 1
            if state[y + 1][x] == 3:
                """ Yukarıda taş yoksa bir yukarıdan tekrar aynı süreç başlar """
                return self.__can_kill_down_long(state, x, y + 1)


""" Board dan hamleleri al, durumları türet, hamleleri puanla, """
class StateManager:

    def __init__(self, board: Board, game_level: int, user_is_first_player):
        self.board = board
        self.game_level = game_level
        self.turn_on_user = not user_is_first_player

    # TODO board üzerinden değil state ve hamleler üzerinden çalışmalı
    def get_ai_moves(self) -> List[StateNode]:
        """
        state_dict bir tür ağaç, her derinlikte düğümler(state_node) liste olarak tutuluyor
        ağacın yönü uçlardan köke doğru, her düğüm bir üst düğümünü father olarak tanır, hangi
        durumdan türediğini bilir
        """
        root_state = StateNode(0, self.board.state)
        state_dict: Dict[int, List[StateNode]] = {0: [root_state]}
        for lvl in range(self.game_level):
            state_dict[lvl + 1] = []
            for root_state in state_dict[lvl]:
                state_dict[lvl + 1] += self.__get_states_of_next_layer(root_state, lvl + 1)

        """ Puanlandır """
        sign = 1
        if self.game_level % 2 == 0:
            sign = -1
        for state_node in state_dict[self.game_level]:
            score_matrix = np.where(state_node.state == 1, SCORE_DICT[1], np.where(
                state_node.state == 5, SCORE_DICT[5], np.where(
                    state_node.state == 2, SCORE_DICT[2], np.where(
                        state_node.state == 4, SCORE_DICT[4], 0
                    )
                )
            ))
            state_node.value = score_matrix.sum() * sign
        for layer in range(self.game_level, 0, -1):
            for state_node in state_dict[layer]:
                # state_node.state = StateManager.reverse_state(state_node.state)
                if ((layer % 2 == 0 and state_node.father.value < state_node.value)
                        or (layer % 2 == 1 and state_node.father.value > state_node.value)):
                    state_node.father.value = state_node.value

        """ Sırala """
        first_layer = state_dict[1]
        first_layer = sorted(first_layer, key=lambda node: node.value, reverse=not self.turn_on_user)
        return first_layer

    def __get_states_of_next_layer(self, root_state: StateNode, layer: int) -> List[StateNode]:
        turn_on_first_player = self.turn_on_user
        if layer % 2 == 0:
            root_state.value = -2500
            turn_on_first_player = not turn_on_first_player
        else:
            root_state.value = 2500

        next_state_nodes: List[StateNode] = []
        final_states: List[np.ndarray] = []
        board = Board(root_state.state, turn_on_first_player)
        try:
            board.update_moves()
        except ValueError:
            if layer % 2 == 1:
                root_state.value = -10000
            else:
                root_state.value = 10000

        for root_move_nodes in board.moves.values():
            for root_move_node in root_move_nodes:
                final_states += StateManager.__get_final_states(root_move_node)

        for final_state in final_states:
            next_state_nodes.append(StateNode(0, final_state, root_state))

        return next_state_nodes

    @staticmethod
    def __get_final_states(move_node: MoveNode) -> List[np.ndarray]:
        final_states: List[np.ndarray] = []
        if len(move_node.next_nodes) == 0:
            final_states.append(move_node.next_state)
            return final_states
        for next_node in move_node.next_nodes:
            final_states += StateManager.__get_final_states(next_node)
        return final_states

    @staticmethod
    def reverse_state(state):
        return 6 - np.flip(state)




