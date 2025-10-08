# Python Telegram AI Bot

Telegram-бот - консультант по курсам повышения квалификации в области программирования. 
Он использует языковую модель LLama, доступ к ней осуществляется по API. 
Бот написан на Python и использует библиотеку `python-telegram-bot` для работы с Telegram API и
библиотеку `ollama` для работы с API LLM Ollama.

## Инструкции по установке

### 1. Скачайте и распакуйте файлы проекта, откройте папку в VsCode.  
Или используйте консоль для клонирования репозитория:
```
git clone https://github.com/informdep1903-sudo/python-telegram-ai-bot
cd python-telegram-ai-bot
```

### 2. Создайте виртуальное окружение
Виртуальное окружение помогает изолировать зависимости проекта.
```bash
python -m venv venv
```
Активация окружения:
- На Windows:
  ```bash
  venv\Scripts\activate
  ```
- На macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

## 3. Установите зависимости
Можно сразу установить галочку на файле `requirements.txt` при создании виртуального окружения в VsCode.  
Или установите все необходимые библиотеки через терминал:
```bash
pip install -r requirements.txt
```

## 4. Настройка переменных окружения
Создайте файл `.env` в корневой папке проекта и добавьте туда токен телеграм-бота:
```
TELEGRAM_BOT_TOKEN=ваш_токен_бота
 
```
- TELEGRAM_BOT_TOKEN — получите в @BotFather в Telegram.

## 5. Запуск бота

Скачайте ollama  по адресу: https://github.com/ollama/ollama/releases/tag/v0.12.3
Выполните установку ollama (для развертывания модели Llama3.1 понадобится 10ГБ дисковой памяти) 

После установки ollama в окне отдельного терминала запустите сервер:
```bash
ollama serve
```
В окне терминала VScode загрузите и запустите модель LLM:
```bash
ollama pull llama3.1:latest
ollama run llama3.1:latest
```
Когда модель работает, то ввод /? отображает доступные команды для управления моделью:
```bash
Available Commands:
  /set            Set session variables
  /show           Show model information
  /load <model>   Load a session or model
  /save <model>   Save your current session
  /clear          Clear session context
  /bye            Exit
  /?, /help       Help for a command
  /? shortcuts    Help for keyboard shortcuts

Use """ to begin a multi-line message.

>>> 
```
Введите команду /bye, чтобы вернуться в терминал.

Запустите бота командой:
```bash
python bot.py
```
Если всё настроено верно, бот начнет работать и принимать сообщения в Telegram.
Для начала работы наберите в Telegram команду 
```
/start
```

## 6. Внесение изменений и помощь проекту
- Если хотите внести свой вклад, создайте issue (обсуждение проблемы) или отправьте pull request (предложение изменений).

