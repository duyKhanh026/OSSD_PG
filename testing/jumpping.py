import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Cài đặt kích thước màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Square Move')

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Kích thước khối vuông và vị trí ban đầu
SQUARE_SIZE = 50
square_x = SCREEN_WIDTH // 2
square_y = SCREEN_HEIGHT // 2
square_y_speed = 0
GRAVITY = 0.5
JUMP_POWER = -10

# Biến kiểm tra xem khối vuông có đang ở trên mặt đất hay không
on_ground = True

# Hàm vẽ khối vuông
def draw_square(x, y):
	pygame.draw.rect(screen, RED, (x, y, SQUARE_SIZE, SQUARE_SIZE))

# Vòng lặp chính
clock = pygame.time.Clock()
running = True
while running:
	screen.fill(WHITE)
	
	# Xử lý sự kiện
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				square_x -= 5
			elif event.key == pygame.K_d:
				square_x += 5
			elif event.key == pygame.K_SPACE and on_ground:  # Chỉ cho nhảy nếu đang ở trên mặt đất
				square_y_speed = JUMP_POWER
				on_ground = False
				
	# Áp dụng trọng lực
	square_y_speed += GRAVITY
	square_y += square_y_speed
	
	# Kiểm tra va chạm với mặt đất
	if square_y >= SCREEN_HEIGHT - SQUARE_SIZE:
		square_y = SCREEN_HEIGHT - SQUARE_SIZE
		square_y_speed = 0
		on_ground = True

	# Giới hạn không cho khối vuông đi quá biên
	if square_x < 0:
		square_x = 0
	elif square_x > SCREEN_WIDTH - SQUARE_SIZE:
		square_x = SCREEN_WIDTH - SQUARE_SIZE

	# Vẽ khối vuông
	draw_square(square_x, square_y)
	
	# Cập nhật màn hình
	pygame.display.update()
	clock.tick(60)

# Kết thúc Pygame
pygame.quit()
sys.exit()
