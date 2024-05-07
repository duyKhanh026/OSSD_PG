from offline_2player import *
# from vsAImode import Vs_AI_Mode
from client import Player_client
# from AI_OSSD.agent import train
from GUI.Menu import Menu



class Main: 
    def run(self):
        offline_2player = Offline_2player()
        menu = Menu(offline_2player.screen)
        while menu.play_option == -1:
            menu.run()

        if menu.play_option == 2:
            offline_2player.start()
        if menu.play_option == 3:
            Player_client().run()

if __name__ == "__main__":
    Main().run()