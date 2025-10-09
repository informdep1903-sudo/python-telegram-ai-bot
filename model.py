import ollama    # Библиотека для работы с Ollama API и совместимыми API
import logging    # Стандартная библиотека Python для логирования


logger = logging.getLogger(__name__)  # Создаем логгер для текущего модуля (__name__ - имя модуля)
logger.setLevel(logging.DEBUG)        # Устанавливаем уровень логирования DEBUG 

class OllamaService:
    """
    Класс для взаимодействия с локальной моделью Ollama.
    """
    def __init__(self, prompt_file, base_url="http://localhost:11434", model="llama3.1:latest"):
        """
        Аргументы:
            prompt_file (str): Путь к файлу с системным промптом.
            base_url (str): URL Ollama API.
            model (str): Название модели Ollama.
        """
        
        try:   
        # Читаем системный промт из файла и сохраняем его в  sys_prompt
            with open(prompt_file, encoding='utf-8') as f:
                print("Системный промпт загружен.")
                self.sys_prompt = f.read()
            self.base_url = base_url
            self.model = model
        except FileNotFoundError:
            logger.error(f"Файл промпта не найден: {prompt_file}")
            raise



    def chat(self, message, history):
        """
        Отправляет сообщение в Ollama и получает ответ.

        Аргументы:
            message (str): Сообщение пользователя.
            history (list): История сообщений (список dict с ключами 'role' и 'content').

        Возвращает:
            str: Ответ Ollama.
        """
        
        # Формируем промт для отправки в API LLM со структурой:
            # - системный промпт: {"role": "system", "content": self.sys_prompt}
            # - последние 4 сообщения из истории диалога, например:
            #  [{"role": "user", "content": "Привет"}, {"role": "assistant", "content": "Здравствуйте"},...]
            # - текущее сообщение пользователя: {"role": "user", "content": message}
        messages = [{"role": "system", "content": self.sys_prompt}] + history[-4:] + [{"role": "user", "content": message}]
        print(f"Сообщения для Ollama: {messages}") # Контрольная печать 

        # Опции для настройки поведения модели
        custom_options = {
        "temperature": 0.5 # Контролирует креативность ответов модели (0.0 - более точные, 1.0 - более креативные; по умолчанию 0.7)
        }

        try:
            # Передача ollama.chat структурированного промта и получение ответа
            response = ollama.chat(model=self.model, messages=messages, options=custom_options)
            return response['message']['content']
        except Exception as e:
            # Логируем ошибку и возвращаем сообщение об ошибке
            logger.error(f"Ollama error: {str(e)}")
            return f"Ошибка при обращении к Ollama: {str(e)}"


# Создание экземпляра OllamaService с системным промтом из файла
llm_1 = OllamaService('prompts/prompt_2.txt')


def chat_with_llm(user_message, history):
    """
    Чат с использованием сервиса LLM.
    Аргументы:
        user_message (str): Сообщение пользователя.
        history (list): История сообщений (список dict с ключами 'role' и 'content').
    Возвращает:
        str: Ответ LLM.
    """
    llm_response = llm_1.chat(user_message, history)
    history.append({"role": "user", "content": user_message})  # добавляем сообщение пользователя в историю
    history.append({"role": "assistant", "content": llm_response}) # добавляем ответ ассистента в историю
    return llm_response, history
