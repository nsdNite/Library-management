import os
import requests

from dotenv import load_dotenv


def send_telegram_notification(message: str) -> None:
    dotenv_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"
    )
    load_dotenv(dotenv_path)

    bot_token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if bot_token and chat_id:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
        }
        response = requests.post(url, data=data)

        if response.status_code != 200:
            print(f"Failed to send message: {response.text}")

    else:
        print("Telegram credentials are not provided")
