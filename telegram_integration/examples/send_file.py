# Пример: отправка PDF-файла
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from telegram_sender import send_document

if __name__ == "__main__":
    # Укажи путь к своему файлу
    file_path = "report.pdf"
    
    if os.path.exists(file_path):
        send_document(file_path, caption="Еженедельный отчёт")
        print("Файл отправлен!")
    else:
        print(f"Файл не найден: {file_path}")
