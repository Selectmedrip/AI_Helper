import requests
from aiogram import Bot, Dispatcher, types, executor


API_TOKEN = '#ключ бота'
bot = Bot(token= API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Привет, я помощник по написанию текста построенный на базе ИИ, который поможет тебе написать текст на любую тему и вид текста. \n\nНапиши <code>Тема:</code> и <code>Вид текста:</code> <blockquote>Чтобы не писать вручную можно просто нажать на слова, они скопируются и можно писать свои мысли после двоеточия</blockquote> \n<tg-spoiler>Например: \n\n\tТема: Польза авокадо \n\n\tВид текста: Пост во Вконтакте</tg-spoiler>', parse_mode="html")

async def get_response(message_text):
  prompt = {
      
    "modelUri": "gpt://b1gf5pfjsd0phsrq2ldh/yandexgpt-lite",
    "completionOptions": {
      "stream": False,
      "temperature": 0.3,
      "maxTokens": "1000"
    },
    "messages": [
      {
        "role": "system",
        "text": "Ты — опытный копирайтер. Напиши маркетинговый текст с учётом вида текста и заданной темы."
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



#Пример забавной фишки
@dp.message_handler(commands='viewimport')
async def start(message: types.Message):
 await message.reply('<pre><code class="language-python">import requests\nfrom aiogram import Bot, Dispatcher, types, executor</code></pre>', parse_mode="html")

@dp.message_handler(commands='viewsett')
async def start(message: types.Message):
 await message.reply('<pre><code class="language-python">API_TOKEN = "Указать токен"\nbot = Bot(token= API_TOKEN)\ndp = Dispatcher(bot)</code></pre>', parse_mode="html")

@dp.message_handler(commands='viewstart')
async def start(message: types.Message):
 await message.reply('<pre><code class="language-python">@dp.message_handler(commands="start")\nasync def start(message: types.Message):\n\tawait message.reply("Привет, я помощник по написанию текста построенный на базе ИИ, который поможет тебе написать текст на любую тему и вид текста. \n\nНапиши <code>Тема:</code> и <code>Вид текста:</code>", parse_mode="html")</code></pre>', parse_mode="html")



if  __name__ == '__main__':
   executor.start_polling(dp, skip_updates= True)