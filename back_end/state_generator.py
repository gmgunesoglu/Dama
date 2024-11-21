"""
    Bu modülün amacı: bir durumdan türeyebilecek diğer durumları bulmaktır.

    Algoritması diyagram olarak verilmiştir.

    Sadece beyaz taşlar üzerinden hesaplama yapar, dolayısıyla oyuncu sırasının değişmesi durumunda,
    state in simetrisi referans alınır.
"""

from back_end.dto import Board, SquareType
from typing import List, Dict


class StateGenerator:
    def __init__(self, board: Board):
        self.board = board

    def update_selectable_pieces(self):
        indexes_of_selectable_pieces = self.__select_stones_that_have_to_move()
        if len(indexes_of_selectable_pieces) == 0:
            indexes_of_selectable_pieces = self.__select_stones_that_can_move()
            if len(indexes_of_selectable_pieces) == 0:
                print(self.board.state)
                raise ValueError(f"[-] player hasn't a move, this is an unexpected state!")
        self.board.indexes_of_selectable_pieces = indexes_of_selectable_pieces
        print(self.board.indexes_of_selectable_pieces)

    """ Taş yeme zorunluluğu olan taşları bulur"""
    def __select_stones_that_have_to_move(self) -> set:
        state = self.board.state
        indexes_of_selectable_pieces = set()
        for y in range(8):
            for x in range(8):
                if state[y][x] == SquareType.m:
                    if self.__can_kill_left(x, y) or self.__can_kill_up(x, y) or self.__can_kill_right(x, y):
                        indexes_of_selectable_pieces.add(y * 8 + x)
                elif state[y][x] == SquareType.M:
                    if self.__can_kill_left_long(x, y) or self.__can_kill_down_long(x, y) or self.__can_kill_right_long(x, y) or self.__can_kill_up_long(x, y):
                        indexes_of_selectable_pieces.add(y)
        return indexes_of_selectable_pieces

    def __select_stones_that_can_move(self) -> set:
        state = self.board.state
        indexes_of_selectable_pieces = set()
        for y in range(8):
            for x in range(8):
                if state[y][x] == SquareType.m:
                    if self.__left_is_free(x, y) or self.__up_is_free(x, y) or self.__right_is_free(x, y):
                        indexes_of_selectable_pieces.add(y * 8 + x)
                elif state[y][x] == SquareType.M:
                    print("will be add")
        return indexes_of_selectable_pieces

    def __left_is_free(self, x: int, y: int) -> bool:
        if x > 0 and self.board.state[y][x - 1] == SquareType.O:
            return True
        return False

    def __up_is_free(self, x: int, y: int) -> bool:
        if y > 1 and self.board.state[y - 1][x] == SquareType.O:
            return True
        return False

    def __right_is_free(self, x: int, y: int) -> bool:
        if x < 7 and self.board.state[y][x + 1] == SquareType.O:
            return True
        return False

    def __can_kill_left(self, x: int, y: int) -> bool:
        """ Seçilen taşın solunda düşman taş var ve onun solu boş """
        """ 0b....01 2. oyuncunun taşı demek... """
        if x >= 2 and self.board.state[y][x - 2] == SquareType.O and self.board.state[y][x - 1].value | 0b100 == 0b101:
            return True
        return False

    def __can_kill_up(self, x: int, y: int) -> bool:
        """ Seçilen taşın yukarısında düşman taş var ve onun yukarısı boş """
        if y >= 2 and self.board.state[y - 2][x] == SquareType.O and self.board.state[y - 1][x].value | 0b100 == 0b101:
            print(f"board state:{bin(self.board.state[y - 1][x].value)}")
            return True
        return False

    def __can_kill_right(self, x: int, y: int):
        """ Seçilen taşın sağında düşman taş var ve onun sağı boş """
        if x <= 5 and self.board.state[y][x + 2] == SquareType.O and self.board.state[y][x + 1].value | 0b100 == 0b101:
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

