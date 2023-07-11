from dotenv import load_dotenv
import os
import time
import schedule
from datetime import datetime
import traceback

from read_json import ReadJson
from database import Database
from create_folders import Folder
from prediction import CryptoPricePredictor
from buyorsell import BuyOrSell
from create_new_balance_entry import NewBalanceEntry


class Bot:
    def __init__(self):
        load_dotenv()
        self.api = os.getenv("KEY")
        self.secret = os.getenv("SECRET")
        self.acc_balance = 850.0
        self.amount_to_buy = 600.0
        self.database = "bot.db"
        self.delta_time_yf = 59
        self.interval_time_yf = "5m"
        self.window = 2
        self.ROC_window = 9
        self.now = datetime.today()
        self.crypto_symbol = ""
        self.current_price = 0.0
        self.prediction_label = ""
        self.accuracy = 0.0
        self.trend_label = ""
        self.last_roc = 0.0
        self.exchange_rate = 0.0
        self.accountid = ""
        self.current_price = 0.0
        self.profit = 0.0
        self.units = 0.0
        self.buyorsell = ""
        self.crypto_current_total_price = 0.0
        self.crypto_total_purchase_price = 0.0
        self.purchase_price = 0.0

    def core_code(self):
        # Code for executing core logic
        file_path = Folder().create_folder_link("CryptoList", "cryptolist.txt")
        with open(file_path, "r") as file:
            for line in file:
                crypto_symbol = line.strip()
                data = ReadJson().readbalancefile()
                try:
                    self.purchase_price = data[crypto_symbol]["purchase_price"]
                    self.units = data[crypto_symbol]["crypto_units"]
                    self.exchange_rate = data[crypto_symbol]["exchange_rate"]
                    self.buyorsell = data[crypto_symbol]["buy_sell"]
                    self.crypto_current_total_price = data[crypto_symbol][
                        "crypto_current_total_price"
                    ]
                    self.crypto_total_purchase_price = data[crypto_symbol][
                        "crypto_total_purchase_price"
                    ]
                    self.profit = data[crypto_symbol]["profit"]
                    self.current_price = data[crypto_symbol]["current_price"]
                    self.prediction_label = data[crypto_symbol]["prediction_label"]
                    self.accuracy = data[crypto_symbol]["accuracy"]
                    self.trend_label = data[crypto_symbol]["trend_label"]
                    self.last_roc = data[crypto_symbol]["last_roc"]
                    self.crypto_symbol = crypto_symbol
                except KeyError:
                    NewBalanceEntry(crypto_symbol)
                    data = ReadJson().readbalancefile()
                    self.purchase_price = data[crypto_symbol]["purchase_price"]
                    self.units = data[crypto_symbol]["crypto_units"]
                    self.exchange_rate = data[crypto_symbol]["exchange_rate"]
                    self.buyorsell = data[crypto_symbol]["buy_sell"]
                    self.crypto_current_total_price = data[crypto_symbol][
                        "crypto_current_total_price"
                    ]
                    self.crypto_total_purchase_price = data[crypto_symbol][
                        "crypto_total_purchase_price"
                    ]
                    self.profit = data[crypto_symbol]["profit"]
                    self.current_price = data[crypto_symbol]["current_price"]
                    self.prediction_label = data[crypto_symbol]["prediction_label"]
                    self.accuracy = data[crypto_symbol]["accuracy"]
                    self.trend_label = data[crypto_symbol]["trend_label"]
                    self.last_roc = data[crypto_symbol]["last_roc"]
                    self.crypto_symbol = crypto_symbol

                self.crypto_current_total_price = (
                    self.units * self.exchange_rate * self.current_price
                )

                try:
                    (
                        self.now,
                        self.current_price,
                        self.prediction_label,
                        self.accuracy,
                        self.trend_label,
                        self.last_roc,
                        self.exchange_rate,
                    ) = CryptoPricePredictor(
                        self.delta_time_yf,
                        self.interval_time_yf,
                        self.window,
                        self.ROC_window,
                    ).predict_crypto_price_movement(
                        crypto_symbol + "-USD"
                    )

                except Exception as e:
                    # Print the exception as text
                    traceback.print_exc()
                    pass

                (
                    self.purchase_price,
                    self.units,
                    self.exchange_rate,
                    self.acc_balance,
                    self.buyorsell,
                ) = BuyOrSell(self.api, self.secret, self.crypto_symbol).buyok(
                    self.prediction_label,
                    self.accuracy,
                    self.acc_balance,
                    self.amount_to_buy,
                    self.purchase_price,
                    self.current_price,
                    self.exchange_rate,
                    self.units,
                    self.buyorsell,
                )

                self.crypto_total_purchase_price = (
                    self.units * self.exchange_rate * self.purchase_price
                )
                self.profit = (
                    self.crypto_current_total_price - self.crypto_total_purchase_price
                )

                (
                    self.purchase_price,
                    self.units,
                    self.exchange_rate,
                    self.acc_balance,
                    self.buyorsell,
                ) = BuyOrSell(self.api, self.secret, self.crypto_symbol).sellok(
                    self.profit,
                    self.acc_balance,
                    self.units,
                    self.exchange_rate,
                    self.current_price,
                    self.purchase_price,
                    self.buyorsell,
                    self.prediction_label,
                )

                print("Date: ", self.now)
                print("Crypto Symbol: ", self.crypto_symbol)
                print("Current Crypto Total Price: ", self.crypto_current_total_price)
                print("Crypto Total Purchase Price: ", self.crypto_total_purchase_price)
                print("Profit: ", self.profit)

                data["acc_balance"] = self.acc_balance
                data[crypto_symbol]["purchase_price"] = self.purchase_price
                data[crypto_symbol]["crypto_units"] = self.units
                data[crypto_symbol]["exchange_rate"] = self.exchange_rate
                data[crypto_symbol]["buy_sell"] = self.buyorsell
                data[crypto_symbol][
                    "crypto_current_total_price"
                ] = self.crypto_current_total_price
                data[crypto_symbol][
                    "crypto_total_purchase_price"
                ] = self.crypto_total_purchase_price
                data[crypto_symbol]["profit"] = self.profit
                data[crypto_symbol]["current_price"] = self.current_price
                data[crypto_symbol]["prediction_label"] = self.prediction_label
                data[crypto_symbol]["accuracy"] = self.accuracy
                data[crypto_symbol]["trend_label"] = self.trend_label
                data[crypto_symbol]["last_roc"] = self.last_roc
                data[crypto_symbol]["account_id"] = self.accountid

                ReadJson().writebalancefile(data)

                # Writing to SQLite database
                self.now = datetime.now()
                sql_insert_data = (
                    float(time.time()),
                    str(self.now),
                    self.crypto_symbol,
                    self.trend_label,
                    self.last_roc,
                    self.purchase_price,
                    self.units,
                    self.exchange_rate,
                    self.prediction_label,
                    self.buyorsell,
                    self.acc_balance,
                    self.profit,
                    self.current_price,
                    self.crypto_current_total_price,
                )
                entry_id = Database().create_entry_crypto(
                    self.database, sql_insert_data
                )
                print("Entry ID: ", entry_id)
                print("*", end="\r")

    def main(self):
        # On start up, create a table in the database and checking account balance
        Database().create_table(self.database)
        data = ReadJson().readbalancefile()
        if data["acc_balance"] == 0:
            data["acc_balance"] = self.acc_balance
            ReadJson().writebalancefile(data)
        else:
            self.acc_balance = data["acc_balance"]

        self.core_code()
        schedule.every(5).minutes.do(self.core_code)

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    Bot().main()
