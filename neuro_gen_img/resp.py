import requests
from aiogram import Bot, Dispatcher, types, executor
from keys import Api, C_Img_ID, G_key, C_GPT_ID


API_TOKEN = Api
bot = Bot(token= API_TOKEN)
dp = Dispatcher(bot)

async def get_responses(msg_text):
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
        #"text": "Ты - нейросеть, которая может улучшить запрос от пользователя, он передает тебе запрос, ты его улучшаешь и делаешь не более 500 символов и передаешь в нейросеть для генерации картинки в высоком разрешении и картинка должны быть реалистиной"
        "text": "Ты — опытный копирайтер. Напиши маркетинговый текст с учётом вида текста и заданной темы."
      },
      {
        "role": "user",
        "text": msg_text
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
   responses_text = await get_responses((message.text))
   await message.answer(responses_text)