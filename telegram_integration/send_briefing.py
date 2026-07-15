"""
Отправка утреннего брифинга в Telegram
Используется для cron-задач или ручного запуска
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from telegram_sender import send_message

def send_briefing(text_content=None):
    """Отправить готовый брифинг или заглушку"""
    
    if text_content:
        message = text_content
    else:
        # Если нет готового текста — отправляем шаблон с призывом
        message = """<b>☀️ Утренний брифинг</b>

Брифинг готовится в рабочем пространстве Kimi Work.
Открой приложение для полной версии.

<i>Нео</i>"""
    
    result = send_message(message)
    print(f"[Briefing] Sent: {result.get('ok', False)}")
    return result

if __name__ == "__main__":
    # Можно передать текст как аргумент
    text = sys.argv[1] if len(sys.argv) > 1 else None
    send_briefing(text)
