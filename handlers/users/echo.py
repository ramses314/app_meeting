from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton

from db.function_db import *
from keyboards.kb_admin import send_admin_panel
from keyboards.kb_search import *
from loader import dp, bot
from states.registration import Registration



@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет 🤗 здесь ты можешь найти поддержу у людей "
                         f"с той же проблемой, что и у тебя. Создай свой профиль, жмякай 👉🏼 /create ")


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
async def create_my_profil(message : types.Message):

    # await Registration.name.set()
    # await message.answer('Как ты хочешь, чтобы отображалось твое имя?')

    identity = await verify_user(message.chat.id)

    if identity == 'already_registered':
        await message.answer('Ты уже зарегистрирован\nСвои пареметры можешь изменить в профиле /profil')
    elif identity == 'blocked':
        await message.answer('Вы заблокированы по немкольким жалобам на ваш профиль')
    else:
        await Registration.name.set()
        await message.answer('Как ты хочешь, чтобы отображалось твое имя?')


# посмотреть свой профиль
@dp.message_handler(commands='profil', state=None)
async def show_profil(message : types.Message):

    identity = await verify_user(message.chat.id)

    if identity == 'already_registered':

        a = (await send_profil(message.chat.id))[0]

        markup = InlineKeyboardMarkup()
        but1 = InlineKeyboardButton('Смотреть все параметры', callback_data="profil_all")
        but2 = InlineKeyboardButton('другое', callback_data="other_bull")
        markup.row(but1).row(but2)
        text = [f'*{a[1]}*, *{a[2]}*, {a[6]}',
                f'*Чувствую себя на {10 - int(a[8])} из 10*',
                f'*Моя проблема*: {a[7]}',
                f'"{a[12]}"']
        await bot.send_photo(message.chat.id, a[9], caption='\n'.join(text), parse_mode=ParseMode.MARKDOWN,
                             reply_markup=markup)
    elif identity == 'blocked':
        await message.answer('Вы заблокированы по немкольким жалобам на ваш профиль')
    else:
        await message.answer('Вы еще не зарегестрированы -> /create')


# начало поиска для знакомства
@dp.message_handler(commands='search', state=None)
async def send_search(message : types.Message):
    identity = await verify_user(message.chat.id)

    if identity == 'already_registered':
        a = (await send_profil(message.chat.id))
        selected = (await send_search_db(message.chat.id, a[0][7].split(',\n'), a[0][13]))
        await send_first_search(message, selected)
        await update_activity(message.chat.id)
    elif identity == 'blocked':
        await message.answer('Вы заблокированы по немкольким жалобам на ваш профиль')
    else:
        await message.answer('Вы еще не зарегестрированы -> /create')


# панель админа (+верификация)
@dp.message_handler(commands='admin', state=None)
async def send_admins_panel(message : types.Message):

    if len(await verify_admin(message.chat.id)):
        await send_admin_panel(message, 'first')
    else:
        await message.answer('Вы не являетесь админом')


# Снова делает невидимого ("спящего") пользователя видимым
@dp.message_handler(commands='lets_search', state=None)
async def send_search(message : types.Message):
    await stop_searching(True, message.chat.id)
    await message.answer('Хаю-хай 😁 ты снова в деле)))')


# Ответ на рандомное сообщение
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer("🔎 Поиск /search\n"
                         "👤 профиль /profil")


# # Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием (удалить????)
# @dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
# async def bot_echo_all(message: types.Message, state: FSMContext):
#     state = await state.get_state()
#     await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
#                          f"\nСодержание сообщения:\n"
#                          f"<code>{message}</code>")