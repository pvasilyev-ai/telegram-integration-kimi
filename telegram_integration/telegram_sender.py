"""
Telegram Sender Module — отправка сообщений из Kimi Work в Telegram
Использует только стандартную библиотеку Python (urllib).
Поддержка SOCKS5 через PySocks (опционально) для обхода блокировок.
"""

import json
import urllib.request
import urllib.parse
import sys
import os
import socket

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "telegram_config.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def setup_socks5_proxy(host="127.0.0.1", port=9050):
    """Настроить SOCKS5-прокси через PySocks (для обхода блокировок)."""
    try:
        import socks
        socks.set_default_proxy(socks.SOCKS5, host, port)
        socket.socket = socks.socksocket
        print(f"[Proxy] SOCKS5 {host}:{port} активен")
        return True
    except ImportError:
        print("[Proxy] PySocks не установлен. Установи: pip install PySocks")
        return False

def api_call(token, method, payload):
    """Универсальный POST-запрос к Telegram Bot API"""
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def api_get(token, method, params=None):
    """GET-запрос к Telegram Bot API"""
    query = urllib.parse.urlencode(params or {})
    url = f"https://api.telegram.org/bot{token}/{method}?{query}"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def send_message(text, chat_id=None, bot_token=None, parse_mode="HTML"):
    """Отправить текстовое сообщение в Telegram"""
    cfg = load_config()
    token = bot_token or cfg.get("bot_token")
    cid = chat_id or cfg.get("chat_id")
    
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        raise ValueError("Bot token не настроен. Заполни telegram_config.json")
    if not cid or cid == "YOUR_CHAT_ID_HERE":
        raise ValueError("Chat ID не настроен. Заполни telegram_config.json")
    
    max_len = cfg.get("max_message_length", 4096)
    
    if len(text) > max_len:
        parts = [text[i:i+max_len] for i in range(0, len(text), max_len)]
        results = []
        for part in parts:
            payload = {"chat_id": cid, "text": part, "parse_mode": parse_mode}
            results.append(api_call(token, "sendMessage", payload))
        return results
    
    payload = {"chat_id": cid, "text": text, "parse_mode": parse_mode}
    return api_call(token, "sendMessage", payload)

def send_document(file_path, caption="", chat_id=None, bot_token=None):
    """Отправить файл в Telegram через multipart/form-data"""
    cfg = load_config()
    token = bot_token or cfg.get("bot_token")
    cid = chat_id or cfg.get("chat_id")
    
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    import mimetypes
    boundary = "----KimiBoundary"
    content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    filename = os.path.basename(file_path)
    
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="chat_id"\r\n\r\n'
        f"{cid}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="caption"\r\n\r\n'
        f"{caption}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="document"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))

def send_photo(photo_path, caption="", chat_id=None, bot_token=None):
    """Отправить фото в Telegram"""
    cfg = load_config()
    token = bot_token or cfg.get("bot_token")
    cid = chat_id or cfg.get("chat_id")
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    boundary = "----KimiBoundary"
    filename = os.path.basename(photo_path)
    
    with open(photo_path, "rb") as f:
        file_data = f.read()
    
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="chat_id"\r\n\r\n'
        f"{cid}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="caption"\r\n\r\n'
        f"{caption}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="photo"; filename="{filename}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python telegram_sender.py '<text>'")
        sys.exit(1)
    
    text = sys.argv[1]
    result = send_message(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
