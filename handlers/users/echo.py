import psycopg2
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton

from data.config import *
from db.create_db import send_profil
from keyboards.inline.kb_profil import send_panel_profil
from loader import dp, bot
from states.registration import Registration


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, зайчик)) не всегда бывает легко, здесь ты можешь найти поддержу у людей"
                         f"с той же проблемой, что и у тебя, чтобы создать свой профиль нажми 👉🏼 /create "
                         f"на это уйдет 2-3 минуты")


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")

    await message.answer("\n".join(text))





# кастомные хэндлеры


# начало создания профиля
@dp.message_handler(commands='create', state=None)
async def ask_name(message : types.Message):
    await Registration.name.set()
    await message.answer('Как ты хочешь, чтобы отображалось твое имя?')


@dp.message_handler(commands='profil', state=None)
async def ask_name(message : types.Message):

    a = (await send_profil(message.chat.id))[0]
    print(a)
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Смотреть все параметры', callback_data="profil_all")
    but2 = InlineKeyboardButton('другое', callback_data="profil_null")
    markup.row(but1).row(but2)

    text = [f'*{a[1]}* - {a[2]} года',
            f'*характер*: {a[6]}',
            f'*Моя проблема*: {a[7]}',
            f'"{a[12]}"'
            ]


    await bot.send_photo(message.from_user.id, a[9], caption='\n'.join(text) ,parse_mode=ParseMode.MARKDOWN,
                         reply_markup=markup)












@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer("создать профиль /create")




# # Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
# @dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
# async def bot_echo_all(message: types.Message, state: FSMContext):
#     state = await state.get_state()
#     await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
#                          f"\nСодержание сообщения:\n"
#                          f"<code>{message}</code>")
#
#
