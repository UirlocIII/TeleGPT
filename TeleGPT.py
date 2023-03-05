import openai
import sys
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
ALLOWED_USER_IDS = [TG-ID]
token = 'TG-TOKEN'
openai.api_key = 'OPENAI-TOKEN'
bot = Bot(token)
dp = Dispatcher(bot)
@dp.message_handler()
async def process_message(message: types.Message):
    if message.from_user.id not in ALLOWED_USER_IDS:
        await message.reply("?? ?? ????????? ?????????? ?????????????.")
        return
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=[" Human:", " AI:"]
    )

    print(response['choices'][0]['text'])
    await message.reply(response['choices'][0]['text'])
    
executor.start_polling(dp, skip_updates=True)
