from tg_neuro import gen_img
from main import get_response
from resp import get_responses
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keys import Api, C_Img_ID, G_key, C_GPT_ID

from aiogram import Bot, Dispatcher, types, executor

Api= Api

bot = Bot(token= Api)
dp = Dispatcher(bot)

keyboard_inline = InlineKeyboardMarkup(row_width= 2)
b_in1 = InlineKeyboardButton('Генерация текста', command='/')
b_in2 = InlineKeyboardButton('Генерация картинки', command='/')
keyboard_inline.add(b_in1, b_in2)
#input_field_placeholder="Выберите нужное"
    


@dp.message_handler(commands= 'start')
async def started(message: types.Message):
   await message.answer('Привет! Я нейро-штучка написанная <a href="tg://user?id=457425978">Маладым Армани</a> \nЯ умею: <blockquote>Cоставлять красивый текст</blockquote>\n<blockquote>А так же генерировать картинки на основе вашего запроса</blockquote>Улучшая запрос, я делаю рисунки более классным и реалистичным', parse_mode= "html")   
   await message.answer("Нажмите на действия ниже чтобы начать")#, reply_markup=keyboard_inline)

@dp.message_handler(commands= 'tomorrow')
async def tomorrow(message: types.Message):
   await message.answer('<blockquote>Генератор текста</blockquote>\nДавай напишем пару слов или словосочетаний из которых хотим получить красивый текст', parse_mode= "html")

@dp.message_handler()
async def analize_message(message:types.Message):
   responses_text = await get_responses((message.text))
   await message.answer(responses_text)


@dp.message_handler(commands= 'today')
async def tomorrow(message: types.Message):
   await message.answer('<blockquote>Генератор изображений</blockquote>\nДавай напишем то что хотим изобразить\n<tg-spoiler>Пример запроса: Нарисуй оранжевое яблоко</tg-spoiler>', parse_mode= "html")

@dp.message_handler()
async def pic_res(message: types.Message):
    response_text = await get_response(message.text)
    user_text = response_text
    await message.answer(f"Вот твой улучшенный запрос: ```\n{user_text}```", parse_mode= "MarkdownV2")
    print(user_text)
    await message.reply('Ждумс')

    try: 
        image_data = gen_img(user_text)
        await message.reply_photo(photo= image_data)
    except Exception as e:
        await message.reply(f"Ошибка {e}")


if  __name__ == '__main__':
   executor.start_polling(dp, skip_updates= True)