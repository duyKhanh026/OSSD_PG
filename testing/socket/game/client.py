import socket
import pygame
import random

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.56.1"
ADDR = (SERVER, PORT)

P2x = 0
P2y = 0

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def get_coordinates_from_string(s):
	# Tách các giá trị số từ chuỗi
	coordinates = s.strip("()").split(", ")
	
	# Chuyển đổi các giá trị từ chuỗi thành số nguyên
	x = int(coordinates[0].strip("()"))
	y = int(coordinates[1].strip("()"))

	return x, y

def send(msg):
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' ' * (HEADER - len(send_length))
	client.send(send_length)
	client.send(message)
	remesage = client.recv(2048).decode(FORMAT)
	global P2x
	global P2y
	if not remesage == 'NOPLAY': 
		P2x, P2y = get_coordinates_from_string(remesage)
		print(remesage)

def main():
	pygame.init()
	screen = pygame.display.set_mode((500, 500))
	clock = pygame.time.Clock()

	# Starting position of the square
	x, y = random.randint(10, 300), random.randint(10, 300)
	speed = 5

	running = True
	while running:
		screen.fill((0, 0, 0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		keys = pygame.key.get_pressed()
		# Move the square based on arrow key inputs
		if keys[pygame.K_LEFT]:
			x -= speed
		if keys[pygame.K_RIGHT]:
			x += speed
		if keys[pygame.K_UP]:
			y -= speed
		if keys[pygame.K_DOWN]:
			y += speed

		# Draw the square
		pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, 50, 50))
		pygame.draw.rect(screen, (0,47,245), pygame.Rect(P2x, P2y, 50, 50))
		print(str(P2x) + ','+str(P2y))

		# Update the display
		pygame.display.flip()
		clock.tick(60)

		# Send the position of the square to the server
		send(f"{x},{y}")

	pygame.quit()
	send(DISCONNECT_MESSAGE)

if __name__ == "__main__":
	main()
