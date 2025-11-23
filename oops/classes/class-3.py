import random

class Dice:
	def roll(self):
		v1 = random.randint(1, 6)
		v2 = random.randint(1, 6)
		# It will be returned as tupple by default
		return v1, v2

d = Dice()
print(d.roll())