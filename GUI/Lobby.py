import pygame
import sys
import os
import time

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
SCREEN_WIDTH = 994
SCREEN_HEIGHT = 705

# Khởi tạo cửa sổ
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Waiting Room")

# Tải hình ảnh nền
background_image = pygame.image.load("GUI/background.jpg")

# Kích thước cửa sổ pygame
window_width, window_height = pygame.display.get_surface().get_size()

# Tính toán vị trí để cửa sổ xuất hiện ở giữa màn hình
x_pos = (pygame.display.Info().current_w - window_width) // 2
y_pos = (pygame.display.Info().current_h - window_height) // 2

# Đặt vị trí cho cửa sổ
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x_pos},{y_pos}"

# Chọn font từ các font có sẵn trong hệ thống
font_title = pygame.font.SysFont("Arial", 72)
font_button = pygame.font.SysFont("Arial", 24)
font_player = pygame.font.SysFont("Arial", 24)

# Kích thước và màu sắc của nút
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 122  # Khoảng cách tăng giữa các nút
BUTTON_COLOR = (255, 255, 255)  # Màu trắng cho nút
BUTTON_TEXT_COLOR = (0, 0, 0)  # Màu đen cho chữ trên nút

# Biến lưu trữ index của hàng được chọn
selected_index = -1

# Hàm để vẽ một nút
def draw_button(text, x, y):
    pygame.draw.rect(screen, BUTTON_COLOR, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=20)
    text_surface = font_button.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + BUTTON_WIDTH // 2, y + BUTTON_HEIGHT // 2))
    screen.blit(text_surface, text_rect)

# Hàm để vẽ giao diện phòng chờ
def draw_waiting_room(room_list, scroll_pos, table_height):
    global selected_index
    
    # Vẽ hình ảnh nền
    screen.blit(background_image, (0, 0))

    # Tiêu đề phòng chờ
    waiting_title = font_title.render("LOBBY", True, (255, 255, 255))
    title_rect = waiting_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
    screen.blit(waiting_title, title_rect)
    
    # Tính toán kích thước của bảng
    table_width = SCREEN_WIDTH - 240

    # Vẽ bảng để hiển thị danh sách phòng
    table_rect = pygame.Rect(0, 150, table_width, table_height)
    pygame.draw.rect(screen, (255, 255, 255), table_rect, 2)  # Vẽ viền cho bảng

    # Tính toán số hàng hiển thị được
    num_visible_rows = min(table_height // 60, len(room_list))

    # Vẽ danh sách phòng dựa trên vị trí thanh cuộn
    start_index = scroll_pos
    end_index = min(scroll_pos + num_visible_rows, len(room_list))
    for i, room in enumerate(room_list[start_index:end_index], start=start_index):
        room_rect = pygame.Rect(table_rect.left + 10, table_rect.top + 10 + (i - start_index) * 60, table_width - 20, 50)
        

        # Kiểm tra xem chuột có hover trên hàng này không
        if room_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (220, 220, 220), room_rect)
        
        # Kiểm tra xem hàng này có phải là hàng được chọn không
        if selected_index == i:
            pygame.draw.rect(screen, (0, 255, 0), room_rect)  # Chọn màu xanh lá cây cho hàng được chọn
        
        # Vẽ thông tin phòng
        room_text = font_button.render(f"Room {i+1}: {room['name']} ({room['players']} players)", True, (255, 255, 255))
        room_text_rect = room_text.get_rect(left=room_rect.left + 10, centery=room_rect.centery)
        screen.blit(room_text, room_text_rect)

        if room_rect.collidepoint(pygame.mouse.get_pos()):
            # In ra id của hàng nếu chuột được click
            if pygame.mouse.get_pressed()[0]:  # Kiểm tra nút chuột trái được click hay không
                print(f"Selected Room ID: {i+1}")
                time.sleep(0.2)  # Chờ 0.2s trước khi nhận input tiếp theo
                selected_index = i

    # Vẽ thanh cuộn
    scrollbar_rect = pygame.Rect(table_rect.right + 5, table_rect.top, 20, table_height)
    pygame.draw.rect(screen, (200, 200, 200), scrollbar_rect)
    # Tính toán vị trí và chiều cao của nút cuộn
    thumb_height = table_height / len(room_list) * num_visible_rows
    thumb_pos = scroll_pos / len(room_list) * table_height
    thumb_rect = pygame.Rect(scrollbar_rect.left + 5, scrollbar_rect.top + thumb_pos, 10, thumb_height)
    pygame.draw.rect(screen, (100, 100, 100), thumb_rect)

    # Vẽ nút
    draw_button("Join Room", 2 * (SCREEN_WIDTH // 3) + BUTTON_MARGIN, SCREEN_HEIGHT // 3)
    draw_button("Create Room", 2 * (SCREEN_WIDTH // 3) + BUTTON_MARGIN, SCREEN_HEIGHT // 3 + (BUTTON_HEIGHT + BUTTON_MARGIN))
    draw_button("Back", 2 * (SCREEN_WIDTH // 3) + BUTTON_MARGIN, SCREEN_HEIGHT // 3 + 2 * (BUTTON_HEIGHT + BUTTON_MARGIN))
    pygame.display.flip()

# Hàm chính
def main():
    room_list = [
        {"name": "Room 1", "players": 1, "code": "ABC123"},
        {"name": "Room 2", "players": 2, "code": "DEF456"},
        {"name": "Room 3", "players": 1, "code": "GHI789"},
        {"name": "Room 4", "players": 3, "code": "JKL012"},
        {"name": "Room 5", "players": 2, "code": "MNO345"},
        {"name": "Room 6", "players": 1, "code": "PQR678"},
        {"name": "Room 7", "players": 2, "code": "STU901"},
        {"name": "Room 8", "players": 1, "code": "VWX234"},
        {"name": "Room 9", "players": 1, "code": "YZA567"},
        {"name": "Room 10", "players": 2, "code": "BCD890"},
        {"name": "Room 11", "players": 1, "code": "EFG123"},
        {"name": "Room 12", "players": 2, "code": "HIJ456"},
        {"name": "Room 13", "players": 1, "code": "KLM789"},
        {"name": "Room 14", "players": 2, "code": "NOP012"},
        {"name": "Room 15", "players": 1, "code": "QRS345"}
    ]  # Danh sách phòng mẫu

    scroll_pos = 0

    # Tính toán chiều cao của bảng
    table_height = SCREEN_HEIGHT - 155
    
    # Biến cờ để theo dõi trạng thái của việc nhấn chuột
    clicked = False

    while True:
        draw_waiting_room(room_list, scroll_pos, table_height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:  # Cuộn lên
                    if scroll_pos < len(room_list) - min(table_height // 60, len(room_list)):
                        scroll_pos = min(scroll_pos + 1, len(room_list) - min(table_height // 60, len(room_list)))
                elif event.button == 4:  # Cuộn xuống
                    if scroll_pos > 0:
                        scroll_pos = max(scroll_pos - 1, 0)
                # Xác định khi nào chuột được nhấn xuống lần đầu tiên
                clicked = True
        
        if clicked and not pygame.mouse.get_pressed()[0]:
            time.sleep(0.2)  # Chờ 0.2s trước khi nhận input tiếp theo
            clicked = False


# Chạy trò chơi
if __name__ == "__main__":
    main()


