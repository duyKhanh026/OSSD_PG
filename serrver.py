import json
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
		# lưu pid của client 1101,1102 
		self.strings = []
		# Lưu thông số room dựa theo pid
		self.information = []
		#Thông số của nhân vật của client đó (dòng cuối player)
		self.coordinates = []
		#Nó là chủ phòng hay là khách mời
		self.roomconnect = None

	def add_string(self, s, pler):
		if s not in self.strings:
			self.strings.append(s)
			self.coordinates.append(pler)
			# print(f"String '{s}' with coordinates {pler}.")
		else:
			index = self.strings.index(s)
			self.coordinates[index] = pler
			# print(f"String '{s}' coordinates updated to {pler}.")

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

			# print(f"[{addr}] {msg}")
			senback = "NOPLAY"
			if connected:
				my_string_list.add_string(str(get_portt(addr)), msg)
				senback = my_string_list.get_coordinate(str(get_portt(addr)))
			conn.send(str(senback).encode(FORMAT))

	conn.close()

	import json

def handle_room_client(conn, addr):
    print(f"[NEW ROOM CONNECTION] {addr} connected.")

    connected = True
    while connected:
        # Nhận dữ liệu từ client room
        msg = conn.recv(4096).decode(FORMAT)
        if msg:
            # Hiển thị dữ liệu nhận được từ client room
            print(f"[{addr}] Sent message: {msg}")

            # Xử lý dữ liệu JSON
            try:
                data = json.loads(msg)
                # Thực hiện xử lý dữ liệu của room
                handle_room_data(data)
            except json.JSONDecodeError as e:
                print(f"[ERROR] Invalid JSON format: {e}")

    conn.close()

def handle_room_data(data):
    # Xử lý dữ liệu của room ở đây
    # Ví dụ:
    room_code = data.get("code")
    room_name = data.get("name")
    room_player = data.get("player")
    print(f"Room Code: {room_code}, Name: {room_name}, Player: {room_player}")
    # Thực hiện các thao tác khác tùy thuộc vào dữ liệu nhận được



def get_portt(adr):
	return adr[1]

def start():
	server.listen()
	print(f"[LISTENING] Server is listening on {SERVER}")
	while True:
		conn, addr = server.accept()
		# thread = threading.Thread(target=handle_room_client, args=(conn, addr))
		# thread.start()
		thread1= threading.Thread(target=handle_client, args=(conn, addr))
		thread1.start()
		
		print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()

# def start():
#     server.listen()
#     print(f"[LISTENING] Server is listening on {SERVER}")
#     while True:
#         conn, addr = server.accept()
#         client_type = conn.recv(HEADER).decode(FORMAT)
#         if client_type == "client":
#             threading.Thread(target=handle_client, args=(conn, addr)).start()
#         elif client_type == "room":
#             threading.Thread(target=handle_room_client, args=(conn, addr)).start()
#         else:
#             print(f"Unknown client type from {addr}")
#             conn.close()

#         print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

# print("[STARTING] server is starting...")
# start()
