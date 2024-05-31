import requests
from aiogram import Bot, Dispatcher, types, executor
from keys import Api, C_Img_ID, G_key, C_GPT_ID


API_TOKEN = Api
bot = Bot(token= API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Привет, я помощник по написанию текста построенный на базе ИИ, который поможет тебе написать текст на любую тему и вид текста. \n\nНапиши <code>Тема:</code> и <code>Вид текста:</code> <blockquote>Чтобы не писать вручную можно просто нажать на слова, они скопируются и можно писать свои мысли после двоеточия</blockquote> \n<tg-spoiler>Например: \n\n\tТема: Польза авокадо \n\n\tВид текста: Пост во Вконтакте</tg-spoiler>', parse_mode="html")

async def get_response(message_text):
  prompt = {
      
    "modelUri": C_GPT_ID,
    "completionOptions": {
      "stream": False,
      "temperature": 0,
      "maxTokens": "2000"
    },
    "messages": [
      {
        "role": "system",
        "text": "Ты - нейросеть, которая может улучшить запрос от пользователя, он передает тебе запрос, ты его улучшаешь и делаешь не более 500 символов и передаешь в нейросеть для генерации картинки в высоком разрешении и картинка должны быть реалистиной"
        #"text": "Ты — опытный копирайтер. Напиши маркетинговый текст с учётом вида текста и заданной темы."
      },
      {
        "role": "user",
        "text": message_text
      }
    ]
  }

  url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
  headers = {
    "Content-Type": "application/json",
    "Authorization": G_key
  } 

  response = requests.post(url, headers= headers, json=prompt)
  result = response.json()
  return result['result']['alternatives'][0]['message']['text']

@dp.message_handler()
async def analize_message(message:types.Message):
   response_text = await get_response((message.text))
   await message.answer(response_text)


if  __name__ == '__main__':
   executor.start_polling(dp, skip_updates= True)