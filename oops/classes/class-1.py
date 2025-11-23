# class name should be capitilized
class Point:
	def move(self):
		print("move")

	def draw(self):
		print("draw")


# creating an object aka instance of a class
# creating an object of Point class assigned to "point1"
# in Python, you absolutely can define class or instance attributes dynamically 
# after an object (or even the class itself) is created.
# Instance attributes → attached to one specific object
# Class attributes → attached to the class itself (shared across all instances)

point1 = Point()
point1.draw()

# attributes of class, assigning dynamically only to point1 object
point1.x = 10
point1.y = 20
print(point1.x)
print(point1.y)

point2 = point1
point2.x = 100
point2.y = 200
print(point2.x)
print(point2.y)
'''
When you write point2 = point1, Python does NOT create a new copy of the object. 
Instead, point2 becomes another reference (or "name") pointing to the same object 
in memory that point1 points to.
Changing point2.x and point2.y actually modifies the same object that point1 refers to
'''
print(point1.x)
print(point1.y)