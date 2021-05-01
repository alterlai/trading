import json
import os
import random

import krakenex
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import requests
from pykrakenapi import KrakenAPI
from algorithms.random_rambo import RandomRambo
from technical_indicators_lib import indicators

from Account import Account

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
		ohlc, last = k.get_ohlc_data(pair, 240)
		ohlc['dtime'] = pd.to_datetime(ohlc['time']).apply(lambda x: x.date())
		print(f'saving data to file: {DATA_FILENAME}')
		ohlc.to_csv(DATA_FILENAME)
	else:
		ohlc = pd.read_csv(DATA_FILENAME)
	return ohlc


def simulate(data, figure):
	account = Account()
	action_chance = 1 # Actie kans is 5%
	balance = account.get_balance(0)
	algo = RandomRambo()

	for row in data.itertuples():
		# Laat het algoritme een beslissing maken.
		descision, ammount = algo.make_descision(data)
		if descision == "buy":
			account.buy('ETHUSDC', 1, row.close)
			figure.update_layout(
				title="buy indicator",
				shapes=[dict(x0=row.dtime, x1=row.dtime, y0=0, y1=1)]
			)
			print(f'Buying 1 ETHUSDC for: {row.close}')
		if descision == "sell":
			account.sell('ETHUSDC', 1, row.close)
			print(f'Selling 1 ETHUSDC for: {row.close}')
		else:
			print("Doing nothing.")
		data.loc[row.Index, 'balance'] = account.get_balance(row.close)
		data.loc[row.Index, 'coins'] = account.coins.get('ETHUSDC')
	return data


if __name__ == '__main__':
	ohlc = get_data("ETHUSDC")
	fig = make_subplots(rows=2, cols=2)
	fig.add_trace(
		go.Candlestick(x=ohlc.dtime,
			open=ohlc['open'],
			high=ohlc['high'],
			low=ohlc['low'],
			close=ohlc['close']
					   ),
		row=1, col=1
	)
	market_trace = {
		'x': ohlc.dtime,
		'open': ohlc['open'],
		'high': ohlc['high'],
		'low': ohlc['low'],
		'close': ohlc['close'],
		'name': 'ETHUSDC',
		'type': 'candlestick'
	}
	data = simulate(ohlc, fig)
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

	macd = indicators.MACD()
	data = macd.get_value_df(data)
	macd_trace = {
		'x': data.dtime,
		'y': data.MACD,
		'type': 'scatter',
		'mode': 'lines',
		'line': {
			'width': 1,
			'color': 'orange'
		},
		'name': 'MACD'
	}.
	print('hello')
	fig.update_layout(xaxis_rangeslider_visible=False)
	fig.add_trace(wallet_trace, row=1, col=2)
	fig.add_trace(macd_trace, row=2, col=1)
	fig.show()
	# balance_graph.show()
