# Telegram-интеграция для Kimi Work (Daimon)

Двусторонняя интеграция Kimi Work с Telegram: исходящие уведомления (брифинги, алерты, отчёты) и входящий сбор сообщений из чатов/каналов для анализа.

## Возможности

- ✅ **Исходящие**: отправка сообщений, фото, документов в Telegram
- ✅ **Входящие**: получение и сохранение сообщений из Telegram в JSON
- ✅ **Cron-ready**: интеграция с автоматическими задачами Kimi Work
- ✅ **Без зависимостей**: только стандартная библиотека Python (urllib)
- ✅ **SOCKS5-прокси**: поддержка Tor для обхода блокировок

## Структура

```
telegram_integration/
├── telegram_config.json          # Конфигурация (токен + chat_id) — НЕ коммитить!
├── telegram_sender.py            # Отправка сообщений/файлов/фото
├── telegram_listener.py          # Получение сообщений (long polling)
├── telegram_cli.py               # CLI для быстрой отправки
├── get_chat_id.py                # Определение chat_id
├── send_briefing.py              # Пример: отправка брифинга
├── messages/                     # Сохранённые входящие сообщения (создаётся автоматически)
└── examples/
    ├── send_text.py              # Пример: отправка текста
    ├── send_file.py              # Пример: отправка файла
    └── poll_messages.py          # Пример: получение сообщений
```

## Быстрый старт

### 1. Создать бота

1. Открой Telegram → найди `@BotFather`
2. Отправь `/newbot` и следуй инструкциям
3. Получи **токен** вида `123456789:ABCdef...`

### 2. Настроить конфиг

```bash
cp telegram_config.example.json telegram_config.json
# Отредактируй telegram_config.json — вставь токен и chat_id
```

### 3. Определить Chat ID

```bash
python telegram_integration/get_chat_id.py
```
Отправь боту `/start` в Telegram. Скрипт выведет chat_id.

### 4. Проверить отправку

```bash
python telegram_integration/telegram_cli.py "Тестовое сообщение"
```

## Использование в коде

### Отправка сообщения

```python
import sys
sys.path.insert(0, "telegram_integration")
from telegram_sender import send_message

send_message(
    "<b>Жирный заголовок</b>\n\nОбычный текст",
    parse_mode="HTML"
)
```

### Получение сообщений

```python
import sys
sys.path.insert(0, "telegram_integration")
from telegram_listener import poll_messages

# Polling на 10 циклов
poll_messages(max_runs=10)
```

### CLI

```bash
# Текст
python telegram_integration/telegram_cli.py "Сообщение"

# Файл
python telegram_integration/telegram_cli.py report.pdf --type doc --caption "Отчёт"

# Фото
python telegram_integration/telegram_cli.py chart.png --type photo --caption "График"
```

## Интеграция с Kimi Work Cron

Создай cron-задачу в Kimi Work, которая генерирует отчёт и вызывает `send_message()`:

```python
# Внутри cron-задачи (local_conversation)
import sys
sys.path.insert(0, "telegram_integration")
from telegram_sender import send_message

briefing = """<b>☀️ Утренний брифинг</b> — 15 июля 2026

<b>📰 Новости</b>
• ...

<b>📈 Рынки</b>
• ...

<b>📋 План дня</b>
• ...
"""

send_message(briefing)
```

## Обход блокировок (Роскомнадзор)

Если `api.telegram.org` недоступен:

### Вариант 1: Tor (рекомендуется)

```bash
# Установи Tor Browser и запусти его
# Затем в Python перед импортом telegram_sender:
from telegram_sender import setup_socks5_proxy
setup_socks5_proxy("127.0.0.1", 9050)
```

### Вариант 2: VPN системный

Включи VPN до запуска Kimi Desktop. Все запросы пойдут через VPN.

### Вариант 3: SOCKS5-прокси

```python
from telegram_sender import setup_socks5_proxy
setup_socks5_proxy("host", port)
```

## Безопасность

- ⚠️ **Никогда не коммить `telegram_config.json`** — там секретный токен
- ⚠️ **Никогда не коммить папку `messages/`** — там могут быть личные данные
- При утечке токена — отзови его через @BotFather (`/revoke`)

## Требования

- Python 3.8+
- Без внешних зависимостей (только стандартная библиотека)
- Для SOCKS5: `pip install PySocks` (опционально)

## Лицензия

MIT
