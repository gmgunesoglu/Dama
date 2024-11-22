"""
    Bu modülün amacı: bir durumdan türeyebilecek diğer durumları bulmaktır.

    Algoritması diyagram olarak verilmiştir.

    Sadece beyaz taşlar üzerinden hesaplama yapar, dolayısıyla oyuncu sırasının değişmesi durumunda,
    state in simetrisi referans alınır.
"""

from back_end.dto import Board, SquareType, MoveNode
from typing import List, Dict
import numpy as np


class StateGenerator:
    def __init__(self, board: Board):
        self.board = board

    def update_selectable_pieces(self):
        moves: Dict[tuple[int, int]: List[MoveNode]]

        indexes_of_selectable_pieces = self.__select_stones_that_have_to_move()
        if len(indexes_of_selectable_pieces) == 0:
            indexes_of_selectable_pieces = self.__select_stones_that_can_move()
            if len(indexes_of_selectable_pieces) == 0:
                print(self.board.state)
                raise ValueError(f"[-] player hasn't a move, this is an unexpected state!")

            else:
                """ Normal hamle yapmak gerekiyor """
                moves = self.__find_normal_moves(indexes_of_selectable_pieces)
                self.board.moves = moves
        else:
            """ Taş yemek gerekiyor"""
            moves = self.__find_mandatory_moves(indexes_of_selectable_pieces)
            self.board.moves = moves
            print("eklenecek...")

        print("boş...")

    """ Taş yeme zorunluluğu olan taşların konumlarını bulur """
    def __select_stones_that_have_to_move(self) -> List[tuple[int, int]]:
        state = self.board.state
        indexes_of_selectable_pieces: List[tuple[int, int]] = []
        for y in range(8):
            for x in range(8):
                if state[y][x] == SquareType.m:
                    if StateGenerator.__can_kill_left(self.board.state, x, y) or StateGenerator.__can_kill_up(self.board.state, x, y) or StateGenerator.__can_kill_right(self.board.state, x, y):
                        indexes_of_selectable_pieces.append((x, y))
                elif state[y][x] == SquareType.M:
                    if self.__can_kill_left_long(x, y) or self.__can_kill_down_long(x, y) or self.__can_kill_right_long(x, y) or self.__can_kill_up_long(x, y):
                        indexes_of_selectable_pieces.append((x, y))
        return indexes_of_selectable_pieces

    """ Hamle yapabilen taşların konumlarını bulur """
    def __select_stones_that_can_move(self) -> List[tuple[int, int]]:
        state = self.board.state
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
            if self.board.state[y][x] == SquareType.m:
                """ Normal taş hamleleri """
                if self.__left_is_free(x, y):
                    next_state = self.board.state.copy()
                    next_state[y][x] = SquareType.O
                    next_state[y][x - 1] = SquareType.m
                    move = MoveNode(next_state, (x, y), (x - 1, y))
                    moves[(x, y)].append(move)
                if self.__up_is_free(x, y):
                    next_state = self.board.state.copy()
                    next_state[y][x] = SquareType.O
                    next_state[y - 1][x] = SquareType.m
                    move = MoveNode(next_state, (x, y), (x, y - 1))
                    moves[(x, y)].append(move)
                if self.__right_is_free(x, y):
                    next_state = self.board.state.copy()
                    next_state[y][x] = SquareType.O
                    next_state[y][x + 1] = SquareType.m
                    move = MoveNode(next_state, (x, y), (x + 1, y))
                    moves[(x, y)].append(move)
            elif self.board.state[y][x] == SquareType.M:
                """ Dama hamleleri """
                moves[(x, y)] = self.__left_is_free_long(x, y) + self.__up_is_free_long(x, y) + self.__right_is_free_long(x, y) + self.__down_is_free_long(x, y)

        return moves

    def __find_mandatory_moves(self, stones_can_move: List[tuple[int, int]]) -> Dict[tuple[int, int], List[MoveNode]]:
        moves: Dict[tuple[int, int], List[MoveNode]] = {}
        for x, y in stones_can_move:
            moves[(x, y)] = []
            # listeyi filtrele, en çok taş yenecek hamleler kalsın
            if self.board.state[y][x] == SquareType.m:
                """ Normal taş hamleleri """
                """ 
                    bir taş, birden fazla taş yiyebilir ve bu farklı hamlelerle yapılabilir, bana lazım olan şey:
                    Birden fazla taş yeme durumu haritalanmalı, ve kaç taş yediği dönmeli
                    Haritalandırma: taşın hareket ettiği konumlar ve oluşan ara geçiş durumları
                    List[Sınıf->attack map/move etc...] 
                """
                moves[(x, y)] = StateGenerator.__get_attack_moves_m(self.board.state, x, y)

            elif self.board.state[y][x] == SquareType.M:
                """ Dama hamleleri """
                moves[(x, y)] = self.__left_is_free_long(x, y) + self.__up_is_free_long(x, y) + self.__right_is_free_long(x, y) + self.__down_is_free_long(x, y)

        return moves

    @staticmethod
    def __get_attack_moves_m(state: np.ndarray, x: int, y: int) -> List[MoveNode]:
        moves: List[MoveNode] = []
        if StateGenerator.__can_kill_left(state, x, y):
            next_state = state.copy()
            next_state[y][x] = SquareType.O
            next_state[y][x - 1] = SquareType.O
            next_state[y][x - 2] = SquareType.m
            node = MoveNode(next_state, (x, y), (x - 2, y))
            node.next_nodes = StateGenerator.__get_attack_moves_m(next_state, x - 2, y)
            moves.append(node)
        if StateGenerator.__can_kill_up(state, x, y):
            next_state = state.copy()
            next_state[y][x] = SquareType.O
            next_state[y - 1][x] = SquareType.O
            next_state[y - 2][x] = SquareType.m
            node = MoveNode(next_state, (x, y), (x, y - 2))
            node.next_nodes = StateGenerator.__get_attack_moves_m(next_state, x, y - 2)
            moves.append(node)
        if StateGenerator.__can_kill_right(state, x, y):
            next_state = state.copy()
            next_state[y][x] = SquareType.O
            next_state[y][x + 1] = SquareType.O
            next_state[y][x + 2] = SquareType.m
            node = MoveNode(next_state, (x, y), (x + 2, y))
            node.next_nodes = StateGenerator.__get_attack_moves_m(next_state, x + 2, y)
            moves.append(node)
        return moves

    def __left_is_free(self, x: int, y: int) -> bool:
        if x >= 1 and self.board.state[y][x - 1] == SquareType.O:
            return True
        return False

    def __up_is_free(self, x: int, y: int) -> bool:
        if y >= 1 and self.board.state[y - 1][x] == SquareType.O:
            return True
        return False

    def __right_is_free(self, x: int, y: int) -> bool:
        if x <= 6 and self.board.state[y][x + 1] == SquareType.O:
            return True
        return False

    def __down_is_free(self, x: int, y: int) -> bool:
        if y <= 6 and self.board.state[y + 1][x] == SquareType.O:
            return True
        return False

    def __left_is_free_long(self, x: int, y: int) -> List[MoveNode]:
        moves: List[MoveNode] = []
        final_x = x
        while self.__left_is_free(x, y):
            next_state = self.board.state.copy()
            next_state[y][final_x] = SquareType.O
            x -= 1
            next_state[y][x] = SquareType.M
            moves.append(MoveNode(next_state, (final_x, y), (x, y)))
        return moves

    def __up_is_free_long(self, x: int, y: int) -> List[MoveNode]:
        moves: List[MoveNode] = []
        final_y = y
        while self.__up_is_free(x, y):
            next_state = self.board.state.copy()
            next_state[final_y][x] = SquareType.O
            y -= 1
            next_state[y][x] = SquareType.M
            moves.append(MoveNode(next_state, (x, final_y), (x, y)))
        return moves

    def __right_is_free_long(self, x: int, y: int) -> List[MoveNode]:
        moves: List[MoveNode] = []
        final_x = x
        while self.__right_is_free(x, y):
            next_state = self.board.state.copy()
            next_state[y][final_x] = SquareType.O
            x += 1
            next_state[y][x] = SquareType.M
            moves.append(MoveNode(next_state, (final_x, y), (x, y)))
        return moves

    def __down_is_free_long(self, x: int, y: int) -> List[MoveNode]:
        moves: List[MoveNode] = []
        final_y = y
        while self.__down_is_free(x, y):
            next_state = self.board.state.copy()
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

    def __can_kill_left_long(self, x: int, y: int):
        """ İlk soldan başlayarak sondan bir önceki sol kadar taş yeme durumunu kontrol eder """
        if x >= 2:
            if self.board.state[y][x - 2] == SquareType.O and self.board.state[y][x - 1].value | 0b100 == 0b101:
                return True
            if self.board.state[y][x - 1] == SquareType.O:
                """ Solda taş yoksa bir soldan tekrar aynı süreç başlar """
                return self.__can_kill_left_long(x - 1, y)
            return False
        return False

    def __can_kill_up_long(self, x: int, y: int):
        """ İlk aşağıdan başlayarak sondan bir önceki aşağıya kadar taş yeme durumunu kontrol eder """
        if y >= 2:
            if self.board.state[y - 2][x] == SquareType.O and self.board.state[y - 1][x].value | 0b100 == 0b101:
                return True
            if self.board.state[y - 1][x] == SquareType.O:
                """ Aşağıda taş yoksa bir aşağıdan tekrar aynı süreç başlar """
                return self.__can_kill_up_long(x, y - 1)
            return False
        return False

    def __can_kill_right_long(self, x: int, y: int):
        """ İlk sağdan başlayarak sondan bir önceki sağa kadar taş yeme durumunu kontrol eder """
        if x <= 5:
            if self.board.state[y][x + 2] == SquareType.O and self.board.state[y][x + 1].value | 0b100 == 0b101:
                return True
            if self.board.state[y][x + 1] == SquareType.O:
                """ Sağda taş yoksa bir sağdan tekrar aynı süreç başlar """
                return self.__can_kill_right_long(x + 1, y)
            return False
        return False

    def __can_kill_down_long(self, x: int, y: int):
        """ İlk yukarıdan başlayarak sondan bir önceki yukarıya kadar taş yeme durumunu kontrol eder """
        if y <= 5:
            if self.board.state[y + 2][x] == SquareType.O and self.board.state[y + 1][x].value | 0b100 == 0b101:
                return True
            if self.board.state[y + 1][x] == SquareType.O:
                """ Yukarıda taş yoksa bir yukarıdan tekrar aynı süreç başlar """
                return self.__can_kill_down_long(x, y + 1)
            return False
        return False

