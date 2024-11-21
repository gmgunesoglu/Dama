import pygame
import sys
import math

# Pygame'i başlat
pygame.init()

# Ekran boyutları
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900

# Renkler
TRANSPARENT_GREEN = (0, 255, 0, 80)  # Yeşil ve saydamlık (alfa kanalı ile)

# Pencere oluştur
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Nesne Hareketi")

# Arka plan resmi yükle
background = pygame.image.load("source/board.png")  # Arka plan için bir resim seçin
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Nesne ayarları
object_color = (0, 128, 255)  # Mavi bir nesne
object_width, object_height = 50, 50
object_x, object_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  # Başlangıç konumu
object_speed = 5

# Geçici renkli boyama (saydam) ayarları
overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)  # Saydam bir yüzey
overlay_surface.fill((0, 0, 0, 0))  # Başlangıçta tamamen şeffaf

# Saat (FPS için)
clock = pygame.time.Clock()


# Geçici boyama fonksiyonu
def apply_overlay(surface, x, y, angle, width, height, color):
    # Nesnenin bulunduğu açıya göre boyama yapılacak alanı hesapla
    length = 800  # Boyama alanının uzunluğu, ekran boyunca devam etmesi için
    offset = 50  # Boyama kalınlığı

    # 90 derece aralıklarla çizgi çizelim
    for i in range(0, 360, 90):  # 90 derece artışla
        # Açıya göre yeni koordinatlar hesapla
        x1 = x
        y1 = y
        x2 = x1 + length * math.cos(math.radians(i + angle))
        y2 = y1 + length * math.sin(math.radians(i + angle))

        # Boyama çizgilerini, nesnenin boyutuna göre genişletelim
        # pygame.draw.rect(surface, color, (x - width // 2, y - height // 2, width, height), 0)  # Nesneyi genişletmek
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), offset)  # Çizgi uzunluğu ve kalınlığı


# Ana döngü
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Tuşlara basıldığında hareket
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        object_x -= object_speed
    if keys[pygame.K_RIGHT]:
        object_x += object_speed
    if keys[pygame.K_UP]:
        object_y -= object_speed
    if keys[pygame.K_DOWN]:
        object_y += object_speed

    # Nesnenin ekran dışına çıkmasını önle
    object_x = max(0, min(SCREEN_WIDTH - object_width, object_x))
    object_y = max(0, min(SCREEN_HEIGHT - object_height, object_y))

    # Ekranı temizle ve eski boyamayı sil
    screen.blit(background, (0, 0))  # Arka planı çiz
    overlay_surface.fill((0, 0, 0, 0))  # Önceki boyamayı temizle

    # Geçici boyama uygulanıyor
    apply_overlay(overlay_surface, object_x + object_width // 2, object_y + object_height // 2, 0, object_width * 2,
                  object_height * 2, TRANSPARENT_GREEN)  # Boyama, nesnenin ortasında olacak

    # Boyama ve resmin karışımını yap
    screen.blit(overlay_surface, (0, 0))  # Saydam yüzeydeki boyama

    # Nesneyi çiz
    pygame.draw.rect(screen, object_color, (object_x, object_y, object_width, object_height))  # Nesneyi çiz
    pygame.display.flip()  # Ekranı yenile

    # FPS ayarı
    clock.tick(60)

# Pygame'i kapat
pygame.quit()
sys.exit()
