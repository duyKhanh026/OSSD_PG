import pygame
import sys

# Khai báo các màu sắc
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Khởi tạo Pygame
pygame.init()

# Thiết lập cửa sổ màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Friction Demo")

# Định nghĩa lớp cho khối vuông đỏ
class RedSquare:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = RED
        self.velocity_x = 10  # Tốc độ ban đầu

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        self.rect.x += self.velocity_x
        
        # Áp dụng ma sát
        if self.velocity_x > 0:
            self.velocity_x -= 0.1  # Giảm tốc độ dương
        elif self.velocity_x < 0:
            self.velocity_x += 0.1  # Giảm tốc độ âm
        if abs(self.velocity_x) < 0.1:
            self.velocity_x = 0  # Đảm bảo tốc độ không trở thành số âm nhỏ
        
        # Kiểm tra không cho khối vuông đi ra ngoài màn hình bên trái
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity_x = 0  # Đặt tốc độ thành 0 nếu chạm cạnh bên trái của màn hình

# Khởi tạo khối vuông đỏ
red_square = RedSquare(100, 300)

# Vòng lặp chính
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Cập nhật vị trí của khối vuông đỏ và vẽ lại màn hình
    red_square.update()
    screen.fill(BLACK)
    red_square.draw()
    pygame.display.flip()

    # Đặt FPS
    clock.tick(60)

# Kết thúc Pygame khi kết thúc ứng dụng
pygame.quit()
sys.exit()
