import pygame
import sys
from enum import Enum
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


# arka planın üzerine taşlar daire olarak çiziliyor,
# bu içlemi hızlandırmak için hashmap...
PIECE_IMAGE_MAP = {
    PieceType.m: pygame.transform.scale(pygame.image.load("source/m.png").convert_alpha(), (80, 80)),
    PieceType.M: pygame.transform.scale(pygame.image.load("source/mm.png").convert_alpha(), (80, 80)),
    PieceType.w: pygame.transform.scale(pygame.image.load("source/w.png").convert_alpha(), (80, 80)),
    PieceType.W: pygame.transform.scale(pygame.image.load("source/ww.png").convert_alpha(), (80, 80))
}



# Tavlın tüm kareleri ve karelerin tipleri, bir durumdur
STATE = [
            [SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O],
            [SquareType.w, SquareType.w, SquareType.w, SquareType.w, SquareType.w, SquareType.w, SquareType.w, SquareType.w],
            [SquareType.w, SquareType.w, SquareType.w, SquareType.w, SquareType.w, SquareType.w, SquareType.w, SquareType.w],
            [SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O],
            [SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O],
            [SquareType.m, SquareType.m, SquareType.m, SquareType.m, SquareType.m, SquareType.m, SquareType.m, SquareType.m],
            [SquareType.m, SquareType.m, SquareType.m, SquareType.m, SquareType.m, SquareType.m, SquareType.m, SquareType.m],
            [SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O, SquareType.O],
        ]


class Piece:
    def __init__(self, type: PieceType, x_pos: int, y_pos: int):
        self.type = type
        self.x_pos = x_pos
        self.y_pos = y_pos


pieces = [
    Piece(PieceType.w, 160, 260),
    Piece(PieceType.m, 760, 560)
]


def get_clicked_piece(mouse_pos) -> SquareType | None:

    """
    İlk önce tıklanan satır ve stunu bulup o karenin merkezini bulur.
    Eğer tıklanan kare de taş varsa ve tıklama taşın üzerine denk geliyorsa
    Taş seçilir ve döndürülür
    """

    if mouse_pos[0] > 840 or mouse_pos[0] < 60 or mouse_pos[1] > 840 or mouse_pos[1] < 60:
        return

    col = int((mouse_pos[0] - 50) / 100)
    row = int((mouse_pos[1] - 50) / 100)
    if STATE[row][col] == SquareType.O:
        return

    center_x = col * 100 + 100
    center_y = row * 100 + 100
    print(f"center_x:{center_x}, center_y:{center_y}")
    print(f"col:{col}, row:{row}")
    print(f"piece_type:{STATE[row][col].name}")
    distance = ((mouse_pos[0] - center_x) ** 2 + (mouse_pos[1] - center_y) ** 2) ** 0.5
    if distance <= 40:
        return STATE[row][col]


def drive_pieces():
    for y in range(8):
        for x in range(8):
            if STATE[y][x] != SquareType.O:
                image = PIECE_IMAGE_MAP[PieceType[STATE[y][x].name]]
                screen.blit(image, (x * 100 + 60, y * 100 + 60))


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
                clicled_piece = get_clicked_piece(mouse_pos)
                print(clicled_piece)

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
