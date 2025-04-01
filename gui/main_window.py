from time import sleep

import pygame
import sys
from enum import Enum
import numpy as np
# from back_end.dto import
from back_end.service import Board, StateManager, MoveNodeDTO, StateNodeDTO
from typing import List


# pygame i kullanabilmek için init edilmesi gerekiyor
pygame.init()

# ekran her zaman sabit ve 900 e 900 olacak
SCREEN_WIDTH = 900
menu_width = 400
menu_height = 400
menu_x = (SCREEN_WIDTH - menu_width) // 2
menu_y = (SCREEN_WIDTH - menu_height) // 2

# Pencere oluşturuluyor
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
pygame.display.set_caption("DAMA")

# Arka plan resmi yükleniyor
background = pygame.image.load("source/board.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_WIDTH))
screen.blit(background, (0, 0))


# arka planın üzerine taşlar daire olarak çiziliyor,
# bu işlemi hızlandırmak için hashmap...
PIECE_IMAGE_MAP = {
    5: pygame.transform.scale(pygame.image.load("source/m.png").convert_alpha(), (80, 80)),
    4: pygame.transform.scale(pygame.image.load("source/mm.png").convert_alpha(), (80, 80)),
    1: pygame.transform.scale(pygame.image.load("source/w.png").convert_alpha(), (80, 80)),
    2: pygame.transform.scale(pygame.image.load("source/ww.png").convert_alpha(), (80, 80))
}

# oyun ayarları
# direct_view = False
user_is_first_player = False
game_level = 4
is_game_continue = True
game_result: str = ""


# state =  np.array([
#                 [3, 3, 3, 3, 3, 3, 2, 3],
#                 [3, 3, 3, 3, 3, 3, 3, 3],
#                 [3, 3, 3, 3, 3, 3, 3, 3],
#                 [3, 3, 3, 3, 3, 3, 3, 2],
#                 [3, 3, 3, 3, 3, 3, 3, 3],
#                 [3, 3, 3, 3, 3, 3, 3, 3],
#                 [3, 3, 3, 3, 3, 3, 3, 3],
#                 [2, 3, 3, 3, 3, 3, 3, 4],
#             ], dtype=int)
# board = Board(state, False)
state =  np.array([
                [3, 3, 3, 3, 3, 3, 3, 3],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [3, 3, 3, 3, 3, 3, 3, 3],
                [3, 3, 3, 3, 3, 3, 3, 3],
                [5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5],
                [3, 3, 3, 3, 3, 3, 3, 3],
            ], dtype=int)
board: Board
state_manager: StateManager
mark_of_ai_move: List[tuple[int, int]] = []


def get_col_row(mouse_pos) -> tuple[int, int] |None:
    if mouse_pos[0] > 850 or mouse_pos[0] < 50 or mouse_pos[1] > 850 or mouse_pos[1] < 50:
        return
    col = int((mouse_pos[0] - 50) / 100)
    row = int((mouse_pos[1] - 50) / 100)
    return col, row


def get_moveable_piece(mouse_pos) -> tuple[int, int] | None:
    """
    İlk önce tıklanan satır ve stunu bulup o karenin merkezini bulur.
    Eğer tıklanan kare de taş varsa, taş oynanabilir bir taş ise
    taşın olduğu stun(x) satır(y) döner
    """
    pos = get_col_row(mouse_pos)
    if not pos:
        return

    col, row = pos
    center_x = col * 100 + 100
    center_y = row * 100 + 100
    distance = ((mouse_pos[0] - center_x) ** 2 + (mouse_pos[1] - center_y) ** 2)
    if distance <= 1600:
        return col, row


""" Taşların şekillerini çizer (dairesel şekiller) """
def drive_pieces():
    for y in range(8):
        for x in range(8):
            if board.state[y][x] != 3:
                image = PIECE_IMAGE_MAP[board.state[y][x]]
                # TODO optimizasyon gerekli
                screen.blit(image, (x * 100 + 60, y * 100 + 60))


""" Oynayabilir bir taş seçildiğinde hangi karelere hareket ettirebileceği gösterilir ve döndürür """
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


""" Kullanıcının hamlesini gerçekleştirir """
def effect_user_move(piece_loc: tuple[int, int], picked_loc: tuple[int, int]):
    move_nodes = board.moves[piece_loc]
    for move in move_nodes:
        if move.next_loc == picked_loc:
            board.update_state(move.next_state)
            if len(move.next_nodes) == 0:
                # print("zincir hamle değil")
                board.load_next_state(move.next_state)
                print(f"\nusers_last_sate:\n{move.next_state}")
                if check_is_game_over(move.next_state):
                    return False
                board.update_moves()
                return False
            else:
                board.moves.clear()
                board.moves[picked_loc] = move.next_nodes
                # print("zincir hame")
                return True


def check_is_game_over(current_state: np.ndarray):
    global game_result
    global is_game_continue
    global user_is_first_player
    # beyazın yenmesi
    w_count = np.sum(current_state < 3)
    if user_is_first_player and w_count == 0:
        game_result = "KAZANDIN"
        is_game_continue = False
        return True
    # siyahın yenmesi
    m_count = np.sum(current_state > 3)
    if not user_is_first_player and m_count == 0:
        game_result = "KAZANDIN"
        is_game_continue = False
        return True

    # beraberlik
    if w_count == 1 and m_count == 1:
        game_result = "BERABERE"
        is_game_continue = False
        return True

    return False


def ai_move():
    next_states = state_manager.get_ai_moves()
    for next_state in next_states:
        update_mark_of_ai_move(next_states[0].state)
        board.load_next_state(next_states[0].state)
        if next_state.is_leaf:
            global is_game_continue
            global game_result
            is_game_continue = False
            if next_state.value == 0:
                game_result = "BERABERE"
            else:
                game_result = "KAYBETTİN"
        board.update_moves()
        break


def update_mark_of_ai_move(next_state: np.ndarray):
    for root_nodes in board.moves.values():
        for root_node in root_nodes:
            if get_trace_of_move(root_node, next_state):
                mark_of_ai_move.append(root_node.init_loc)
                # print(f"trace: {mark_of_ai_move}")


def mark_ai_move():
    for x, y in mark_of_ai_move:
        color = (0, 0, 255, 50)  # Saydam yeşil (RGBA)
        # Saydam yüzey oluştur
        overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_WIDTH), pygame.SRCALPHA)
        # Saydam yüzey üzerine kare çiz
        pygame.draw.rect(overlay_surface, color, (x * 100 + 50, y * 100 + 50, 100, 100))
        # Ana yüzeyin üzerine saydam yüzeyi yerleştir
        screen.blit(overlay_surface, (0, 0))


def get_trace_of_move(move_node: MoveNodeDTO, target_state: np.ndarray):
    if np.array_equal(move_node.next_state, target_state):
        return True
    for next_node in move_node.next_nodes:
        if get_trace_of_move(next_node, target_state):
            mark_of_ai_move.append(next_node.init_loc)
            return True
    return False


def menu():
    global user_is_first_player
    global game_level
    global is_game_continue
    is_game_continue = True
    menu_color = (72, 30, 20)
    menu_option_color = (155, 57, 34)

    title_font = pygame.font.Font(None, 56)
    button_font = pygame.font.Font(None, 40)

    # Menü arka planı
    menu_background = pygame.Surface((menu_width, menu_height))
    menu_background.fill(menu_color)  # Menü arka plan rengi

    # Menü başlığı
    title_text = title_font.render("OYUN MODU", True, (255, 255, 255))
    title_x = menu_width // 2 - title_text.get_width() // 2

    # Buton boyutları
    button_1_rect = pygame.Rect(menu_x + 50, menu_y + 110, 300, 50)
    button_2_rect = pygame.Rect(menu_x + 50, menu_y + 180, 300, 50)
    button_3_rect = pygame.Rect(menu_x + 50, menu_y + 250, 300, 50)
    button_4_rect = pygame.Rect(menu_x + 50, menu_y + 320, 300, 50)

    while True:


        # Menü yüzeyini çizin
        screen.blit(menu_background, (menu_x, menu_y))
        screen.blit(title_text, (menu_x + title_x, menu_y + 50))

        # Butonları çizin
        pygame.draw.rect(screen, menu_option_color, button_1_rect)
        pygame.draw.rect(screen, menu_option_color, button_2_rect)
        pygame.draw.rect(screen, menu_option_color, button_3_rect)
        pygame.draw.rect(screen, menu_option_color, button_4_rect)

        button_1_text = button_font.render("1. Oyuncu", True, (255, 255, 255))
        button_2_text = button_font.render("2. Oyuncu", True, (255, 255, 255))
        button_3_text = button_font.render(f"Zorluk Seviyesi {game_level}", True, (255, 255, 255))
        button_4_text = button_font.render("Yapay Zekayı Eğit", True, (255, 255, 255))

        screen.blit(button_1_text, (button_1_rect.x + 50, button_1_rect.y + 10))
        screen.blit(button_2_text, (button_2_rect.x + 50, button_2_rect.y + 10))
        screen.blit(button_3_text, (button_3_rect.x + 50, button_3_rect.y + 10))
        screen.blit(button_4_text, (button_4_rect.x + 50, button_4_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_1_rect.collidepoint(event.pos):
                    user_is_first_player = True
                    return
                elif button_2_rect.collidepoint(event.pos):
                    user_is_first_player = False
                    return
                elif button_3_rect.collidepoint(event.pos):
                    if game_level < 5:
                        game_level += 1
                    else:
                        game_level = 1
                elif button_4_rect.collidepoint(event.pos):
                    # TODO yapay zekanın kendi kendine oynaması simüle edilecek
                    print("Bu fonksiyon geliştirme aşamasında")

        pygame.display.update()


def game_over():
    global game_result
    menu_color = (72, 30, 20)
    menu_option_color = (155, 57, 34)

    title_font = pygame.font.Font(None, 56)
    button_font = pygame.font.Font(None, 40)

    menu_background = pygame.Surface((menu_width, menu_height))
    menu_background.fill(menu_color)  # Menü arka plan rengi

    # Menü başlığı
    title_text = title_font.render(game_result, True, (255, 255, 255))
    title_x = menu_width // 2 - title_text.get_width() // 2

    # Buton boyutları
    button_1_rect = pygame.Rect(menu_x + 50, menu_y + 170, 300, 50)
    button_2_rect = pygame.Rect(menu_x + 50, menu_y + 260, 300, 50)

    while True:
        screen.blit(menu_background, (menu_x, menu_y))
        screen.blit(title_text, (menu_x + title_x, menu_y + 50))

        pygame.draw.rect(screen, menu_option_color, button_1_rect)
        pygame.draw.rect(screen, menu_option_color, button_2_rect)

        button_1_text = button_font.render("Tekrar Oyna", True, (255, 255, 255))
        button_2_text = button_font.render("Çıkış", True, (255, 255, 255))

        screen.blit(button_1_text, (button_1_rect.x + 50, button_1_rect.y + 10))
        screen.blit(button_2_text, (button_2_rect.x + 50, button_2_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_1_rect.collidepoint(event.pos):
                    return
                elif button_2_rect.collidepoint(event.pos):
                    sys.exit()
        pygame.display.update()


def main():
    # print(f"user_is_first_player = {user_is_first_player}")
    global board
    global state_manager
    global is_game_continue
    global mark_of_ai_move
    mark_of_ai_move = []
    board = Board(state, True)
    board.update_moves()
    state_manager = StateManager(board, game_level, user_is_first_player)

    selected_movable_piece: tuple[int, int] | None = None
    clock = pygame.time.Clock()
    squares_that_piece_can_move: List[tuple[int, int]] = []
    user_turn = user_is_first_player

    # Ana döngü
    while is_game_continue:
        if not user_turn:
            ai_move()
            user_turn = True
            selected_movable_piece = None
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
                        mark_of_ai_move.clear()
                        user_turn = effect_user_move(selected_movable_piece, col_row)
                        # Arka planı tekrar çiz
                        screen.blit(background, (0, 0))
                        # Arka planın üzerine taşları çiz
                        drive_pieces()
                        # Ekranı güncelle
                        pygame.display.update()

                selected_movable_piece = get_moveable_piece(mouse_pos)
                # print(f"selected: {selected_movable_piece}")

        # Arka planı tekrar çiz
        screen.blit(background, (0, 0))
        # Arka planın üzerine taşları çiz
        drive_pieces()
        # oynanabilir bir taş seçilmişse oynayabileceği kareleri yeşil belirt ve oynanabilir karelerin konumları döndür
        squares_that_piece_can_move = select_and_mark_squares_that_piece_can_move(selected_movable_piece)
        # bilgisayar hamlesini yaptıysa çiz
        mark_ai_move()

        # Ekranı güncelle
        pygame.display.update()

        # FPS sınırı
        clock.tick(10)


if __name__ == "__main__":
    while True:
        menu()
        main()
        game_over()
