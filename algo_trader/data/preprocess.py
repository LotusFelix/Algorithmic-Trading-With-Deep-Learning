import numpy as np
from sklearn.preprocessing import MinMaxScaler
import logging

logger = logging.getLogger("algo_trader")

class Preprocessor:
    def __init__(self, look_back: int):
        self.look_back = look_back
        self.scaler_X = MinMaxScaler()
        self.scaler_y = MinMaxScaler()

    def prepare(self, df):
        """
        From a DataFrame with columns [open,high,low,close,volume]:
        - Scale features and targets
        - Build LSTM sequences of length `look_back`
        - Split into train/test (80/20)
        """
        features = df[['open','high','low','close','volume']].values
        targets  = df[['high','low','close']].values

        X_scaled = self.scaler_X.fit_transform(features)
        y_scaled = self.scaler_y.fit_transform(targets)

        X, y = [], []
        for i in range(self.look_back, len(X_scaled)):
            X.append(X_scaled[i-self.look_back:i])
            y.append(y_scaled[i])

        X, y = np.array(X), np.array(y)
        split = int(len(X)*0.8)

        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]

        logger.info(
            f"Prepared data: X_train={X_train.shape}, "
            f"y_train={y_train.shape}, X_test={X_test.shape}, y_test={y_test.shape}"
        )
        return X_train, y_train, X_test, y_test
