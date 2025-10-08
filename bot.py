"""
Бот, который отвечает на сообщения в Telegram.
Этот бот использует библиотеку python-telegram-bot для взаимодействия 
с Telegram API и библиотеку ollama для общения с моделью LLM.
Бот работает до тех пор, пока вы не нажмете Ctrl-C в командной строке.
"""

# Подключаем ведение журнала в файле bot.log
import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, filename='bot.log', filemode='w'
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

from telegram import ForceReply, Update

from telegram.ext import (
    ApplicationBuilder, # Основной класс для создания Telegram бот-приложения
    CommandHandler,     # Обработчик команд, начинающихся с "/" (например, /start)
    MessageHandler,     # Обработчик обычных текстовых сообщений
    ContextTypes,       # Типы контекста для хранения данных между вызовами обработчиков
    filters,            # Фильтры для определения, какие сообщения должен обрабатывать handler
)

import nest_asyncio
nest_asyncio.apply()


from model import chat_with_llm # Импортируем функцию для общения с LLM из model.py

import dotenv
# Загружаем переменные окружения из файла .env
try:
    env = dotenv.dotenv_values(".env")
    TELEGRAM_BOT_TOKEN = env["TELEGRAM_BOT_TOKEN"]
except FileNotFoundError:
    raise FileNotFoundError("Файл .env не найден. Убедитесь, что он существует в корневой директории проекта.")
except KeyError as e:
    raise KeyError(f"Переменная окружения {str(e)} не найдена в файле .env. Проверьте его содержимое.")


# <--- Определим функции-обработчики команд и сообщений---->

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start. При старте бота пользователь получает приветственное сообщение."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Здравствуйте {user.mention_html()}! Я чат-бот. Чем могу помочь?",
        reply_markup=ForceReply(selective=True),
    )

# Функция для обработки обычных сообщений
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Основная функция для обработки текстовых сообщений от пользователя с целью ответа на них с помощью AI."""
    user_message = update.message.text
    user = update.effective_user.mention_html() 
    print(f"Получено сообщение от {user}: {user_message}")    # Контрольная печать  
    user_message = f'Имя пользователя: {user}, Вопрос: {user_message}'
    # Получаем историю сообщений телеграм из context.chat_data
    history = context.chat_data.get("history", [])
    logger.debug(f"History: {history}")

    # Передаем текущий запрос и историю сообщений в LLM
    llm_response, history = chat_with_llm(user_message, history=history)
    print('H=',history)  # Контрольная печать 
    context.chat_data["history"] = history  # сохраняем обновленную историю
    
    await update.message.reply_text(llm_response)


async def main() -> None:
    """Функция инициализации бот-приложения."""
    
    # Создание основного объекта приложения Telegram API
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Обработчик всех текстовых сообщений 
    chat_handler = MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            chat
        )

    # Регистрируем обработчики:
    # Команда /start
    application.add_handler(CommandHandler("start", start))

    # Все остальные текстовые сообщения обрабатываются chat_handler
    application.add_handler(chat_handler)

    # Запуск бота в режиме постоянного ожидания команд.
    # Бот работает до остановки программы (нажатие Ctrl-C )
    print("Бот запущен...")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)
    

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    
