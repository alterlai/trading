from .abstract_algorithm import AbstractAlgorithm

class MACDCrossover(AbstractAlgorithm):

	def __init__(self, account):
		self.stop_loss = None
		self.take_profit1 = None
		self.take_profit2 = None
		self.account = account

	def make_descision(self, data):
		previous_macd = data['macd'][len(data) -2]
		current_macd = data['macd'][len(data) -1]
		previous_macd_signal = data['macd_signal'][len(data) -2]
		current_macd_signal = data['macd_signal'][len(data) -1]
		current_price = data['close'][len(data) -1]

		if self.stop_loss is None:
			self.stop_loss = data['bb_lb'][len(data) -1]
			self.take_profit1 = (1 + (100 - (100 * self.stop_loss / current_price)) / 100) * current_price
			self.take_profit2 = (1 + (1.5 * (100 - (100 * self.stop_loss / current_price)) / 100)) * current_price

		if current_macd != "nan":
			if current_macd > current_macd_signal and previous_macd <= previous_macd_signal:
				return ('buy', 1)
			elif current_price < self.stop_loss:
				return ('sell', 1)

			# if current_price >= self.take_profit1:
			# 	coins_to_sell = self.account.get_tp1_value() / current_price
			# 	return ('sell', )

