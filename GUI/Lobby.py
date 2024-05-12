import pygame
import sys
import os
import time

class WaitingRoom:
    def __init__(self, surface):

        # Kích thước màn hình
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = surface.get_size()

        self.screen = surface
        self.default_font_size = 30
        self.font_path = "../Font/1FTV-Rexilya.otf"
        self.font_vietnamese = pygame.font.Font(self.font_path, self.default_font_size)

        # Tải hình ảnh nền
        self.background_image = pygame.image.load("background.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (self.SCREEN_WIDTH - 240, self.SCREEN_HEIGHT - 10))

        # Kích thước cửa sổ pygame
        self.window_width, self.window_height = surface.get_size()

        # Tính toán vị trí để cửa sổ xuất hiện ở giữa màn hình
        self.x_pos = (pygame.display.Info().current_w - self.window_width) // 2
        self.y_pos = (pygame.display.Info().current_h - self.window_height) // 2

        # Đặt vị trí cho cửa sổ
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{self.x_pos},{self.y_pos}"

        # Chọn font từ các font có sẵn trong hệ thống
        self.font_title = self.font_vietnamese = pygame.font.Font(self.font_path, 108)
        self.font_button = self.font_vietnamese = pygame.font.Font(self.font_path, 30)
        self.font_player = self.font_vietnamese = pygame.font.Font(self.font_path, 40)

        # Kích thước và màu sắc của nút
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 40
        self.BUTTON_MARGIN = 122  # Khoảng cách tăng giữa các nút
        self.BUTTON_COLOR = (255, 255, 255)  # Màu trắng cho nút
        self.BUTTON_TEXT_COLOR = (0, 0, 0)  # Màu đen cho chữ trên nút

        # Biến lưu trữ index của hàng được chọn
        self.selected_index = -1

        self.room_list = [
            {"name": "Người lái đò", "players": 1, "code": "ABC123"},
            {"name": "Chiến thắng Điện Biên Phủ", "players": 2, "code": "DEF456"},
            {"name": "Không thể kết thúc", "players": 1, "code": "GHI789"},
            {"name": "Quá mệt mỏi", "players": 2, "code": "JKL012"},
            {"name": "Solo ys", "players": 2, "code": "MNO345"},
            {"name": "Thua làm chóa", "players": 1, "code": "PQR678"},
            {"name": "1vs1", "players": 2, "code": "STU901"},
            {"name": "Ai win thì thua", "players": 1, "code": "VWX234"},
            {"name": "Nobody said yes", "players": 1, "code": "YZA567"},
            {"name": "*********", "players": 2, "code": "BCD890"},
            {"name": "Mật khẩu : 123", "players": 1, "code": "EFG123"},
            {"name": "Solo yasuoooooooooooooo", "players": 2, "code": "HIJ456"},
            {"name": "Rất là mệt nhé", "players": 1, "code": "KLM789"},
            {"name": "Cần tìm đối mạnh", "players": 2, "code": "NOP012"},
            {"name": "Siêu dự bị", "players": 1, "code": "QRS345"}
        ]  # Danh sách phòng mẫu

        self.scroll_pos = 0

        # Tính toán chiều cao của bảng
        self.table_height = self.SCREEN_HEIGHT - 155

        # Biến cờ để theo dõi trạng thái của việc nhấn chuột
        self.clicked = False

    # Hàm để vẽ một nút
    def draw_button(self, text, x, y):
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, (x, y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT), border_radius=20)
        text_surface = self.font_button.render(text, True, self.BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x + self.BUTTON_WIDTH // 2, y + self.BUTTON_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

    # Hàm để vẽ giao diện phòng chờ
    def draw_waiting_room(self):
        # Vẽ hình ảnh nền
        self.screen.blit(self.background_image, (0, 0))

        # Tiêu đề phòng chờ
        waiting_title = self.font_title.render("LOBBY", True, (255, 255, 255))
        title_rect = waiting_title.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 8))
        self.screen.blit(waiting_title, title_rect)

        # Tính toán kích thước của bảng
        table_width = self.SCREEN_WIDTH - 240

        # Vẽ bảng để hiển thị danh sách phòng
        table_rect = pygame.Rect(0, 150, table_width, self.table_height)
        pygame.draw.rect(self.screen, (255, 255, 255), table_rect, 2)  # Vẽ viền cho bảng

        # Tính toán số hàng hiển thị được
        num_visible_rows = min(self.table_height // 60, len(self.room_list))

        # Vẽ danh sách phòng dựa trên vị trí thanh cuộn
        start_index = self.scroll_pos
        end_index = min(self.scroll_pos + num_visible_rows, len(self.room_list))
        for i, room in enumerate(self.room_list[start_index:end_index], start=start_index):
            room_rect = pygame.Rect(table_rect.left + 10, table_rect.top + 10 + (i - start_index) * 60, table_width - 20, 50)

            # Kiểm tra xem chuột có hover trên hàng này không
            if room_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (220, 220, 220), room_rect)

            # Kiểm tra xem hàng này có phải là hàng được chọn không
            if self.selected_index == i:
                pygame.draw.rect(self.screen, (0, 255, 0), room_rect)  # Chọn màu xanh lá cây cho hàng được chọn

            # Vẽ thông tin phòng
            room_text_color = (255, 255, 255) if room['players'] < 2 else (150, 150, 150)  # Màu chữ phòng thay đổi khi có ít nhất 2 người chơi

            # Vẽ thông tin phòng
            room_name_text = self.font_vietnamese.render(f"Room {i+1}: {room['name']}", True, room_text_color)
            player_count_text = self.font_vietnamese.render(f"{room['players']} / 2", True, room_text_color)

            # Lấy kích thước của văn bản để tính toán vị trí
            room_name_text_rect = room_name_text.get_rect(left=room_rect.left , centery=room_rect.centery)
            player_count_text_rect = player_count_text.get_rect(right=room_rect.right - 10, centery=room_rect.centery)

            # Đặt khoảng cách giữa 2 phần văn bản là 10 pixel
            spacing = 10

            # Cập nhật vị trí của văn bản
            room_name_text_rect.width = room_rect.width * 1/3 - spacing
            player_count_text_rect.width = room_rect.width * 1/3 - spacing

            # Đặt vị trí của văn bản room_name_text ở bên trái của room_rect
            room_name_text_rect.right = room_name_text_rect.left + room_name_text_rect.width

            # Đặt vị trí của văn bản player_count_text ở bên phải của room_rect
            player_count_text_rect.left = player_count_text_rect.right - player_count_text_rect.width

            # Vẽ văn bản
            self.screen.blit(room_name_text, room_name_text_rect)
            self.screen.blit(player_count_text, player_count_text_rect)

            # Chỉ cho phép chọn phòng khi có ít hơn 2 người chơi
            if room['players'] < 2 and room_rect.collidepoint(pygame.mouse.get_pos()):
                # In ra id của hàng nếu chuột được click
                if pygame.mouse.get_pressed()[0]:  # Kiểm tra nút chuột trái được click hay không
                    print(f"Selected Room ID: {i+1}")
                    time.sleep(0.2)  # Chờ 0.2s trước khi nhận input tiếp theo
                    self.selected_index = i

        # Vẽ thanh cuộn
        scrollbar_rect = pygame.Rect(table_rect.right + 5, table_rect.top, 20, self.table_height)
        pygame.draw.rect(self.screen, (200, 200, 200), scrollbar_rect)
        # Tính toán vị trí và chiều cao của nút cuộn
        thumb_height = self.table_height / len(self.room_list) * num_visible_rows
        thumb_pos = self.scroll_pos / len(self.room_list) * self.table_height
        thumb_rect = pygame.Rect(scrollbar_rect.left + 5, scrollbar_rect.top + thumb_pos, 10, thumb_height)
        pygame.draw.rect(self.screen, (100, 100, 100), thumb_rect)

        # Vẽ nút
        self.draw_button("Join Room", 2.34 * (self.SCREEN_WIDTH // 3) + self.BUTTON_MARGIN, self.SCREEN_HEIGHT // 3)
        self.draw_button("Create Room", 2.34 * (self.SCREEN_WIDTH // 3) + self.BUTTON_MARGIN, self.SCREEN_HEIGHT // 3 + (self.BUTTON_HEIGHT + self.BUTTON_MARGIN))
        self.draw_button("Back", 2.34 * (self.SCREEN_WIDTH // 3) + self.BUTTON_MARGIN, self.SCREEN_HEIGHT // 3 + 2 * (self.BUTTON_HEIGHT + self.BUTTON_MARGIN))
        pygame.display.flip()

    # Hàm chính
    def run(self):
        # Biến cờ để theo dõi trạng thái của việc nhấn chuột
        clicked = False
        self.draw_waiting_room()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:  # Cuộn lên
                    if self.scroll_pos < len(self.room_list) - min(self.table_height // 60, len(self.room_list)):
                        self.scroll_pos = min(self.scroll_pos + 1, len(self.room_list) - min(self.table_height // 60, len(self.room_list)))
                elif event.button == 4:  # Cuộn xuống
                    if self.scroll_pos > 0:
                        self.scroll_pos = max(self.scroll_pos - 1, 0)
                # Xác định khi nào chuột được nhấn xuống lần đầu tiên
                clicked = True

        if clicked and not pygame.mouse.get_pressed()[0]:
            # Chờ 0.2s trước khi nhận input tiếp theo
            clicked = False


# Chạy trò chơi
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1500, 800))
    pygame.display.set_caption('LOBBY')
    game = WaitingRoom(screen)
    while True:
        game.run()
    