"""
Telegram CLI — быстрая отправка сообщений и файлов из командной строки
Использует только стандартную библиотеку Python.
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from telegram_sender import send_message, send_document, send_photo

def main():
    parser = argparse.ArgumentParser(description="Telegram CLI для Kimi Work")
    parser.add_argument("content", help="Текст сообщения или путь к файлу")
    parser.add_argument("--type", choices=["text", "doc", "photo"], default="text",
                        help="Тип контента: text (по умолчанию), doc, photo")
    parser.add_argument("--caption", default="", help="Подпись к файлу")
    
    args = parser.parse_args()
    
    if args.type == "text":
        result = send_message(args.content)
    elif args.type == "doc":
        result = send_document(args.content, caption=args.caption)
    elif args.type == "photo":
        result = send_photo(args.content, caption=args.caption)
    
    print(result)

if __name__ == "__main__":
    main()
