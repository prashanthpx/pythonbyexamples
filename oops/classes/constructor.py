# class name should be capitalized
class Point:
	# constructor assigning values to x & y
	# They are called when an object is created
	# self refers to current object
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def move(self):
		print("move")

	def draw(self):
		print("draw")

point = Point(10, 20)
print(point.x)
print(point.y)

point.x = 100
point.y = 200
print(point.x)
print(point.y)

'''
output
10
20
100
200
'''