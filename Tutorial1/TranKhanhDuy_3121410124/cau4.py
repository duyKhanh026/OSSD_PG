class Map:
	def __init__(self, number):
		self.list = []
		self.__mapAdd(number)

	def __mapAdd(self, number):
		for item in number:
			self.list.append(item)

class MapSubclass(Map):
	def mapAdd(self, keys, number):
		if len(keys) < len(number):
			for i in range(0, len(number) - len(keys)):
				keys.append("undefind_key_" + str(i))
		for i in zip(keys, number):
			self.list.append(i)

def main():
	number_list = [1, 2, 3, 4, 5]
	map_instance = Map(number_list)
	print(f"Map list = {map_instance.list}")

	keys = ['one', 'two', 'three']
	map_subclass_instance = MapSubclass([])
	map_subclass_instance.mapAdd(keys, number_list)
	print(f'MapSubClass list:\n {map_subclass_instance.list}')

if __name__ == "__main__":
	main()