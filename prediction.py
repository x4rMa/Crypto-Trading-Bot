import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from datetime import datetime, timedelta
from finta import TA
from collections import Counter


class CryptoPricePredictor:
    def __init__(self, delta_time_yf=1, interval_time_yf="1d", window=3, ROC_window=9):
        self.delta_time_yf = delta_time_yf
        self.interval_time_yf = interval_time_yf
        self.window = window
        self.ROC_window = ROC_window

    def predict_crypto_price_movement(self, crypto_symbol):
        now = datetime.utcnow()
        now = now - timedelta(microseconds=now.microsecond)
        yesterday = now - timedelta(days=self.delta_time_yf)
        crypto_data = yf.download(
            crypto_symbol,
            yesterday,
            now,
            interval=self.interval_time_yf,
            progress=False,
        )
        crypto_data["Price_Up"] = (
            TA.ROC(crypto_data, self.ROC_window).diff().shift(-1) > 0.0
        )
        crypto_data["Momentum"] = (
            crypto_data["Close"]
            - crypto_data["Close"].rolling(window=self.window).mean()
        )
        crypto_data["Volume_Change"] = crypto_data["Volume"].diff()
        crypto_data["Consecutive_Price_Ups"] = (
            crypto_data["Price_Up"]
            .rolling(window=self.window)
            .apply(lambda x: x.all())
            .shift(-self.window)
        )
        X = crypto_data[["Momentum", "Volume_Change"]].shift(1)
        y = crypto_data["Consecutive_Price_Ups"]
        X = X.iloc[self.window : -self.window]
        y = y.iloc[self.window : -self.window]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=False
        )
        model = RandomForestClassifier()
        model.fit(X_train.values, y_train.values)
        y_pred = model.predict(X_test.values)
        accuracy = (accuracy_score(y_test, y_pred)) * 100
        cm = confusion_matrix(y_test, y_pred)

        last_close = crypto_data.iloc[-1]["Close"]
        last_momentum = (
            last_close
            - crypto_data["Close"].rolling(window=self.window).mean().iloc[-1]
        )
        last_volume_change = (
            crypto_data.iloc[-1]["Volume"] - crypto_data.iloc[-2]["Volume"]
        )
        predicted_movement = model.predict([[last_momentum, last_volume_change]])
        prediction_label = "UP" if predicted_movement else "DOWN"
        trend_label = (
            "UP"
            if last_close
            > crypto_data["Close"].rolling(window=self.window).mean().iloc[-1]
            else "DOWN"
        )
        ROC = TA.ROC(crypto_data, self.ROC_window)
        current_exchange_rate = yf.download("USDNOK=X", progress=False)["Adj Close"]

        return (
            now,
            last_close,
            prediction_label,
            accuracy,
            trend_label,
            ROC.iloc[-1],
            current_exchange_rate.iloc[-1],
        )
