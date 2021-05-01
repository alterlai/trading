

class Macd():

    def has_macd_up_cross(self, row):
        if data.macd > data.macd_signal and
            return True
        return False

    def has_macd_down_cross(self, row):
        pass

    def make_descision(self, data):
        # Even als voorbeeld
        # Als macd groter is dan 0, koop.
        if data.macd > data.macd_signal and data.close > data['200_ema'] and self.has_macd_up_cross():
            return 'buy', 1
        elif (data.macd < data.macd_signal) and data.close < data['200_ema'] and has_macd_up_cross = true:
            return 'sell', 1
        else:
            return 'sell', 1
