import pygame
import time

# Khởi tạo Pygame
pygame.init()

# Thiết lập màn hình
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Tải hình ảnh
image1 = pygame.image.load("assets/kill1.png")

# Vòng lặp game
running = True

# Tạo list để lưu trữ các biến hình
hinh_1_list = []

lengt = int(SCREEN_WIDTH / 50)

# Thêm 10 biến hình 1 vào list
for i in range(0, lengt):
    hinh_1_list.append(image1)

spam = False
clock = pygame.time.Clock()

spam_l = 0
frame_count = 0
frame_rate = 10

while running:

    # Vẽ màn hình
    screen.fill((255, 255, 255))
    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                spam_l = lengt

    # Vẽ hình 1
    for i in range(0, lengt - spam_l):
        screen.blit(hinh_1_list[i], (i * 50, SCREEN_HEIGHT - 150))

    # Cập nhật mỗi 10 fps
    frame_count += 1
    if frame_count == 3 and spam_l > 0 :
        spam_l -= 1

    if frame_count == 3:
        frame_count = 0

    pygame.display.update()
    print(str(frame_count))
    clock.tick(60)

# Thoát Pygame
pygame.quit()
