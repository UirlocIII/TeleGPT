import telebot
import openai
import requests
from io import BytesIO
from PIL import Image

# Задайте ваш OpenAI API ключ
openai.api_key = "OpenAI API ключ"

# Задайте ваш Telegram bot токен
TOKEN = 'Telegram bot токен'

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Обработка команды /text
@bot.message_handler(commands=['text'])
def generate_text(message):
    # Отправка сообщения пользователю
    bot.send_message(message.chat.id, "Введите ваш вопрос:")
    
    # Создание функции для получения ответа от OpenAI GPT-3
    @bot.message_handler(func=lambda message: True)
    def generate_response(message):
        # Получение ответа от OpenAI GPT-3
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt=message.text,
          max_tokens=1024,
          n=1,
          stop=None,
          temperature=0.5,
        )
        
        # Отправка ответа пользователю
        bot.send_message(message.chat.id, response.choices[0].text)
    
    # Регистрация функции для получения ответа от пользователя
    bot.register_next_step_handler(message, generate_response)

# Обработка команды /img
@bot.message_handler(commands=['img'])
def generate_image(message):
    # Отправка сообщения пользователю
    bot.send_message(message.chat.id, "Введите описание изображения:")
    
    # Создание функции для генерации изображения от OpenAI DALL-E
    @bot.message_handler(func=lambda message: True)
    def generate_response(message):
        # Получение изображения от OpenAI DALL-E
        image = requests.post("https://api.openai.com/v1/images/generations", 
                              headers={
                                  "Authorization": f"Bearer {openai.api_key}",
                              },
                              json={
                                  "model": "image-alpha-001",
                                  "prompt": message.text,
                                  "num_images": 1,
                                  "size": "512x512",
                                  "response_format": "url"
                              })
        # Преобразование изображения в формат для отправки пользователю
        img = Image.open(BytesIO(requests.get(image.json()['data'][0]['url']).content))
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Отправка изображения пользователю
        bot.send_photo(message.chat.id, photo=buffer)
    
    # Регистрация функции для получения описания изображения от пользователя
    bot.register_next_step_handler(message, generate_response)

# Запуск бота
bot.polling()
