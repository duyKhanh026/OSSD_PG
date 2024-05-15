import socket
import json

class Room:
    def __init__(self, code, name, player):
        self.code = code
        self.name = name
        self.player = player

class RoomClient:
    def __init__(self, server_address=('127.0.0.1', 5050)):
        self.server_address = server_address
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)

    def create_room(self, room):
        try:
            # Gửi dữ liệu phòng tới server
            room_data = {
                "code": room.code,
                "name": room.name,
                "player": room.player
            }
            self.client_socket.sendall(json.dumps(room_data).encode())

            # Nhận phản hồi từ server
            response = self.client_socket.recv(4096).decode()
            print("Server response:", response)

        except Exception as e:
            print("Error:", e)

    def close_connection(self):
        self.client_socket.close()

# Sử dụng
if __name__ == "__main__":
    # Tạo một đối tượng RoomClient
    room_client = RoomClient()

    # Tạo một đối tượng Room
    room = Room("ABC123", "Room 1", 2)
    
    # Gọi phương thức create_room để gửi dữ liệu phòng tới server
    room_client.create_room(room)

    # Đóng kết nối
    room_client.close_connection()