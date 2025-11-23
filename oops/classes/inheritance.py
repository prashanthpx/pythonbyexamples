'''
class Dog:
	def walk(self):
		print("walk")

class Cat:
	def walk(self):
		print("walk")
# Here Dog and Cat has same method which is duplicated
'''

class Mammal:
	def walk(self):
		print("walk")

# Here Dog will inherit all methods from Mammal class
class Dog(Mammal):
	# To get over empty class as Python won't allow
	# So we use "pass"
	pass

class Cat(Mammal):
	pass


dog1 = Dog()
print(dog1.walk())
cat1 = Cat()
print(cat1.walk())
