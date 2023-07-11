import traceback
from read_json import ReadJson


class NewBalanceEntry:
    def __init__(self, symbol):
        self.symbol = symbol
        data = ReadJson().readbalancefile()
        new_entry = {
            "purchase_price": 0,
            "crypto_units": 0,
            "exchange_rate": 0.0,
            "prediction_label": " ",
            "buy_sell": 0,
            "current_account_value": 0.0,
            "current_account_profit": 0.0,
            "crypto_current_total_price": 0,
            "crypto_total_purchase_price": 0.0,
            "profit": 0.0,
            "current_price": 0.0,
            "accuracy": 0.0,
            "trend_label": " ",
            "last_roc": 0.0,
            "account_id": "",
        }

        data[self.symbol] = new_entry
        ReadJson().writebalancefile(data)
