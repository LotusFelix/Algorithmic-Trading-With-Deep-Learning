import logging
from logging.handlers import RotatingFileHandler
from ..config import LOG_LEVEL, LOG_FILE

def setup_logger(name="algo_trader"):
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    fmt   = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # Rotating file handler
    fh = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=3)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return logger
