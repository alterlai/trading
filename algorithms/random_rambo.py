import random

class RandomRambo:
	"""
	Random rambo maakt gewoon een random besluit of hij wil kopen of verkopen.
	:return: (string, ammount)
	string = "buy" of "sell"
	"""

	def __init__(self):
		self.action_chance = 5

	def make_descision(self, data):
		if random.randint(0, 100) <= self.action_chance:
			if random.randint(0,1) > 0.5:
				# If positive, buy, if negative, sell
				return ('buy', 1)
			else:
				return ('sell', 1)
