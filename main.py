from offline_2player import *
# from vsAImode import Vs_AI_Mode
from client import Player_client
from AI_OSSD.agent import train
from GUI.Menu import Menu
from GUI.Lobby import WaitingRoom

class Main: 
    def run(self):
        offline_2player = Offline_2player()
        menu = Menu(offline_2player.screen)
        lobby = WaitingRoom(offline_2player.screen)
        while True:
            menu.run()
            print(menu.play_option)
            if menu.play_option == 2:
                offline_2player.start()
            if menu.play_option == 3: 
                Player_client().run()
                # while lobby.option != 3:
                #     lobby.run()
                # lobby.option = -1  
            menu.play_option = -1

if __name__ == "__main__":
    Main().run()
    # offline_2player = Offline_2player()
    # lobby = WaitingRoom(offline_2player.screen)
    # while lobby.option != 3:
    #     lobby.run()