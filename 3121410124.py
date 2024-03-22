class Map:
    def __init__(self, list):
        self.list = list

    def mapAdd(self, value):
        self.list.append(value)

class MapSubClass(Map):
    def __init__(self, list):
        super().__init__(list)  # Call the parent class constructor

    def mapAdd(self, keys, values):
        """Adds key-value pairs to the internal list as tuples."""
        for key, value in zip(keys, values):
            self.list.append((key, value))

def main():
    number_list = [6,8,3,6,9]
    map_instance = Map(number_list)
    print("Map List =", map_instance.list)

    keys = ['one','two','three']
    map_subclass_instance = MapSubClass([])
    map_subclass_instance.mapAdd(keys, values)
    print("MapSubClass list:",map_subclass_instance.list)

if __name__ =="__main__":
    main()
