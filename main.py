import requests
from aiogram import Bot, Dispatcher, types, executor


API_TOKEN = '6864333041:AAEsBWkfwrXH0bIF6V6fUFrnXiUdvKYNNiU'
bot = Bot(token= API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply('Привет, я помощник по трудоустройству построенный на базе ИИ, который поможет тебе подготовиться к собеседованию. \nНапиши название компании и желаемую должность по которой ты хочешь пройти собеседование.')


async def get_response(message_text):
  prompt = {
      
    "modelUri": "gpt://b1gf5pfjsd0phsrq2ldh/yandexgpt-lite",
    "completionOptions": {
      "stream": False,
      "temperature": 0,
      "maxTokens": "2000"
    },
    "messages": [
      {
        "role": "system",
        "text": "Ты — рекрутер в указанной компании. Имитируй собеседование на работу для указанной должности, задавая вопросы, как будто ты потенциальный работодатель. Твоя задача — определить технические навыки кандидата. Сгенерируй вопросы для интервью с потенциальным кандидатом"
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
    "Authorization": "Api-Key AQVN2o_cOTMNQHd8b3UIPPnfPfNL4ZJ_d8S3oavt"
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