import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

class StringList:
	def __init__(self):
		self.strings = []
		self.coordinates = []

	def add_string(self, s, x=None, y=None):
		if s not in self.strings:
			self.strings.append(s)
			self.coordinates.append((x, y))
			print(f"String '{s}' with coordinates ({x}, {y}) added to the list.")
		else:
			index = self.strings.index(s)
			self.coordinates[index] = (x, y)
			print(f"String '{s}' coordinates updated to ({x}, {y}).")

	def contains_string(self, s):
		return s in self.strings

	def get_coordinate(self, s):
		if len(self.strings) < 2:
			return "NOPLAY"
		else:
			for i, string in enumerate(self.strings):
				if string != s:
					return self.coordinates[i]
			return "String not found"


my_string_list = StringList()


def handle_client(conn, addr):
	print("[NEW CONNECTION] {addr} connected.")

	connected = True
	while connected:
		msg_length = conn.recv(HEADER).decode(FORMAT)
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(FORMAT)
			if msg == DISCONNECT_MESSAGE:
				connected = False

			print(f"[{addr}] {msg}")
			senback = "NOPLAY"
			if connected:
				my_string_list.add_string(str(get_portt(addr)), convert_to_coordinate(msg))
				senback = my_string_list.get_coordinate(str(get_portt(addr)))
			conn.send(str(senback).encode(FORMAT))

	conn.close()

def get_portt(adr):
	return adr[1]
def convert_to_coordinate(string):
	x_str, y_str = string.split(',')
	x = int(x_str)
	y = int(y_str)
	return x, y

def start():
	server.listen()
	print(f"[LISTENING] Server is listening on {SERVER}")
	while True:
		conn, addr = server.accept()
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()