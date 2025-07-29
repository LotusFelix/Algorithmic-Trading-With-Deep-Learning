import MetaTrader5 as mt5
import logging
from ..config import SYMBOL, LOT_SIZE, PRICE_CHANGE_THRESHOLD, SL_MULTIPLIER, TP_MULTIPLIER
from .risk import RiskManager
from ..utils.telegram import send_message

logger = logging.getLogger("algo_trader")

class OrderExecutor:
    def __init__(self):
        self.risk_mgr = RiskManager()

    def place_order(self, prediction: dict, df):
        """
        Builds and sends an MT5 order based on the prediction dict
        and recent DataFrame (for ATR). Returns MT5 result or None.
        """
        cpct = prediction['close_change_pct']
        if abs(cpct) < PRICE_CHANGE_THRESHOLD:
            logger.info(f"No trade: change {cpct:.2f}% < threshold")
            return None

        order_type = mt5.ORDER_TYPE_BUY if cpct > 0 else mt5.ORDER_TYPE_SELL
        tick = mt5.symbol_info_tick(SYMBOL)
        if tick is None:
            logger.error("Failed to get tick info")
            return None
        price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid

        # ATR-based SL/TP
        atr = self.risk_mgr.calculate_atr(df)
        sl_pips = atr * SL_MULTIPLIER
        tp_pips = atr * TP_MULTIPLIER
        if order_type == mt5.ORDER_TYPE_BUY:
            sl, tp = price - sl_pips, price + tp_pips
        else:
            sl, tp = price + sl_pips, price - tp_pips

        req = {
            "action":   mt5.TRADE_ACTION_DEAL,
            "symbol":   SYMBOL,
            "volume":   LOT_SIZE,
            "type":     order_type,
            "price":    price,
            "sl":       sl,
            "tp":       tp,
            "deviation":10,
            "magic":    12345,
            "comment":  "AlgoTrade",
            "type_time":    mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        res = mt5.order_send(req)
        if res.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Order failed: {res.comment}")
            send_message(f"❌ Order failed: {res.comment}")
            return None

        logger.info(f"Order placed: {res}")
        send_message(f"🔔 Order placed: {res}")
        return res
