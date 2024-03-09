import pygame as py
from classes.player import Player  
from values.color import *
from values.screen import *

py.init()

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption('Demo')

player1 = Player(300, 350, RED, py.K_a, py.K_d, py.K_SPACE, 'L')
player2 = Player(800, 350, BLUE, py.K_LEFT, py.K_RIGHT, py.K_RCTRL, 'R')

run = True
clock = py.time.Clock()
while run:
    screen.fill(WHITE)
    
    line_spacing = 50  # Khoảng cách giữa các đường line
    for y in range(0, SCREEN_HEIGHT, line_spacing):
        py.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))
    line_spacing_vertical = 50
    for x in range(0, SCREEN_WIDTH, line_spacing_vertical):
        py.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    
    for player in [player1, player2]:
        player.draw(screen)
        player.move_logic(py.key.get_pressed())

    for event in py.event.get():
        if event.type == py.QUIT:
            run = False

    py.display.update()
    clock.tick(60)

py.quit()