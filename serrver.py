import socket
import threading
from classes.player import Player

HEADER = 64
PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

class StringList:
	def __init__(self):
		self.strings = []
		self.coordinates = []

	def add_string(self, s, pler):
		if s not in self.strings:
			self.strings.append(s)
			self.coordinates.append(pler)
			print(f"String '{s}' with coordinates {pler}")
		else:
			index = self.strings.index(s)
			self.coordinates[index] = pler
			print(f"String '{s}' coordinates updated to {pler}.")

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
	def remove_string(self, s):
		if s in self.strings:
			index = self.strings.index(s)
			del self.strings[index]
			del self.coordinates[index]
			print(f"String '{s}' and its coordinates removed from the list.")
		else:
			print(f"String '{s}' not found in the list.")


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
				my_string_list.remove_string(str(get_portt(addr)))
				connected = False

			print(f"[{addr}] {msg}")
			senback = "NOPLAY"
			if connected:
				my_string_list.add_string(str(get_portt(addr)), msg)
				senback = my_string_list.get_coordinate(str(get_portt(addr)))
			conn.send(str(senback).encode(FORMAT))

	conn.close()

def get_portt(adr):
	return adr[1]

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