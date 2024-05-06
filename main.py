from offline_2player import Offline_2player
from vsAImode import Vs_AI_Mode
from client import Player_client
from AI_OSSD.agent import train
from GUI.Menu import Menu

class Main:
    def run(self):
        menu = Menu()
        while menu.play_option == -1: 
            menu.run()

if __name__ == "__main__": 
    Main().run()