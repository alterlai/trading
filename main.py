import json
import os

import krakenex
import pandas as pd
import plotly.graph_objects as go
import requests
from plotly.subplots import make_subplots
from pykrakenapi import KrakenAPI
from ta import add_all_ta_features
from ta.trend import ema_indicator
from ta.trend import macd, macd_signal
from ta.volatility import BollingerBands

from Account import Account
from algorithms.random_rambo import RandomRambo
from algorithms.high_macd import HighMACD

BASE_URL = "https://api.kraken.com/0/public/"
HEADERS = {
	'Accept': '*/*'
}
DATA_FILENAME = 'data.csv'


def make_request(method, url_extension, params=None, headers=None, files=None, json_data=None, auto_parse=True):
	"""
	Make a request to the API and return the repsonse content

	:param auto_parse: bool: Wether the response should be automatically parsed from json. Disable this for requests like filereponses.
	:param method: [string] HTTP method e.g. "POST", "GET"
	:param url_extension: [string] extension of the base url. e.g. incidents/
	:param params: [dict] parameters to be added to the request
	:param headers: [dict] headers to be added to the request
	:param files: [dict] files to be added to the request
	:param: json_data [dict] Body data.
	:return: [dict] response body

	"""
	url = BASE_URL + url_extension
	# get default headers if not set.
	if headers is None:
		headers = headers
	response = requests.request(method, url, params=params, headers=headers, files=files, json=json_data)
	if 200 <= response.status_code <= 299:
		if response.content:
			if auto_parse:
				return json.loads(response.content)
			else:
				return response
		else:
			return ""


def get_data(pair: str):
	if not os.path.exists(DATA_FILENAME):
		api = krakenex.API()
		k = KrakenAPI(api)
		data, last = k.get_ohlc_data(pair, 240)
		data['dtime'] = pd.to_datetime(data['time']).apply(lambda x: x.date())
		print(f'saving data to file: {DATA_FILENAME}')
		data.to_csv(DATA_FILENAME)
	data = pd.read_csv(DATA_FILENAME)
	data = data.sort_values(by='dtime')
	data.reset_index(inplace=True)
	data.drop('index', axis=1, inplace=True)
	# Add technical analysis features
	data = add_all_ta_features(data, open='open', high='high', low='low', close='close', volume='volume', fillna=False)
	# Bollinger bands
	indicators_bb = BollingerBands(close=data['close'], window=20, window_dev=2)

	data['bb_hb'] = indicators_bb.bollinger_hband()
	data['bb_lb'] = indicators_bb.bollinger_lband()
	data['macd'] = macd(data['close'])
	data['macd_signal'] = macd_signal(data['close'])
	data['200_ema'] = ema_indicator(data['close'], 200)

	return data


def add_line(figure, x0, x1, y0, y1, color, text):
	figure.add_trace(go.Scatter(
		x=[x0, x1],
		y=[y0, y1],
		mode="lines+text",
		name="Lines and Text",
		text=[f"{text}"],
		line= {
			'width': 1,
			'color': f'{color}'
		},
		textposition="bottom center"
	))


def simulate(data, figure):
	account = Account()
	algo = HighMACD()

	for row in data.itertuples():
		# Loop over alle data en geef deze aan het algoritme incl. historische data tot op dat punt.
		current_data = data[0:row.Index + 1] # Index + 1, zodat we de eerste rij pakken
		descision = algo.make_descision(current_data)
		# action kan ook niks zijn.
		if descision:
			if descision[0] == 'buy':
				data.loc[row.Index, 'action'] = ('buy')
				account.buy('ETHUSDC', 1, row.close)
				print(f'Buying 1 ETHUSDC for: {row.close}')
				# add_line(figure, row.dtime, row.dtime, 0, row.close+500, 'green', 'B')
			if descision[0] == "sell":
				data.loc[row.Index, 'action'] = ('sell')
				account.sell('ETHUSDC', 1, row.close)
				print(f'Selling 1 ETHUSDC for: {row.close}')
				# add_line(figure, row.dtime, row.dtime, 0, row.close+500, 'red', 'S')
		data.loc[row.Index, 'balance'] = account.get_balance(row.close)
		data.loc[row.Index, 'coins'] = account.coins.get('ETHUSDC')
	return data


if __name__ == '__main__':
	data = get_data("ETHUSDC")
	fig = make_subplots(rows=3, cols=1)
	fig.add_trace(
		go.Candlestick(x=data.dtime,
					   open=data['open'],
					   high=data['high'],
					   low=data['low'],
					   close=data['close']
					   ),
		row=1, col=1
	)



	data = simulate(data, fig)
	wallet_trace = {
		'x': data.dtime,
		'y': data.balance,
		'type': 'scatter',
		'mode': 'lines',
		'line' : {
			'width': 1,
			'color': 'blue'
		},
		'name': 'account balans'
	}

	bb_hb_trace = {
		'x': data.dtime,
		'y': data.bb_hb,
		'type': 'scatter',
		'mode': 'lines',
		'line': {
			'width': 1,
			'color': 'blue'
		},
		'name': 'Bollinger high band'
	}
	bb_lb_trace = {
		'x': data.dtime,
		'y': data.bb_lb,
		'type': 'scatter',
		'mode': 'lines',
		'line': {
			'width': 1,
			'color': 'blue'
		},
		'name': 'Bollinger low band'
	}


	fig2 = go.Figure()
	macd_trace = {
		'y': data['macd'],
		'x': data['dtime'],
		'type': 'scatter',
		'mode': 'lines',
		'name': 'MACD'
	}
	fig2.add_trace(macd_trace)

	# fig.update_layout(xaxis_rangeslider_visible=False)
	fig.add_trace(wallet_trace, row=3, col=1)
	fig.add_trace(bb_hb_trace, row=1, col=1)
	fig.add_trace(bb_lb_trace, row=1, col=1)
	fig.show()
	fig2.show()
	# balance_graph.show()
