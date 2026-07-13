import os
import requests

from dotenv import load_dotenv


def main():

    load_dotenv()

    bot_token = os.getenv(
        "TELEGRAM_BOT_TOKEN"
    )

    if not bot_token:

        print(
            "❌ TELEGRAM_BOT_TOKEN not found in .env"
        )

        return

    url = (
        f"https://api.telegram.org/"
        f"bot{bot_token}/getUpdates"
    )

    try:

        print(
            "\n🤖 Checking Telegram Bot...\n"
        )

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        results = data.get(
            "result",
            []
        )

        if not results:

            print(
                "❌ No Telegram messages found"
            )

            print(
                "👉 Bot ko /start ya hello bhejo"
            )

            return

        latest_update = results[-1]

        message = latest_update.get(
            "message",
            {}
        )

        chat = message.get(
            "chat",
            {}
        )

        chat_id = chat.get(
            "id"
        )

        first_name = chat.get(
            "first_name",
            "Unknown"
        )

        print(
            "✅ Telegram Bot Connected"
        )

        print(
            f"👤 User : {first_name}"
        )

        print(
            f"💬 Chat ID : {chat_id}"
        )

        print(
            "\n👉 Copy Chat ID and save it in .env"
        )

    except Exception as e:

        print(
            f"❌ Telegram Error : {e}"
        )


if __name__ == "__main__":

    main()