from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
import logging

logger = logging.getLogger("algo_trader")

def build_lstm_model(input_shape):
    """
    Constructs and compiles an LSTM model.
    input_shape: tuple (timesteps, features)
    """
    try:
        model = Sequential()
        model.add(LSTM(64, return_sequences=True, input_shape=input_shape))
        model.add(Dropout(0.2))
        model.add(LSTM(64))
        model.add(Dropout(0.2))
        model.add(Dense(3))  # predicting [high, low, close]
        model.compile(optimizer='adam', loss='mse')
        logger.info("Built new LSTM model")
        return model
    except Exception as e:
        logger.error(f"Error building model: {e}")
        raise
