import pygame
import sys
import os

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
SCREEN_WIDTH = 994
SCREEN_HEIGHT = 705

# Khởi tạo cửa sổ
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighting Game")

# Tải hình ảnh nền
background_image = pygame.image.load("GUI/background.jpg")

# Kích thước cửa sổ pygame
window_width, window_height = pygame.display.get_surface().get_size()

# Tính toán vị trí để cửa sổ xuất hiện ở giữa màn hình
x_pos = (pygame.display.Info().current_w - window_width) // 2
y_pos = (pygame.display.Info().current_h - window_height) // 2

# Đặt vị trí cho cửa sổ
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x_pos},{y_pos}"

# Select a font from the available fonts in the system
font_title = pygame.font.SysFont("Arial", 72)
font_button = pygame.font.SysFont("Arial", 24)
font_player = pygame.font.SysFont("Arial", 24)

# Button dimensions and colors
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 40  # Increased margin between buttons
BUTTON_COLOR = (255, 255, 255)  # White color for buttons
BUTTON_TEXT_COLOR = (0, 0, 0)  # Black color for text on buttons

# Function to draw a button
def draw_button(text, x, y):
    pygame.draw.rect(screen, BUTTON_COLOR, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=20)
    text_surface = font_button.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + BUTTON_WIDTH // 2, y + BUTTON_HEIGHT // 2))
    screen.blit(text_surface, text_rect)

# Function to draw the menu interface
def draw_menu(player_name):
    # Draw background image
    screen.blit(background_image, (0, 0))

    # Game title
    game_title = font_title.render("Fighting Game", True, (255, 255, 255))
    title_rect = game_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(game_title, title_rect)
    # Player name
    player_text = font_player.render(player_name, True, (255, 255, 0))
    player_rect = player_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
    screen.blit(player_text, player_rect)
    # Draw buttons
    draw_button("Play with Bot", (SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 2)
    draw_button("Play 2 Players", (SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_MARGIN)
    draw_button("Play Online", (SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 2 + 2 * (BUTTON_HEIGHT + BUTTON_MARGIN))
    pygame.display.flip()

# Main function
def main():
    player_name = "Player 1"  # Default player name
    while True:
        draw_menu(player_name)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check which button the player clicked
                if (SCREEN_WIDTH - BUTTON_WIDTH) // 2 <= mouse_x <= (SCREEN_WIDTH - BUTTON_WIDTH) // 2 + BUTTON_WIDTH:
                    if SCREEN_HEIGHT // 2 <= mouse_y <= SCREEN_HEIGHT // 2 + BUTTON_HEIGHT:
                        print("Play with Bot")
                    elif SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_MARGIN <= mouse_y <= SCREEN_HEIGHT // 2 + 2 * (BUTTON_HEIGHT + BUTTON_MARGIN):
                        print("Play 2 Players")
                    elif SCREEN_HEIGHT // 2 + 2 * (BUTTON_HEIGHT + BUTTON_MARGIN) <= mouse_y <= SCREEN_HEIGHT // 2 + 3 * (BUTTON_HEIGHT + BUTTON_MARGIN):
                        print("Play Online")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    # Change player name when 'n' key is pressed
                    player_name = input("Enter player name: ")

# Run the game
if __name__ == "__main__":
    main()
