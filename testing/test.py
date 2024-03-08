import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Định nghĩa màu sắc
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Cấu hình cửa sổ
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game")

# Định nghĩa nhân vật
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)

    def update(self):
        pass

# Định nghĩa đạn
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

# Tạo nhóm sprite
all_sprites = pygame.sprite.Group()
character = Character()
all_sprites.add(character)
bullets = pygame.sprite.Group()

# Vòng lặp chính của game
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(character.rect.centerx, character.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Cập nhật
    all_sprites.update()

    # Vẽ
    window.fill(BLACK)
    all_sprites.draw(window)

    # Hiển thị
    pygame.display.flip()

    # Giới hạn FPS
    clock.tick(60)

# Kết thúc Pygame
pygame.quit()
sys.exit()
