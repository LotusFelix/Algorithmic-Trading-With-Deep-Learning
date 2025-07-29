import requests
import logging
from ..config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger("algo_trader")

def send_message(text: str, image_path: str = None):
    """
    Sends a text message (and optional image) to the configured Telegram chat.
    """
    base = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
    try:
        # send text
        resp = requests.post(f"{base}/sendMessage", data={
            'chat_id': TELEGRAM_CHAT_ID,
            'text': text
        })
        resp.raise_for_status()

        # send image if provided
        if image_path:
            with open(image_path, 'rb') as img:
                files = {'photo': img}
                resp = requests.post(f"{base}/sendPhoto",
                                     data={'chat_id': TELEGRAM_CHAT_ID},
                                     files=files)
                resp.raise_for_status()
    except Exception as e:
        logger.error(f"Telegram send failed: {e}")
