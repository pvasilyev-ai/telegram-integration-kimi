# Telegram-интеграция для Kimi Work

## Назначение

Двусторонняя интеграция с Telegram:
1. **Исходящие уведомления** — автоматическая отправка отчётов, брифингов, алертов из Kimi Work в Telegram
2. **Входящие данные** — получение и сохранение сообщений из Telegram-чатов/каналов для анализа

## Структура

```
telegram_integration/
├── telegram_config.json      # ← Заполни токен и chat_id
├── telegram_sender.py        # Отправка сообщений/файлов/фото
├── telegram_listener.py      # Получение сообщений (polling)
├── telegram_cli.py           # CLI для быстрой отправки
├── get_chat_id.py            # Скрипт определения chat_id
├── send_briefing.py          # Пример: отправка брифинга
├── README.md                 # Эта инструкция
└── messages/                 # Сохранённые сообщения (создаётся автоматически)
```

## Настройка

### 1. Создание Telegram-бота

1. Открой Telegram и найди `@BotFather`
2. Отправь `/newbot` и следуй инструкциям
3. Получи **токен** вида `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
4. Запиши токен в `telegram_config.json` в поле `bot_token`

### 2. Определение Chat ID

**Вариант А — через скрипт:**
```bash
python telegram_integration/get_chat_id.py
```
Затем отправь любое сообщение боту в Telegram. Скрипт выведет chat_id.

**Вариант Б — через BotFather:**
1. Найди бота в Telegram, отправь `/start`
2. Открой в браузере: `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Найди `"chat":{"id":123456789` — это твой chat_id

### 3. Заполнение конфигурации

Открой `telegram_config.json` и заполни:
```json
{
  "bot_token": "123456789:ABCdef...",
  "chat_id": "123456789",
  "channels_to_monitor": ["@channel_name"],
  "groups_to_monitor": ["-1001234567890"],
  "polling_interval": 5,
  "auto_forward": false,
  "max_message_length": 4096
}
```

> **Важно:** `chat_id` может быть отрицательным для групп и каналов.

### 4. Проверка отправки

```bash
python telegram_integration/telegram_cli.py "Тестовое сообщение от Нео"
```

## Использование

### Отправка сообщений из кода

```python
import sys
sys.path.insert(0, "telegram_integration")
from telegram_sender import send_message, send_document

# Текст
send_message("<b>Жирный заголовок</b>\n\nОбычный текст")

# Файл
send_document("/path/to/report.pdf", caption="Еженедельный отчёт")
```

### Получение сообщений (polling)

```bash
# Интерактивный режим
python telegram_integration/telegram_listener.py

# Ограниченное число циклов (для cron)
python -c "import sys; sys.path.insert(0, 'telegram_integration'); from telegram_listener import poll_messages; poll_messages(max_runs=10)"
```

Сообщения сохраняются в `telegram_integration/messages/` как JSON-файлы.

### Быстрая отправка из командной строки

```bash
# Текст
python telegram_integration/telegram_cli.py "Сообщение"

# Файл
python telegram_integration/telegram_cli.py report.pdf --type doc --caption "Отчёт"

# Фото
python telegram_integration/telegram_cli.py chart.png --type photo --caption "График"
```

## Интеграция с cron-задачами

### Утренний брифинг в Telegram

Пример: `telegram_integration/send_briefing.py` — скрипт, который генерирует брифинг и отправляет в Telegram. Можно вызвать из cron-задачи или запустить напрямую:

```bash
python telegram_integration/send_briefing.py
```

### Настройка cron для автоматических уведомлений

Создай cron-задачу через Kimi Work (`Cron` tool), которая:
1. Генерирует отчёт/брифинг
2. Вызывает `telegram_sender.py` для отправки

## Безопасность

- Не коммить `telegram_config.json` в публичные репозитории
- Токен бота — секретный ключ. При компрометации — отзови через @BotFather (`/revoke`)
- Для production рассмотри использование переменных окружения вместо JSON-конфига

## Ограничения Telegram Bot API

- Максимум 30 сообщений в секунду
- Длина сообщения: 4096 символов (скрипт автоматически разбивает)
- Размер файла: до 20 МБ для документов, до 10 МБ для фото
- Для каналов бот должен быть администратором

## Поддержка

При проблемах проверь:
1. Корректность токена (через `https://api.telegram.org/bot<TOKEN>/getMe`)
2. Chat ID (через `get_chat_id.py` или `getUpdates`)
3. Права бота в группах/каналах
