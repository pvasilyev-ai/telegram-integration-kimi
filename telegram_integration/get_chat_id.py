"""
Скрипт для определения Chat ID через getUpdates
Использует только стандартную библиотеку Python.
"""

import json
import urllib.request
import time
import sys
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "telegram_config.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def api_get(token, method, params=None):
    query = ""
    if params:
        query = "?" + "&".join(f"{k}={v}" for k, v in params.items())
    url = f"https://api.telegram.org/bot{token}/{method}{query}"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))

def main():
    cfg = load_config()
    token = cfg.get("bot_token")
    
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        print("❌ Bot token не настроен!")
        print("1. Создай бота через @BotFather (/newbot)")
        print("2. Запиши токен в telegram_config.json")
        sys.exit(1)
    
    print("⏳ Ожидаю сообщение...")
    print("Отправь что-нибудь боту в Telegram (или /start)")
    print("(Ctrl+C для отмены)")
    
    offset = None
    found = False
    
    try:
        while not found:
            params = {"limit": 10, "timeout": 30}
            if offset:
                params["offset"] = offset
            result = api_get(token, "getUpdates", params)
            
            if not result.get("ok"):
                print(f"❌ Ошибка API: {result}")
                break
            
            updates = result.get("result", [])
            
            for update in updates:
                offset = update.get("update_id", 0) + 1
                msg = update.get("message") or update.get("channel_post")
                
                if msg:
                    chat = msg.get("chat", {})
                    chat_id = chat.get("id")
                    chat_type = chat.get("type")
                    chat_title = chat.get("title", "Личный чат")
                    text = msg.get("text", "<без текста>")
                    
                    print(f"\n✅ Сообщение получено!")
                    print(f"   Chat ID: {chat_id}")
                    print(f"   Тип: {chat_type}")
                    print(f"   Название: {chat_title}")
                    print(f"   Текст: {text[:60]}...")
                    print(f"\n👉 Запиши Chat ID в telegram_config.json: \"{chat_id}\"")
                    found = True
                    break
            
            if not found:
                time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n\n⛔ Отменено")

if __name__ == "__main__":
    main()
