import numpy as np
import logging

logger = logging.getLogger("algo_trader")

class Predictor:
    def __init__(self, model_trainer, preprocessor):
        """
        model_trainer: instance of ModelTrainer (with .model loaded)
        preprocessor: instance of Preprocessor (with fitted scalers)
        """
        self.trainer = model_trainer
        self.preprocessor = preprocessor

    def predict(self, df):
        """
        Expects df with at least look_back+1 rows.
        Returns dict with pred_high, pred_low, pred_close,
        their % changes vs current_close, and current_close.
        """
        try:
            # prepare input
            feats = df[['open','high','low','close','volume']].values
            scaled = self.preprocessor.scaler_X.transform(feats)
            X_pred = np.array([scaled])

            # predict & unscale
            y_scaled = self.trainer.model.predict(X_pred)
            y = self.preprocessor.scaler_y.inverse_transform(y_scaled)[0]

            current = df['close'].iloc[-1]
            ph, pl, pc = y
            pct = lambda x: (x - current) / current * 100

            result = {
                'pred_high': ph,
                'pred_low':  pl,
                'pred_close': pc,
                'high_change_pct': pct(ph),
                'low_change_pct':  pct(pl),
                'close_change_pct':pct(pc),
                'current_close':   current
            }
            logger.info(f"Prediction: {result}")
            return result
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return None
