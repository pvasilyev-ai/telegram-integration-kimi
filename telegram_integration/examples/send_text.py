# Пример: отправка текстового сообщения
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from telegram_sender import send_message

if __name__ == "__main__":
    send_message(
        "<b>Привет!</b>\n\nЭто тестовое сообщение из примера.",
        parse_mode="HTML"
    )
    print("Сообщение отправлено!")
