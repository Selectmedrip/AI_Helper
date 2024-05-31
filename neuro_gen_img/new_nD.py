from tg_neuro import gen_img
from main import get_response
from resp import get_responses
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from keys import Api, C_Img_ID, G_key, C_GPT_ID

from aiogram import Bot, Dispatcher, types, executor

Api= Api

bot = Bot(token= Api)
dp = Dispatcher(bot)

state = None
running = True

# Создаем inline клавиатуру
inline_kb = InlineKeyboardMarkup()
inline_kb.add(InlineKeyboardButton('Сгенерировать текст', callback_data='tomorrow'))
inline_kb.add(InlineKeyboardButton('Сгенерировать изображение', callback_data='today'))

# Создаем markup клавиатуру
markup_kb = ReplyKeyboardMarkup(resize_keyboard=True)
markup_kb.add(KeyboardButton('/start - Запустить'))
markup_kb.add(KeyboardButton('/today - Сгенерировать изображение'))
markup_kb.add(KeyboardButton('/tomorrow - Сгенерировать текст'))
markup_kb.add(KeyboardButton('/stop - Остановить работу'))
markup_kb.add(KeyboardButton('/reset - Сброс при ошибке'))

@dp.message_handler(commands='start')
async def started(message: types.Message):
   global state, running
   state = None
   running = True
   await message.answer('Привет! Я нейро-штучка написанная <a href="tg://user?id=457425978">Маладым Армани</a> \nЯ умею: <blockquote>Cоставлять красивый текст</blockquote>\n<blockquote>А так же генерировать картинки на основе вашего запроса</blockquote>Улучшая запрос, я делаю рисунки более классным и реалистичным', parse_mode= "html")
   await message.answer("Нажмите на действия ниже чтобы начать", reply_markup=inline_kb)   

@dp.message_handler(commands='stop')
async def stop(message: types.Message):
   global running
   running = False
   await message.answer('Бот остановлен.')

@dp.callback_query_handler(lambda c: c.data == 'tomorrow')
async def process_callback_tomorrow(callback_query: types.CallbackQuery):
   global state
   if not running:
       return
   state = 'text_generation'
   await bot.answer_callback_query(callback_query.id)
   await bot.send_message(callback_query.from_user.id, '<blockquote>Генератор текста</blockquote>\nДавай напишем пару слов или словосочетаний из которых хотим получить красивый текст', parse_mode= "html", reply_markup=markup_kb)

@dp.callback_query_handler(lambda c: c.data == 'today')
async def process_callback_today(callback_query: types.CallbackQuery):
   global state
   if not running:
       return
   state = 'image_generation'
   await bot.answer_callback_query(callback_query.id)
   await bot.send_message(callback_query.from_user.id, '<blockquote>Генератор изображений</blockquote>\nДавай напишем то что хотим изобразить\n<tg-spoiler>Пример запроса: Нарисуй оранжевое яблоко</tg-spoiler>', parse_mode= "html", reply_markup=markup_kb)

@dp.message_handler(commands='reset')
async def reset(message: types.Message):
   global state
   if not running:
       return
   state = None
   await message.answer('Состояние сброшено, вы можете начать заново.')

@dp.message_handler()
async def process_message(message: types.Message):
   global state
   if not running:
       return
   if state == 'text_generation':
       responses_text = await get_responses((message.text))
       await message.answer(responses_text)
   elif state == 'image_generation':
       response_text = await get_response(message.text)
       user_text = response_text
       await message.answer(f"Вот ваш улучшенный запрос: ```\n{user_text}```", parse_mode= "MarkdownV2")
       print(user_text)
       await message.reply('Ждумс')
       try: 
           image_data = gen_img(user_text)
           await message.reply_photo(photo= image_data)
       except Exception as e:
           await message.reply(f"Ошибка {e}")
   state = None

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
