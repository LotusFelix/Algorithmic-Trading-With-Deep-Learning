import time
import logging
from datetime import datetime, timedelta
import MetaTrader5 as mt5

from ..config import RETRAIN_HOURS, TIMEFRAME
from ..data.loader import DataLoader
from ..data.preprocess import Preprocessor
from ..model.trainer import ModelTrainer
from ..model.predictor import Predictor
from ..trading.executor import OrderExecutor
from ..utils.telegram import send_message

logger = logging.getLogger("algo_trader")

# mapping MT5 timeframe strings to seconds
TIMEFRAME_SECONDS = {
    'M1': 60, 'M5': 5*60, 'M15':15*60,
    'M30':30*60, 'H1':3600,  'H4':4*3600,
    'D1':86400
}

class TradingBot:
    def __init__(self, look_back):
        self.loader       = DataLoader()
        self.preprocessor = Preprocessor(look_back)
        self.trainer      = ModelTrainer(model_path="model.h5")
        self.predictor    = Predictor(self.trainer, self.preprocessor)
        self.executor     = OrderExecutor()
        self.last_trained = None

    def run(self):
        send_message("🚀 Trading Bot started")
        # initial training
        df = self.loader.get_historical_data()
        X_train, y_train, _, _ = self.preprocessor.prepare(df)
        self.trainer.train(X_train, y_train)
        self.last_trained = self.trainer.last_trained

        # main loop
        while True:
            try:
                # retrain if needed
                if datetime.now() - self.last_trained > timedelta(hours=RETRAIN_HOURS):
                    df = self.loader.get_historical_data()
                    X_train, y_train, _, _ = self.preprocessor.prepare(df)
                    self.trainer.train(X_train, y_train)
                    self.last_trained = self.trainer.last_trained

                # predict & trade
                df_latest = self.loader.get_historical_data(num_bars=self.preprocessor.look_back + 1)
                pred = self.predictor.predict(df_latest)
                if pred:
                    send_message(f"🔮 PREDICTION:\n{pred}")
                    self.executor.place_order(pred, df_latest)

                # wait for next candle
                wait_s = TIMEFRAME_SECONDS.get(TIMEFRAME, 3600)
                logger.info(f"Sleeping {wait_s} seconds until next candle")
                time.sleep(wait_s)

            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                send_message(f"⚠️ Error: {e}")
                time.sleep(60)

    def stop(self):
        self.loader.shutdown()
