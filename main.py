from algo_trader.utils.logging_setup import setup_logger
from algo_trader.config import LOOK_BACK
from algo_trader.trading.scheduler import TradingBot

logger = setup_logger()

if __name__ == "__main__":
    bot = TradingBot(look_back=LOOK_BACK)
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        bot.stop()
