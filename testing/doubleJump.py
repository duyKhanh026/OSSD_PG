import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Thiết lập màn hình
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jumping Square")

# Thiết lập màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Thiết lập hình vuông
square_size = 50
square_x = screen_width // 2 - square_size // 2
square_y = screen_height - square_size
jumping = False
jump_count = -11

clock = pygame.time.Clock()

# Vòng lặp chính của trò chơi
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:             
                jump_count = 10

    if square_y > screen_height - 50:
        neg = 1
        if jump_count < 0:
            neg = -1
        square_y -= (jump_count ** 2) * 0.5 * neg
        jump_count -= 1
    

    # Vẽ hình vuông
    pygame.draw.rect(screen, BLACK, (square_x, square_y, square_size, square_size))

    pygame.display.flip()
    clock.tick(30)
