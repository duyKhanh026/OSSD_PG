import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Thiết lập màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Platformer")

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Khối vuông người chơi
player_size = 50
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_velocity = 10

# Hạnh động nhảy
is_jump = False
jump_count = 10

# Vòng lặp chính
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Di chuyển sang trái
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_velocity
    # Di chuyển sang phải
    if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_size:
        player_pos[0] += player_velocity

    # Nhảy
    if not is_jump:
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_pos[1] -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 10

    # Vẽ người chơi
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

    # Cập nhật màn hình
    pygame.display.update()
    pygame.time.Clock().tick(120)
