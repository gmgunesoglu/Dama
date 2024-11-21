from time import sleep

import pygame
import sys
from enum import Enum
import numpy as np
from back_end.dto import SquareType, PieceType, Board
from back_end.state_generator import StateGenerator
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
state_generator = StateGenerator(board)
state_generator.update_selectable_pieces()


def get_clicked_piece(mouse_pos) -> int | None:

    """
    İlk önce tıklanan satır ve stunu bulup o karenin merkezini bulur.
    Eğer tıklanan kare de taş varsa ve tıklama taşın üzerine denk geliyorsa
    Taş seçilir ve döndürülür
    """

    if mouse_pos[0] > 840 or mouse_pos[0] < 60 or mouse_pos[1] > 840 or mouse_pos[1] < 60:
        return

    col = int((mouse_pos[0] - 50) / 100)
    row = int((mouse_pos[1] - 50) / 100)
    if board.state[row][col] == SquareType.O:
        return

    center_x = col * 100 + 100
    center_y = row * 100 + 100
    # print(f"center_x:{center_x}, center_y:{center_y}")
    # print(f"col:{col}, row:{row}")
    # print(f"piece_type:{board.state[row][col].name}")
    distance = ((mouse_pos[0] - center_x) ** 2 + (mouse_pos[1] - center_y) ** 2) ** 0.5
    if distance <= 40:
        return row * 8 + col


def drive_pieces():
    for y in range(8):
        for x in range(8):
            if board.state[y][x] != SquareType.O:
                image = PIECE_IMAGE_MAP[PieceType((PieceType[SquareType(board.state[y][x]).name]))]
                screen.blit(image, (x * 100 + 60, y * 100 + 60))


def mark_squares_that_stone_can_move(x, y):
    color = (0, 255, 0, 50)  # Saydam yeşil (RGBA)

    # Saydam yüzey oluştur
    overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_WIDTH), pygame.SRCALPHA)

    # Saydam yüzey üzerine kare çiz
    pygame.draw.rect(overlay_surface, color, (x, y, 100, 100))

    # Ana yüzeyin üzerine saydam yüzeyi yerleştir
    screen.blit(overlay_surface, (0, 0))

    # Ekranı güncelle
    pygame.display.update()

    sleep(2)


def main():
    clock = pygame.time.Clock()

    # Ana döngü
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                pos = get_clicked_piece(mouse_pos)
                if pos:
                    print(f"x: {pos % 8}, y:{pos // 8}")
                    if pos in board.indexes_of_selectable_pieces:
                        mark_squares_that_stone_can_move((pos % 8) * 100 + 50, (pos // 8) * 100 + 50)
                        print("tıklanabilir")
                        print()
                    else:
                        print(board.indexes_of_selectable_pieces)

        # Arka planı tekrar çiz
        screen.blit(background, (0, 0))
        # Arka planın üzerine taşları çiz
        drive_pieces()

        # Ekranı güncelle
        pygame.display.update()

        # FPS sınırı
        clock.tick(70)


if __name__ == "__main__":
    main()
