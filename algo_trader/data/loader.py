import MetaTrader5 as mt5
import pandas as pd
import logging
from ..config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER, SYMBOL, TIMEFRAME, LOOK_BACK

logger = logging.getLogger("algo_trader")

class DataLoader:
    def __init__(self):
        """Initialize and connect to MT5."""
        if not mt5.initialize(login=MT5_LOGIN,
                              password=MT5_PASSWORD,
                              server=MT5_SERVER):
            err = mt5.last_error()
            logger.error(f"MT5 initialize failed: {err}")
            raise ConnectionError(f"MT5 initialize failed: {err}")
        logger.info("MT5 initialized successfully")

    def get_historical_data(self, num_bars: int = None) -> pd.DataFrame:
        """Fetch OHLCV bars from MT5 and return as a pandas DataFrame."""
        if num_bars is None:
            num_bars = LOOK_BACK * 10  # or some default max

        tf = mt5.TIMEFRAME_DICT.get(TIMEFRAME, mt5.TIMEFRAME_H1)
        bars = mt5.copy_rates_from_pos(SYMBOL, tf, 0, num_bars)
        if bars is None or len(bars) == 0:
            err = mt5.last_error()
            logger.error(f"No data: {err}")
            raise RuntimeError(f"Error fetching data: {err}")

        df = pd.DataFrame(bars)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)

        # Standardize columns
        if 'tick_volume' in df.columns and 'volume' not in df.columns:
            df['volume'] = df['tick_volume']
        for short, full in [('o','open'), ('h','high'), ('l','low'), ('c','close')]:
            if short in df.columns and full not in df.columns:
                df[full] = df[short]

        # Ensure required columns
        for col in ['open','high','low','close','volume']:
            if col not in df.columns:
                if col == 'volume':
                    df['volume'] = 1
                    logger.warning("volume missing → filled with 1s")
                else:
                    raise KeyError(f"Missing required column: {col}")

        logger.info(f"Fetched {len(df)} bars for {SYMBOL}@{TIMEFRAME}")
        return df

    def shutdown(self):
        """Shutdown MT5 connection."""
        mt5.shutdown()
        logger.info("MT5 connection closed")
