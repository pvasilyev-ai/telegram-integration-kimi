"""
Telegram Listener Module — получение сообщений из Telegram для анализа
Использует long polling и только стандартную библиотеку Python.
Поддержка SOCKS5 через PySocks (опционально) для обхода блокировок.
"""

import json
import urllib.request
import time
import os
import socket
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "telegram_config.json")
STORAGE_DIR = os.path.join(os.path.dirname(__file__), "messages")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def setup_socks5_proxy(host="127.0.0.1", port=9050):
    """Настроить SOCKS5-прокси через PySocks."""
    try:
        import socks
        socks.set_default_proxy(socks.SOCKS5, host, port)
        socket.socket = socks.socksocket
        print(f"[Proxy] SOCKS5 {host}:{port} активен")
        return True
    except ImportError:
        print("[Proxy] PySocks не установлен. Установи: pip install PySocks")
        return False

def ensure_storage():
    os.makedirs(STORAGE_DIR, exist_ok=True)

def save_message(msg_data):
    """Сохранить сообщение в JSON-файл"""
    ensure_storage()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    msg_id = msg_data.get("message_id", "unknown")
    filename = f"msg_{ts}_{msg_id}.json"
    filepath = os.path.join(STORAGE_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(msg_data, f, ensure_ascii=False, indent=2)
    
    return filepath

def api_get(token, method, params=None):
    """GET-запрос к Telegram Bot API"""
    import urllib.parse
    query = urllib.parse.urlencode(params or {})
    url = f"https://api.telegram.org/bot{token}/{method}?{query}"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))

def get_updates(bot_token, offset=None, limit=100):
    """Получить обновления от Telegram Bot API"""
    params = {"limit": limit, "timeout": 30}
    if offset:
        params["offset"] = offset
    return api_get(bot_token, "getUpdates", params)

def extract_message_data(update):
    """Извлечь нужные данные из обновления"""
    msg = update.get("message") or update.get("channel_post")
    if not msg:
        return None
    
    chat = msg.get("chat", {})
    from_user = msg.get("from", {})
    
    return {
        "update_id": update.get("update_id"),
        "message_id": msg.get("message_id"),
        "chat_id": chat.get("id"),
        "chat_type": chat.get("type"),
        "chat_title": chat.get("title"),
        "from_id": from_user.get("id"),
        "from_username": from_user.get("username"),
        "date": msg.get("date"),
        "text": msg.get("text"),
        "entities": msg.get("entities"),
        "photo": msg.get("photo"),
        "document": msg.get("document"),
        "caption": msg.get("caption"),
    }

def poll_messages(bot_token=None, interval=5, max_runs=None, save=True):
    """
    Запустить polling для получения сообщений.
    
    Args:
        bot_token: токен бота (или из конфига)
        interval: интервал между запросами в секундах
        max_runs: максимальное количество циклов (None = бесконечно)
        save: сохранять ли сообщения в файлы
    """
    cfg = load_config()
    token = bot_token or cfg.get("bot_token")
    
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        raise ValueError("Bot token не настроен. Заполни telegram_config.json")
    
    offset = None
    run_count = 0
    
    print(f"[Telegram Listener] Polling started (interval={interval}s)")
    
    try:
        while True:
            if max_runs and run_count >= max_runs:
                break
            
            result = get_updates(token, offset=offset)
            
            if not result.get("ok"):
                print(f"[Error] {result}")
                time.sleep(interval)
                continue
            
            updates = result.get("result", [])
            
            for update in updates:
                offset = update.get("update_id", 0) + 1
                data = extract_message_data(update)
                
                if data and data.get("text"):
                    if save:
                        filepath = save_message(data)
                        print(f"[Saved] {filepath}: {data['text'][:80]}...")
                    else:
                        print(f"[Message] {data['text'][:100]}...")
            
            run_count += 1
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("[Telegram Listener] Stopped by user")
    
    return run_count

if __name__ == "__main__":
    poll_messages()
