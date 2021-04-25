class Account():
	money = 10000
	coins = {
		'ETHUSDC': 0
	}

	def get_balance(self):
		return self.money

	def buy(self, coin, ammount, close_price):
		"""
		Koop een coin
		:param coin: De coin om te kopen.
		:param ammount: Ammount of coins om te kopen
		:return:
		"""
		usd_price = ammount * close_price
		if self.money - usd_price < 0:
			print(f"Niet genoeg geld om coins te kopen. Huidige bank balans: {self.money} USD")
			return self.money
		# Voeg de hoeveelheid coins toe
		self.coins[coin] = self.coins[coin] + ammount
		# Haal het geld van de bank balance.
		self.money = self.money - usd_price
		return self.money

	def sell(self, coin, ammount, close_price):
		"""
		Verkoop een coin.
		:param coin:
		:param ammount: Ammount of coinse to be sold
		:param close_price: current value of the coin
		:return:
		"""
		try:
			coin_balance = self.coins.get(coin)
			if coin_balance - ammount < 0:
				print(f'Niet genoeg coins om te verkopen. Huidige coin balance: {coin_balance}')
				return coin_balance
			# Haal de coins van de coin balance
			self.coins[coin] = self.coins[coin] - ammount
			# voeg bank balance toe
			self.money = self.money + ammount * close_price
			return self.money
		except Exception as e:
			print("Er ging iets fout. Waarschijnlijk bestaat deze coin niet in de wallet")
			print(e)