from offline_2player import *
import socket
import json

class Player_client:
    def __init__(self, client, screen,  p1='', p2=''):
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.HEADER = 4096
        self.client = client
        self.game = Offline_2player(screen, p1, p2)

    def send(self, msg):
        try:
            self.client.sendall(json.dumps("pler/" + msg).encode())
            remessage = self.client.recv(4096).decode()
            print(remessage)
            if not remessage == 'NOPLAY':
                self.game.player2.from_string(remessage)
        except Exception as e:
            print("Error:", e)

    def run(self):
        while True:
            self.game.run(None, True)
            self.send(str(self.game.player1))

        self.send(self.DISCONNECT_MESSAGE)

    # def __init__(self, server_ip="127.0.0.1", port=5050):
    #     self.SERVER = server_ip
    #     self.PORT = port
    #     self.FORMAT = 'utf-8'
    #     self.HEADER = 64
    #     self.DISCONNECT_MESSAGE = "!DISCONNECT"
    #     self.ADDR = (self.SERVER, self.PORT)

    #     self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.client.connect(self.ADDR)
    #     self.game = Offline_2player()

    # def send(self, msg):
    #     message = msg.encode(self.FORMAT)
    #     msg_length = len(message)
    #     send_length = str(msg_length).encode(self.FORMAT)
    #     send_length += b' ' * (self.HEADER - len(send_length))
    #     self.client.send(send_length)
    #     self.client.send(message)
    #     remessage = self.client.recv(4096).decode(self.FORMAT)
    #     if not remessage == 'NOPLAY':
    #         self.game.player2.from_string(remessage)
    #         print(remessage)

    
