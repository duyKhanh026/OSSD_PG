import pygame as py
import numpy as np
import random
from classes.player import Player
from classes.character1 import Character1
from classes.character2 import Character2
from collections import namedtuple
from classes.action import *
from values.color import *
from values.screen import *


class BattleGameAI:
	
    def __init__(self):
        py.init()
        self.reset()




    def reset(self):
        self.count_frame = 0
        self.game_over = False
        self.screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        py.display.set_caption('Demo')
        self.point = self.random_point()
        self.player1 = Character1(200, 50, 'blue/stickman_blade', self.point[0], self.point[1], RED, py.K_a, py.K_d, py.K_w, py.K_g, py.K_h, py.K_j, py.K_e, 'L')
        self.player2 = Character2(200, 80, 'purple/stickman', 1200, 150, BLUE, py.K_LEFT, py.K_RIGHT, py.K_UP, py.K_KP1, py.K_KP2, py.K_KP3, py.K_KP4, 'R')
        self.player1.name = 'player1'
        self.player2.name = 'player2'
        self.clock = py.time.Clock()
        bg = py.image.load(f'assets/bg2.jpg')
        self.bg1 = py.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.score = 0
        self.hitpoint = False





    def random_point(self):
        x = random.randint(180, SCREEN_WIDTH - 300)

        y = random.randint(200, SCREEN_HEIGHT // 2)

        return [x, y]
    


    def _update_ui(self):
        self.screen.fill(BLACK)
        py.draw.rect(self.screen, (157,157,157), py.Rect(200, 600, SCREEN_WIDTH - 400, SCREEN_HEIGHT))
        # vẽ sọc trắng lên màn hình
        line_spacing = 50
        for y in range(0, SCREEN_HEIGHT, line_spacing):
            py.draw.line(self.screen, WHITE, (0, y), (SCREEN_WIDTH, y))
        line_spacing_vertical = 50
        for x in range(0, SCREEN_WIDTH, line_spacing_vertical):
            py.draw.line(self.screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))

        # self.screen.blit(self.bg1, (0,0))

        # xữ lý đầu vào để di chuyển và thực hiện hành động cho nhân vật 
        for player in [self.player2]:
            player.move_logic(py.key.get_pressed())
            player.sp_move(py.key.get_pressed())

            if player.state == 'ATK' or player.state == 'KIC':
                if player.attack_cooldown_p1 == 0:
                    player.attack_cooldown_p1 = ATTACK_COOLDOWN
                    player.attack_ready_p1 = False

        if self.player1.skill_active(self.screen, self.player2):
            handle_attack(None, self.player2)
            self.pushed_side(self.player1, self.player2)

        self.attack_confirmation(self.player1, 10, 30)
        self.attack_confirmation(self.player2, SCREEN_WIDTH - 110, 30)

        self.player_attack(self.player1, self.player2)
        if self.player_attack(self.player2, self.player1):
            self.score += 1
            self.hitpoint = True

        self.player_kick(self.player1, self.player2)
        self.player_kick(self.player2, self.player1)

        self.stunning_confirmation(self.player1, 10, 50)
        self.stunning_confirmation(self.player2, SCREEN_WIDTH - 110, 50)

        self.kicked_confirmation(self.player1, 10, 80)
        self.kicked_confirmation(self.player2, SCREEN_WIDTH - 110, 80)




def move_player(self, action):
        if np.array_equal(action, [1, 0, 0, 0]) and self.player2.state != 'ATK':
            self.player2.go_left()
        elif np.array_equal(action, [0, 1, 0, 0]) and self.player2.state != 'ATK':
            self.player2.go_right()
        elif np.array_equal(action, [0, 0, 1, 0]):
            self.player2.do_atk()
        elif self.player2.on_ground:
            self.player2.do_jump()

    