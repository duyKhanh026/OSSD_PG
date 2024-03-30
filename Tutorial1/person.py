class Person(object):
	address = "123 Street"
	"""docstring for Person"""
	def __init__(self, name, age):
		self.name= name
		self.age= age

	@classmethod
	def changeAddress(cls, newAddress):
		cls.address = newAddress
		
class ExClass(object):
	astatic_dat = 'lop OSSD'

	@staticmethod
	def update_static_data(newData):
		ExClass.static_data = newData

ex_obj = ExClass()

ex_obj.update_static_data('dfdf')

print(ex_obj.static_data)
		