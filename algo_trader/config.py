import os
from dotenv import load_dotenv

# read .env from project root
load_dotenv()

def _getenv(key, cast=str, default=None):
    val = os.getenv(key, default)
    if val is None:
        raise RuntimeError(f"Required config {key} not set in .env")
    return cast(val)

# Connection & credentials
MT5_LOGIN        = _getenv("MT5_LOGIN",        cast=int)
MT5_PASSWORD     = _getenv("MT5_PASSWORD")
MT5_SERVER       = _getenv("MT5_SERVER")
TELEGRAM_TOKEN   = _getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = _getenv("TELEGRAM_CHAT_ID", cast=int)

# Symbol & timeframe
SYMBOL    = _getenv("SYMBOL")
TIMEFRAME = _getenv("TIMEFRAME")

# Model hyperparameters
LOOK_BACK              = _getenv("LOOK_BACK",              cast=int)
PRICE_CHANGE_THRESHOLD = _getenv("PRICE_CHANGE_THRESHOLD", cast=float)
SL_MULTIPLIER          = _getenv("SL_MULTIPLIER",          cast=float)
TP_MULTIPLIER          = _getenv("TP_MULTIPLIER",          cast=float)
LOT_SIZE               = _getenv("LOT_SIZE",               cast=float)
RETRAIN_HOURS          = _getenv("RETRAIN_HOURS",          cast=int)

# Logging
LOG_LEVEL = _getenv("LOG_LEVEL", default="INFO")
LOG_FILE  = _getenv("LOG_FILE",  default="trading.log")
