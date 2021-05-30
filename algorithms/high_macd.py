from .abstract_algorithm import AbstractAlgorithm


class HighMACD(AbstractAlgorithm):
	"""
	Dit algoritme kijkt naar MACD. Als hij hoger is dan 1 probeert hij te kopen, als het lager is verkoopt hij.
	"""
	def __init__(self, account):
		self.account = account

	def make_descision(self, data):
		if data['macd'][len(data) -1] != "nan" and data['macd'][len(data) -1] > 0:
			return ('buy', 1)
		else:
			return('sell', 1)
