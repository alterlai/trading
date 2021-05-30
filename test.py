

import pandas as pd
from TradingRecord import TradingRecord

data = pd.DataFrame([1, 2, 3, 4, 5], columns=['a', 'b', 'c', 'd', 'e'])

TradingRecord.add_record(data, 200, 300, 150, "Stop los geraakt")
TradingRecord.add_record(data, 300, 500, 350, "Stop los geraakt 2")
print("klaar")