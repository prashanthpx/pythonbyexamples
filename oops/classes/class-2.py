class Person:
	def __init__(self, name):
		self.name = name
	def talk(self):
		# name can be referenced anywhere using self.name
		print(f"Hi, i am {self.name}")


per = Person("John")
per.talk()