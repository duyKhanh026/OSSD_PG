from offline_2player import *
# from vsAImode import Vs_AI_Mode
from client import Player_client
from AI_OSSD.agent import train
from GUI.Menu import Menu
from GUI.Lobby import WaitingRoom
import json

class Main: 
    def __init__(self, name_character):
        self.name_character = name_character

    def run(self):
<<<<<<< HEAD
        menu = Menu(self.name_character)
=======
        menu = Menu()
        lobby = None
>>>>>>> 4de311d66f4c0e8b56a562fd3383c28d1c0c0a44
        while True:
            menu.run()
            if menu.play_option == 1:
                train()
            if menu.play_option == 2:
                offline_2player = Offline_2player(menu.screen)
                while offline_2player.retrunMenu == -1:
                    offline_2player.run()
            if menu.play_option == 3:
                lobby = WaitingRoom(menu.screen)
                # Player_client().run()
                while lobby.option != 3:
                    lobby.run()
                lobby.client_socket.sendall(json.dumps("!DISCONNECT").encode())
                lobby.option = -1
            menu.play_option = -1

if __name__ == "__main__":
    # train()
    Main().run()
    # Offline_2player().start()
    # offline_2player = Offline_2player()
    # lobby = WaitingRoom(offline_2player.screen)
    # while lobby.option != 3:
    #     lobby.run()ădưdwada