import pygame
import random
import torch
import torch.nn as nn
import torch.optim as optim




# Lớp mạng nơ-ron AI
class AI(nn.Module):
    def __init__(self):
        super(AI, self).__init__()
        self.fc1 = nn.Linear(2, 64)
        self.fc2 = nn.Linear(64, 2)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Hàm kiểm tra va chạm
def check_collision(player_pos, reward_pos):
    return player_pos.colliderect(reward_pos)

# Hàm huấn luyện mô hình AI
def train(model, optimizer, criterion, num_episodes=100):

    pos_ran = 10
    for episode in range(num_episodes):
        # Khởi tạo trạng thái ban đầu
        pygame.init()
        SCREEN_WIDTH = 400
        SCREEN_HEIGHT = 300
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Khởi tạo vị trí của người chơi và điểm
        player_pos = pygame.Rect(200, 250, 20, 20)
        reward_pos = pygame.Rect(pos_ran, 250, 20, 20)
        clock = pygame.time.Clock()
        player_x = player_pos.x - reward_pos.x
        player_y = player_pos.y - reward_pos.y
        state = torch.tensor([player_x, player_y], dtype=torch.float32).unsqueeze(0)
        
        # Khởi tạo tổng reward cho mỗi episode
        total_reward = 0
        
        # Khởi tạo trạng thái kết thúc trò chơi
        game_over = False
        
        while not game_over:
            # Lựa chọn hành động dựa trên trạng thái hiện tại và mô hình AI
            action = model(state)
            
            # Di chuyển người chơi dựa trên hành động được chọn
            if action.argmax().item() == 0:
                player_pos.x += 5
            else:
                player_pos.x -= 5
            
            # Tính reward và kiểm tra trạng thái kết thúc trò chơi
            if check_collision(player_pos, reward_pos):
                reward = 1
                game_over = True
            elif player_pos.x <= 0 or player_pos.x >= SCREEN_WIDTH:
                reward = -1
                game_over = True
            else:
                reward = 0
                
            # Cập nhật tổng reward
            total_reward += reward
            
            # Tính loss và cập nhật mô hình AI
            optimizer.zero_grad()
            loss = criterion(action, torch.tensor([[reward]], dtype=torch.float32))
            loss.backward()
            optimizer.step()
            
            # Cập nhật trạng thái mới
            player_x = player_pos.x - reward_pos.x
            player_y = player_pos.y - reward_pos.y
            state_new = torch.tensor([player_x, player_y], dtype=torch.float32).unsqueeze(0)
            state = state_new
            
            # Vẽ trạng thái mới của trò chơi
            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, (255, 0, 0), player_pos)
            pygame.draw.rect(screen, (0, 255, 0), reward_pos)
            pygame.display.flip()
            clock.tick(60)

        print(f"Episode {episode}, Total Reward: {total_reward}")

# Khởi tạo mô hình AI, optimizer và hàm mất mát
model = AI()
optimizer = optim.SGD(model.parameters(), lr=0.001)
criterion = nn.MSELoss()


# Huấn luyện mô hình AI
train(model, optimizer, criterion)
