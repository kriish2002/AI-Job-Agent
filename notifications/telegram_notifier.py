import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Telegram credentials missing in .env file")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, data=payload, timeout=10)

        if response.status_code == 200:
            print("✅ Telegram notification sent successfully")
            return True

        print(f"❌ Telegram error: {response.text}")
        return False

    except requests.RequestException as error:
        print(f"❌ Telegram connection error: {error}")
        return False


if __name__ == "__main__":
    send_telegram_message(
        "🚀 Job Search Bot is connected with Telegram!"
    )