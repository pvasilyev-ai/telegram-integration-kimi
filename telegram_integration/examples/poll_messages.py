# Пример: получение сообщений из Telegram
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from telegram_listener import poll_messages

if __name__ == "__main__":
    print("Сбор сообщений из Telegram...")
    print("Отправь что-нибудь боту, чтобы увидеть результат.")
    print("(Ctrl+C для остановки)\n")
    
    # Пolling на 20 циклов (≈ 100 секунд)
    poll_messages(max_runs=20)
    
    print("\nГотово! Сообщения сохранены в telegram_integration/messages/")
