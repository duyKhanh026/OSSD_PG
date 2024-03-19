import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Thiết lập màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite Animation")

# Tải ảnh và cắt thành các frame
list_img = []
for i in range(1, 13):
    img = pygame.image.load(f"assets/stickman_blade_slashed{i}.png")
    list_img.append(img)
idle_img = pygame.image.load("assets/stickman_blade_idle.png")


# Cài đặt thông số animation
frame_rate = 10  # Thay đổi tốc độ hiển thị frame thành mỗi 5fps là 1 frame
attack_count = 0
action_done = True  # Khởi tạo action_done là True để player ở trạng thái idle
time_since_last_frame = 0  # Biến đếm thời gian từ lần hiển thị frame trước đó

# Vòng lặp game
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((255, 255, 255))

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                attack_count += 1
                if attack_count > 3:
                    attack_count = 1
                action_done = False  # Đánh dấu action_done là False khi bắt đầu hành động mới

    # Kiểm tra xem action_done có True không, nếu có thì player ở trạng thái idle
    if action_done:
        screen.blit(idle_img, (100, 200))
    else:
        # Tính thời gian từ lần hiển thị frame trước đó
        time_since_last_frame += clock.get_time()

        # Hiển thị sprite animation dựa trên số lần nhấn phím E và thời gian đã trôi qua
        if attack_count == 1:
            frame_index = min(int(time_since_last_frame // (1000 / frame_rate)), 1)
        elif attack_count == 2:
            frame_index = min(int(time_since_last_frame // (1000 / frame_rate)), 2) + 1
        else:
            frame_index = min(int(time_since_last_frame // (1000 / frame_rate)), 6) + 3

        # Hiển thị frame tương ứng
        screen.blit(list_img[frame_index], (100, 100))

        # Kiểm tra xem đã hiển thị hết frame của hành động hiện tại chưa
        if frame_index >= 11:
            action_done = True  # Đánh dấu action_done là True khi hành động kết thúc
            time_since_last_frame = 0  # Đặt lại thời gian từ lần hiển thị frame trước đó về 0

    pygame.display.flip()
    clock.tick(60)

# Thoát Pygame
pygame.quit()
sys.exit()
