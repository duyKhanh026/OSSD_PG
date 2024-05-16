
class StringList:
    def __init__(self):
        # lưu pid của client 1101,1102 
        self.strings = []
        # Lưu thông số room dựa theo pid
        self.name = []
        #Thông số của nhân vật của client đó (dòng cuối player)
        self.coordinates = []
        #Nó là chủ phòng hay là khách mời
        self.player = []

    def add_string(self, s, information, roomconnect, pler):
        if s not in self.strings:
            self.strings.append(s)
            self.coordinates.append(pler)
            self.name.append(information)
            self.player.append(roomconnect)
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

    def __str__(self):
        # Tạo một chuỗi đại diện cho đối tượng Player
        user_info = [
            ','.join(self.strings),  # 0
            ','.join(self.player),  # 0
            ','.join(self.coordinates),  # 0
            ','.join(self.name)  # 1
        ]
        return ",".join(user_info)

    def from_string(self, user_info):
        # chuyển string lấy từ server thành giá trị cho player
        values = user_info.split(",")
        self.strings = values[0].split(',')
        self.player = values[1].split(',')
        self.coordinates = values[2].split(',')
        self.name = values[3].split(',')