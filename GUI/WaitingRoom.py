import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
screen_width = 1500
screen_height = 750

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)

# Font cho văn bản
font = pygame.font.Font(None, 24)
font_name = pygame.font.Font(None, 48)

# Tạo màn hình
screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Game Lobby")

# Tải hình nền
background_image = pygame.image.load("background_waitingroom.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
char1show = pygame.transform.scale(pygame.image.load("../assets/blue/stickman_blade_idle.png"), (640, 320))
char2show = pygame.transform.scale(pygame.image.load("../assets/purple_sp/stickman_idle1.png"), (640, 320))
char3show = pygame.transform.scale(pygame.image.load("../assets/black/stickman_blade_defense.png"), (640, 320))

# Class cho người chơi
class Player:
    def __init__(self, name, character):
        self.name = name
        self.character = character
        self.ready = False  # Trạng thái sẵn sàng của người chơi

# Class cho nhân vật
class Character:
    def __init__(self, name, image):
        self.name = name
        self.image = image

# Khởi tạo danh sách các nhân vật
characters = [
    Character("Character 1", char1show),
    Character("Character 2", char2show),
    Character("Character 3", char3show),
    # Thêm các nhân vật khác tại đây
]

# Danh sách người chơi
players = [
    Player("Yasou", None),
    Player("Leesin", None)
]

# Danh sách tin nhắn chat
chat_messages = []

# Tên phòng
room_name = "Room name: Solo kill"
room_name_x = (screen_width - font_name.size(room_name)[0]) // 2

# Biến lưu trữ nội dung tin nhắn đang nhập
input_text = ""

# Hàm vẽ giao diện
def draw_interface():
    button_y = 450
    # Vẽ hình nền
    screen.blit(background_image, (0, 0))

    # Vẽ tên phòng
    draw_text(room_name, font_name, WHITE, screen, room_name_x, 20)

    # Vẽ tên người chơi và các ô chọn nhân vật
    for i, player in enumerate(players):
        if player.name == "Yasou":
            draw_text(player.name, font_name, WHITE, screen, 150, 400)  # Điều chỉnh x và y tại đây
        elif player.name == "Leesin":
            draw_text(player.name, font_name, WHITE, screen, 1220, 400)  # Điều chỉnh x và y tại đây
        # pygame.draw.rect(screen, GRAY, (80 + i * 1100, 10, 260, 320))
        if player.character is not None:
            screen.blit(player.character.image, (-80 + i * 1100, 10))

    # Vẽ bảng chọn nhân vật
    for i, character in enumerate(characters):
        button_rect = pygame.Rect(520 + (i % 3) * 150, 100 + (i // 3) * 150, 120, 120)
        # pygame.draw.rect(screen, GRAY, button_rect)
        draw_text(character.name, font, WHITE, screen, 530 + (i % 3) * 150, 105 + (i // 3) * 150)
        character.button_rect = button_rect  # Lưu vị trí nút vào đối tượng nhân vật
        # Thu nhỏ hình ảnh nhân vật để vừa với nút
        scaled_image = pygame.transform.scale(character.image, (100, 100))
        image_x = button_rect.x + (button_rect.width - scaled_image.get_width()) // 2
        image_y = button_rect.y + (button_rect.height - scaled_image.get_height()) // 2
        screen.blit(scaled_image, (image_x, image_y))

    # Hiển thị đoạn chat
    chat_box_rect = pygame.Rect(20, 530, 1460, 150)
    pygame.draw.rect(screen, GRAY, chat_box_rect)

    # Hiển thị các tin nhắn chat
    for i, message in enumerate(chat_messages[-5:]):  # Hiển thị tối đa 5 tin nhắn cuối
        draw_text(message, font, WHITE, screen, 30, 540 + i * 30)

    # Vẽ hộp nhập liệu
    input_box_rect = pygame.Rect(20, 690, 1460, 40)
    pygame.draw.rect(screen, WHITE, input_box_rect)
    draw_text(input_text, font, BLACK, screen, 25, 700)

    # Vẽ nút Ready với bo tròn góc
    for i, player in enumerate(players):
        if player.name == "Yasou":
            ready_button_rect = pygame.Rect(150, 450, 100, 40)
        elif player.name == "Leesin":
            ready_button_rect = pygame.Rect(1220, 450, 100, 40)
        
        button_color = GREEN if player.ready else WHITE
        pygame.draw.rect(screen, button_color, ready_button_rect, border_radius=20)
        button_text = "All set" if player.ready else "Ready"
        draw_text(button_text, font, BLACK, screen, ready_button_rect.x + 10, ready_button_rect.y + 10)
        player.ready_button_rect = ready_button_rect  # Lưu vị trí nút vào đối tượng người chơi

# Hàm vẽ văn bản
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for i, character in enumerate(characters):
                if character.button_rect.collidepoint(mouse_pos):
                    players[0].character = characters[i]
            for player in players:
                if player.ready_button_rect.collidepoint(mouse_pos):
                    player.ready = not player.ready
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                chat_messages.append(input_text)
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    draw_interface()
    pygame.display.flip()

pygame.quit()
sys.exit()
