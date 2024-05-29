import aiogram
import time
import base64
import requests
from random import randint
from aiogram import Bot, Dispatcher, types, executor

Api= '#ключ бота'

bot = Bot(token= Api)
dp = Dispatcher(bot)


@dp.message_handler(commands= 'start')
async def started(message: types.Message):
   await message.answer('Давай работать')

def gen_img(prompt_text): 
   
    prompt = {
    
        "modelUri": "art://b1g3f13cj7d6d3ss2md9/yandex-art/latest",
        "generationOptions": {
        "seed": randint(20000, 40000000)
        },
        "messages": [
        {
            "weight": 1,
            "text": prompt_text
        }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key AQVN1cZPDuaKqCCvn2KuJJ51xXP_QOv_Cm0_YFu8"
        }
    response = requests.post(url= url, headers= headers, json= prompt)
    result = response.json()
    print(result)

    operation_id = result['id']
    operation_url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"

    while True:
        operation_response = requests.get(url= operation_url, headers= headers)
        operation_result = operation_response.json()
        if 'response' in operation_result:
            image_base64 = operation_result['response']['image']
            image_data = base64.b64decode(image_base64)
            return image_data
        else:
            print('Ожидайте компиляции')
            time.sleep(5)

@dp.message_handler()
async def pic_res(message: types.Message):
    user_text = message.text
    await message.reply('Ждумс')

    try: 
        image_data = gen_img(user_text)
        await message.reply_photo(photo= image_data)
    except Exception as e:
        await message.reply(f"Ошибка {e}")

if  __name__ == '__main__':
   executor.start_polling(dp, skip_updates= True)