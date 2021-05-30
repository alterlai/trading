import pandas as pd

columns = ['take_profit1', 'take_profit2', 'stop_los' 'label', 'data']

class TradingRecord:
	data = pd.DataFrame(columns=columns)

	@staticmethod
	def add_record(data, take_profit1, take_profit2, stop_los, label):
		new_df = pd.DataFrame(columns=columns)
		new_df.take_profit1 = take_profit1
		new_df.take_profit2 = take_profit2
		new_df.stop_los = stop_los,
		new_df.label = label
		new_df.data = data
		data.append(new_df)
