import pygame
import sys
from enum import Enum
import numpy as np
from back_end.dto import SquareType, PieceType, Board, MoveNode
from back_end.state_generator import MoveGenerator
from typing import List


# pygame i kullanabilmek için init edilmesi gerekiyor
pygame.init()

# ekran her zaman sabit ve 900 e 900 olacak
SCREEN_WIDTH = 900

# Pencere oluşturuluyor
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
pygame.display.set_caption("DAMA")

# Arka plan resmi yükleniyor
background = pygame.image.load("source/board.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_WIDTH))
screen.blit(background, (0, 0))


# arka planın üzerine taşlar daire olarak çiziliyor,
# bu içlemi hızlandırmak için hashmap...
PIECE_IMAGE_MAP = {
    PieceType.m: pygame.transform.scale(pygame.image.load("source/m.png").convert_alpha(), (80, 80)),
    PieceType.M: pygame.transform.scale(pygame.image.load("source/mm.png").convert_alpha(), (80, 80)),
    PieceType.w: pygame.transform.scale(pygame.image.load("source/w.png").convert_alpha(), (80, 80)),
    PieceType.W: pygame.transform.scale(pygame.image.load("source/ww.png").convert_alpha(), (80, 80))
}


board = Board()
move_generator = MoveGenerator(board)
move_generator.update_selectable_pieces()


def get_col_row(mouse_pos) -> tuple[int, int] |None:
    if mouse_pos[0] > 850 or mouse_pos[0] < 50 or mouse_pos[1] > 850 or mouse_pos[1] < 50:
        return
    col = int((mouse_pos[0] - 50) / 100)
    row = int((mouse_pos[1] - 50) / 100)
    return col, row


def get_moveable_piece(mouse_pos) -> tuple[int, int] | None:

    """
    İlk önce tıklanan satır ve stunu bulup o karenin merkezini bulur.
    Eğer tıklanan kare de taş varsa, taş oyuncunun taşıysa ve oynanabilir ise
    taşın olduğu stun(x) satır(y) döner
    """
    pos = get_col_row(mouse_pos)
    if not pos:
        return

    col, row = pos
    if board.state[row][col].value & SquareType.m.value != SquareType.m.value:
        return
    center_x = col * 100 + 100
    center_y = row * 100 + 100
    distance = ((mouse_pos[0] - center_x) ** 2 + (mouse_pos[1] - center_y) ** 2) ** 0.5
    if distance <= 40:
        return col, row


""" Taşların şekillerini çizer """
def drive_pieces():
    for y in range(8):
        for x in range(8):
            if board.state[y][x] != SquareType.O:
                image = PIECE_IMAGE_MAP[PieceType((PieceType[SquareType(board.state[y][x]).name]))]
                screen.blit(image, (x * 100 + 60, y * 100 + 60))


""" Oynayabilir bir taş seçildiğinde hangi karelere hareket ettirebileceği gösterilir """
def select_and_mark_squares_that_piece_can_move(clicked_piece: tuple[int, int] | None) -> List[tuple[int, int]]:
    squares_that_piece_can_move: List[tuple[int, int]] = []
    if clicked_piece and clicked_piece in board.moves:
        move_nodes = board.moves[clicked_piece]
        for move_node in move_nodes:
            x, y = move_node.next_loc
            squares_that_piece_can_move.append((x, y))
            color = (0, 255, 0, 50)  # Saydam yeşil (RGBA)
            # Saydam yüzey oluştur
            overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_WIDTH), pygame.SRCALPHA)
            # Saydam yüzey üzerine kare çiz
            pygame.draw.rect(overlay_surface, color, (x * 100 + 50, y * 100 + 50, 100, 100))
            # Ana yüzeyin üzerine saydam yüzeyi yerleştir
            screen.blit(overlay_surface, (0, 0))
    return squares_that_piece_can_move


""" Hamle yapıldığında bir sonraki geçişi yapıp tabloyu günceller """
def load_next_state(piece_loc: tuple[int, int], picked_loc: tuple[int, int]):
    move_nodes = board.moves[piece_loc]
    for move in move_nodes:
        if move.next_loc == picked_loc:
            board.update_state(move.next_state)
            if len(move.next_nodes) == 0:
                print("zincir hamle değil")
                move_generator.update_selectable_pieces()
            else:
                board.moves.clear()
                board.moves[picked_loc] = move.next_nodes
                print("zincir hame")


def main():
    clock = pygame.time.Clock()
    selected_movable_piece: tuple[int, int] | None = None
    squares_that_piece_can_move: List[tuple[int, int]] = []

    # Ana döngü
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if selected_movable_piece:
                    col_row = get_col_row(mouse_pos)
                    if col_row and col_row in squares_that_piece_can_move:
                        # hamle yapılıyor
                        load_next_state(selected_movable_piece, col_row)
                        # state_generator.update_selectable_pieces()
                selected_movable_piece = get_moveable_piece(mouse_pos)

        # Arka planı tekrar çiz
        screen.blit(background, (0, 0))
        # Arka planın üzerine taşları çiz
        drive_pieces()
        # oynanabilir bir taş seçilmişse oynayabileceği kareleri yeşil belirt ve oynanabilir karelerin konumları döndür
        squares_that_piece_can_move = select_and_mark_squares_that_piece_can_move(selected_movable_piece)

        # Ekranı güncelle
        pygame.display.update()

        # FPS sınırı
        clock.tick(10)


if __name__ == "__main__":
    main()
