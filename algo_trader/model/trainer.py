import os
import logging
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

from ..utils.telegram import send_message
from ..utils.plotting import plot_training_history

logger = logging.getLogger("algo_trader")

class ModelTrainer:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.last_trained = None

    def _build(self, input_shape):
        from .architecture import build_lstm_model
        return build_lstm_model(input_shape)

    def train(self, X_train, y_train):
        """
        Trains (or re-trains) the LSTM model. Saves best weights to disk,
        plots training history, and sends a Telegram notification.
        """
        # load existing or build new
        if os.path.exists(self.model_path) and self.model is None:
            try:
                self.model = load_model(self.model_path)
                logger.info("Loaded existing model")
            except Exception:
                logger.warning("Failed to load model, building a new one")
                self.model = self._build(X_train.shape[1:])
        elif self.model is None:
            self.model = self._build(X_train.shape[1:])

        # callbacks
        callbacks = [
            EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
            ModelCheckpoint(self.model_path, save_best_only=True)
        ]

        # train
        history = self.model.fit(
            X_train, y_train,
            epochs=50,
            batch_size=32,
            validation_split=0.2,
            callbacks=callbacks,
            verbose=1
        )

        self.last_trained = datetime.now()

        # plot & notify
        history_path = os.path.splitext(self.model_path)[0] + "_history.png"
        plot_training_history(history, history_path)
        send_message("🔄 Model retrained", image_path=history_path)

        logger.info(f"Model trained at {self.last_trained}")
        return history
