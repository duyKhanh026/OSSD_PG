from offline_2player import Offline_2player
from vsAImode import Vs_AI_Mode
from client import Player_client

class Main:
    def run(self):
        while True:
            choice = input("Bạn muốn chạy trò chơi Offline (O) hay Player2_client (P)? Nhập O hoặc P: ").upper()
            if choice == "O":
                Offline_2player().start()
                break
            elif choice == "P":
                Player_client().run()
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng nhập lại.")

if __name__ == "__main__":
	Offline_2player().start()