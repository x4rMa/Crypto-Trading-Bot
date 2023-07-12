from coinbase.wallet.client import Client

import traceback


class BuyOrSell:
    def __init__(self, apikey, apisecret, symbol):
        client = Client(apikey, apisecret)
        self.client = client
        self.symbol = symbol

        # Get the account id details
        try:
            account = self.client.get_account(self.symbol)
            for key, value in account.items():
                if key == "id":
                    self.accountid = value
        except Exception as e:
            # Print the exception as text
            traceback.print_exc()
            self.accountid = "None"
            pass

    def buyok(
        self,
        prediction_label,
        accuracy,
        acc_balance,
        amount_to_buy,
        purchase_price,
        current_price,
        exchange_rate,
        units,
        buy,
    ):
        if (
            prediction_label == "UP"
            and accuracy >= 60
            and acc_balance >= amount_to_buy
            and purchase_price == 0.0
        ):
            buy = "Buy"
            print(f"{self.symbol} -> Buy")
            purchase_price = float(current_price)
            units = (amount_to_buy) / (float(current_price) * float(exchange_rate))
            acc_balance = acc_balance - (units * current_price * exchange_rate)
            units = round(units, 3)
            try:
                returned = self.client.buy(self.accountid, amount=units, currency=self.symbol, commit=True)
                print(returned)
                print("Buy successful")
            except Exception as e:
                # Print the exception as text
                traceback.print_exc()
            return purchase_price, units, exchange_rate, acc_balance, buy
        else:
            return purchase_price, units, exchange_rate, acc_balance, buy

    def sellok(
        self,
        profit,
        acc_balance,
        units,
        exchange_rate,
        current_price,
        purchase_price,
        sell,
        prediciton_label,
    ):
        print("")
        # print(f"Profit: {profit}")
        if profit >= 30.0 and units > 0.0 and prediciton_label == "DOWN":
            sell = "Sell"
            print(f"{self.symbol} -> Sell")
            try:
                returned = self.client.sell(self.accountid, amount=units, currency=self.symbol, commit=True)
                print(returned)
                print("Sell successful")

            except Exception as e:
                # Print the exception as text
                traceback.print_exc()
            units = round(units, 3)
            acc_balance = acc_balance + (units * current_price * exchange_rate)
            units = 0.0
            exchange_rate = 0.0
            purchase_price = 0.0
            return purchase_price, units, exchange_rate, acc_balance, sell
        else:
            return purchase_price, units, exchange_rate, acc_balance, sell
