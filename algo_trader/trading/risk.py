import pandas as pd
import logging

logger = logging.getLogger("algo_trader")

class RiskManager:
    def __init__(self, period: int = 14):
        self.period = period

    def calculate_atr(self, df: pd.DataFrame) -> float:
        """
        df must have columns ['high','low','close'] and at least period+1 rows.
        Returns the latest Average True Range.
        """
        d = df.copy()
        d['prev_close'] = d['close'].shift(1)
        d['tr1'] = d['high'] - d['low']
        d['tr2'] = (d['high'] - d['prev_close']).abs()
        d['tr3'] = (d['low']  - d['prev_close']).abs()
        d['tr']  = d[['tr1','tr2','tr3']].max(axis=1)
        atr = d['tr'].rolling(self.period).mean().iloc[-1]
        if pd.isna(atr):
            atr = d['tr'].mean()
            logger.warning(f"Insufficient data for rolling ATR; using simple mean {atr}")
        return float(atr)
