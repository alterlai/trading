import json
import os
import random

import krakenex
import pandas as pd
import plotly.express as px
import plotly.subplots as subplots
import plotly.graph_objects as go
import requests
from pykrakenapi import KrakenAPI
from algorithms.random_rambo import RandomRambo

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


def simulate(data):
	account = Account()
	action_chance = 1 # Actie kans is 5%
	balance = account.get_balance()
	algo = RandomRambo()

	for row in data.itertuples():
		# Laat het algoritme een beslissing maken.
		descision, ammount = algo.make_descision(data)
		if descision == "buy":
			balance = account.buy('ETHUSDC', 1, row.close)
			print(f'Buying 1 ETHUSDC for: {row.close}')
		if descision == "sell":
			balance = account.sell('ETHUSDC', 1, row.close)
			print(f'Selling 1 ETHUSDC for: {row.close}')
		else:
			print("Doing nothing.")
		data.loc[row.Index, 'balance'] = balance
		data.loc[row.Index, 'coins'] = account.coins.get('ETHUSDC')
	return data


if __name__ == '__main__':
	ohlc = get_data("ETHUSDC")
	fig = go.Figure(
		data=[go.Candlestick(x=ohlc['dtime'],
		open=ohlc['open'],
		high=ohlc['high'],
		low=ohlc['low'],
		close=ohlc['close'])]
	)
	data = simulate(ohlc)
	balance_data = data[['dtime', 'balance']].copy()
	balance_graph = px.line(balance_data, x="dtime", y="balance", title="Balance graph")
	fig.show()
	balance_graph.show()
