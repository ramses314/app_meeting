from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton

from db.create_db import *
from keyboards.kb_admin import send_admin_panel
from keyboards.kb_search import *
from loader import dp, bot
from states.registration import Registration


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, дорогуша 🤗 не всегда бывает легко, здесь ты можешь найти поддержу у людей "
                         f"с той же проблемой, что и у тебя, чтобы создать свой профиль жми 👉🏼 /create "
                       )


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/create - Создать профиль",
            "/search - Начать поиск",
            "/profil - Мой профиль",
            "/help - Получить справку",
            )
    await message.answer("\n".join(text))



# начало создания профиля
@dp.message_handler(commands='create', state=None)
async def ask_name(message : types.Message):
    await Registration.name.set()
    await message.answer('Как ты хочешь, чтобы отображалось твое имя?')

    # if len(await verify_user(message.chat.id)):
    #     await message.answer('Ты уже зарегистрирован\nСвои пареметры можешь изменить в профиле /profil')
    # else:
    #     await Registration.name.set()
    #     await message.answer('Как ты хочешь, чтобы отображалось твое имя?')
    #



# посмотреть свой профиль
@dp.message_handler(commands='profil', state=None)
async def show_profil(message : types.Message):
    a = (await send_profil(message.chat.id))[0]
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Смотреть все параметры', callback_data="profil_all")
    but2 = InlineKeyboardButton('другое', callback_data="other_bull")
    markup.row(but1).row(but2)

    text = [f'*{a[1]}* - {a[2]} года',
            f'*характер*: {a[6]}',
            f'*Моя проблема*: {a[7]}',
            f'"{a[12]}"']
    await bot.send_photo(message.chat.id, a[9], caption='\n'.join(text) ,parse_mode=ParseMode.MARKDOWN,
                         reply_markup=markup)


# начало поиска для знакомства
@dp.message_handler(commands='search', state=None)
async def send_search(message : types.Message):
    a = (await send_profil(message.chat.id))
    selected = (await send_search_db(message.chat.id, a[0][7].split(',\n'), a[0][13]))
    await send_first_search(message, selected)


# панель админа (+верификация)
@dp.message_handler(commands='admin', state=None)
async def send_search(message : types.Message):

    if len(await verify_admin(message.chat.id)):
        await send_admin_panel(message)
    else:
        await message.answer('Вы не являетесь админом')


# Ответ на рандомное сообщение
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer("🔎 Поиск /search\n"
                         "👤 профиль /profil")



# # Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
# @dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
# async def bot_echo_all(message: types.Message, state: FSMContext):
#     state = await state.get_state()
#     await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
#                          f"\nСодержание сообщения:\n"
#                          f"<code>{message}</code>")