import random

class RandomRambo:
	"""
	Random rambo maakt gewoon een random besluit of hij wil kopen of verkopen.
	:return: (string, ammount)
	string = "buy" of "sell"
	"""

	def __init__(self):
		self.action_chance = 1

	def make_descision(self, data):
		for row in data.itertuples():
			if random.randint(0, 100) <= self.action_chance:
				# If positive, buy, if negative, sell
				if random.randint(0, 1):
					data.loc[row.Index, 'action'] = ('buy', 1)
				else:
					data.loc[row.Index, 'action'] = ('sell', 1)
		return data
