import pygame
import random

# Định nghĩa màu sắc
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Khởi tạo pygame
pygame.init()

# Thiết lập màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bot Game')

# Định nghĩa lớp cho khối vuông đỏ
class RedSquare:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = RED
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def move_towards(self, target, grid):
        # Tính toán hướng di chuyển
        dx = target.rect.x - self.rect.x
        dy = target.rect.y - self.rect.y

        # Tìm hướng di chuyển tối ưu dựa trên mảng địa hình
        if dx != 0:
            dx = dx // abs(dx)
        if dy != 0:
            dy = dy // abs(dy)

        # Di chuyển theo hướng tối ưu
        next_x = self.rect.x + dx * 5
        next_y = self.rect.y + dy * 5
        if grid[next_y // 50][next_x // 50] == 1:
            self.rect.x = next_x
            self.rect.y = next_y

            # Kiểm tra va chạm với địa hình
            if grid[self.rect.y // 50][self.rect.x // 50] == 0:
                self.rect.x -= dx * 5
                self.rect.y -= dy * 5


# Định nghĩa lớp cho khối vuông xanh
class GreenSquare:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = GREEN
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def move_random(self, grid):
        # Tạo vị trí ngẫu nhiên cho khối vuông xanh
        while True:
            x = random.randint(0, WIDTH - 50)
            y = random.randint(0, HEIGHT - 50)
            if grid[y // 50][x // 50] == 1:
                self.rect.x = x
                self.rect.y = y
                break

# Tạo một mảng địa hình
grid = [[1 for _ in range(WIDTH // 50)] for _ in range(HEIGHT // 50)]
# Thiết lập các ô không thể đi qua
grid[1][4] = 0
grid[2][4] = 0
grid[3][4] = 0
grid[4][4] = 0

# Khởi tạo đối tượng cho khối vuông đỏ và khối vuông xanh
red_square = RedSquare(50, 50)
green_square = GreenSquare(random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50))

# Vòng lặp chính của trò chơi
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Di chuyển khối vuông đỏ tới khối vuông xanh
    red_square.move_towards(green_square, grid)

    # Kiểm tra va chạm giữa khối vuông đỏ và khối vuông xanh
    if red_square.rect.colliderect(green_square.rect):
        # Di chuyển khối vuông xanh đến vị trí mới
        green_square.move_random(grid)

    # Vẽ các khối vuông
    red_square.draw()
    green_square.draw()

    # Vẽ địa hình
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 0:
                pygame.draw.rect(screen, BLACK, pygame.Rect(x * 50, y * 50, 50, 50))

    # Cập nhật màn hình
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
