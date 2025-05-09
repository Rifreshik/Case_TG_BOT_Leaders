🆘 Telegram Бот Поддержки

Простой Telegram-бот на Python для сбора заявок на поддержку, их просмотра и хранения в базе данных. Использует python-telegram-bot, SQLAlchemy и SQLite

Возможности:

📝 Приём заявок в заданном формате (ФИО, статус, сезон, контакты)  
📤 Автоматическая отправка заявки в групповой чат поддержки  
🗃 Хранение данных в базе (SQLite)  
👀 Просмотр всех заявок прямо в интерфейсе бота  
🔁 Удобная навигация по кнопкам

Установка:

1. Клонируй репозиторий  
git clone https://github.com/yourname/support-bot.git  
cd support-bot

2. Установи зависимости  
pip install -r requirements.txt

3. Проверь настройки в config.py  
GROUP_CHAT_ID = -1002632571519  
BOT_TOKEN = "ТВОЙ_ТОКЕН_БОТА"  
DATABASE_URL = "sqlite+aiosqlite:///database.db"

▶️ Запуск  
python main.py

💬 Формат заявки:

Пользователь должен отправить сообщение в формате:  
ФИО, Статус (полуфиналист/финалист/победитель), Сезон (1-5), Контакты (телефон и Telegram)  

Пример:  
Иванов Иван Иванович, финалист, 3, +79161234567 @username

🧠 Структура проекта:

support-bot/  
config.py — Конфигурации бота  
handlers.py — Основная логика и обработчики  
keyboards.py — Кнопки меню  
main.py — Точка входа  
models.py — ORM-модели и инициализация БД  
tools.py — Дополнительные утилиты  
README.md

🛡 Безопасность:

Не загружай BOT_TOKEN и другие чувствительные данные в открытые репозитории. Лучше используй .env файл и библиотеку python-dotenv

📦 Зависимости:

python-telegram-bot  
SQLAlchemy  
aiosqlite

🤝 Контрибьюция:

Pull request'ы и улучшения приветствуются. Если нашёл баг или есть идея — создавай issue
