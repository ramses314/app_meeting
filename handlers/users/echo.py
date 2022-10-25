from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton

from db.function_db import *
from keyboards.kb_admin import send_admin_panel
from keyboards.kb_search import *
from loader import dp, bot
from states.registration import Registration, BeAdmin


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, меня зовут Митти 🤗 здесь ты можешь найти поддержу у людей "
                         f"с той же проблемой, что и у тебя. Создай свой профиль, жмякай 👉🏼 /create")
                         # f"\nЕсли ты здесь для регистрации на сайте, то 👉🏼 /get_login")


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд 📋 ",
            "/search - Начать поиск",
            "/profil - Мой профиль",
            "/start - Начать диалог",
            "/create - Создать профиль",
            "/stop_searching - Включить невидимку",
            "/lets_search - Выключить невидимку",
            "/help - Получить справку",
            "",
            'В центр поддержки можете обратиться через "мой профиль (/profil) ➡️ другое ➡️ оставить пожелание"'
            )
    await message.answer("\n".join(text))

# @dp.message_handler(commands='get_login')
# async def bot_help(message: types.Message):
#
#     await message.answer(f'Привет, вот твои данные для входа на сайт'
#                          f'\nЛогин : {message.chat.id},\n Пароль : 1234')


# начало создания профиля
@dp.message_handler(commands='create', state=None)
async def create_my_profil(message : types.Message):

    # await Registration.name.set()
    # await message.answer('Как ты хочешь, чтобы отображалось твое имя?')

    identity = await verify_user(message.chat.id)

    if message.chat.id == 1087882216:
        identity = 10

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
        but3 = InlineKeyboardButton('Данные для входа на сайт', callback_data='login')
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


@dp.message_handler(commands='stop_search', state=None)
async def send_search(message : types.Message):
    await stop_searching(False, message.chat.id)
    await message.answer('Ценим твое желание побыть одному/ой 😌 твой профиль не будет виден другим в течении '
                                      '2 недель, чтобы вновь стать видимым нажми 👉🏼 /lets_search')


# Снова делает невидимого ("спящего") пользователя видимым
@dp.message_handler(commands='be_admin', state=None)
async def send_search(message : types.Message):

    await message.answer('Введите код доступа:')
    await BeAdmin.begin.set()


# Ответ на рандомное сообщение
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer("Алоха 😇🌴🐼\n"
                         "Поиск --  /search\n"
                         "Профиль -- /profil"
                    )
