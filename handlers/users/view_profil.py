import psycopg2
from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Text

from data.config import *
from db.create_db import *
from keyboards.inline.kb_profil import *
from keyboards.kb_auth import *
from loader import dp, bot
from states.registration import *

# Шаблоны
async def shablon_send_new_profil(message):
    a = (await send_profil(message.chat.id))[0]
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Смотреть все параметры', callback_data="profil_all")
    but2 = InlineKeyboardButton('другое', callback_data="other_bull")
    markup.row(but1).row(but2)
    text = [f'*{a[1]}* - {a[2]} года',
            f'*характер*: {a[6]}',
            f'*Моя проблема*: {a[7]}',
            f'"{a[12]}"'
            ]
    await bot.send_photo(message.chat.id, a[9], caption='\n'.join(text), parse_mode=ParseMode.MARKDOWN,
                         reply_markup=markup)


# Распределитель колбеков от панели на просмотре профиля
@dp.callback_query_handler(Text(startswith='profil'))
async def send_full_profil(callback : types.CallbackQuery):
    value = callback.data.split('_')[1]
    if value == 'all':
        async def shablon(callback):
            a = (await send_profil(callback.message.chat.id))[0]
            markup = InlineKeyboardMarkup()
            but1 = InlineKeyboardButton('Редактировать', callback_data="profil_edit")
            but2 = InlineKeyboardButton('назад', callback_data="profil_same")
            markup.row(but1).row(but2)

            text = [f'Имя - {a[1]}',
                    f'Возраст - {a[2]}',
                    f'Страна - {a[3]}',
                    f'Город - {a[4]}',
                    f'Пол - {a[5]}',
                    f'Характер - {a[6]}',
                    f'болезнь - {a[7]}',
                    f'Уровень боли - {a[8]}'
                    ]
            await callback.message.edit_caption(caption='\n'.join(text), reply_markup=markup)
        await shablon(callback)
    elif value == 'edit':
        a = await send_panel_profil_for_edit()
        await callback.message.edit_reply_markup(reply_markup=a)
    elif value == 'same':
        a = (await send_profil(callback.message.chat.id))[0]
        markup = InlineKeyboardMarkup()
        but1 = InlineKeyboardButton('Смотреть все параметры', callback_data="profil_all")
        but2 = InlineKeyboardButton('другое', callback_data="other_")
        markup.row(but1).row(but2)

        text = [f'*{a[1]}* - {a[2]} года',
                f'*характер*: {a[6]}',
                f'*Моя проблема*: {a[7]}',
                '"Здесь пара слов о том, как мне  нелегко, думаю это сообщение можно ограничить 100 символами"'
                ]

        await callback.message.edit_caption(caption='\n'.join(text), parse_mode=ParseMode.MARKDOWN, reply_markup=markup)


# Начала редактирования профиля (!!! нужно добавить валидацию данных !!!)
@dp.callback_query_handler(Text(startswith='edit'), state=None)
async def editing_profil(callback : types.CallbackQuery, state : FSMContext):
    value = callback.data.split('_')[1]

    if value in ('name', 'age', 'country', 'city-country', 'indy'):
        dict = {'name': 'имя', 'age': 'возраст', 'city-country': 'город и страну через 1 запятую', 'indy': 'описание себя'}
        async with state.proxy() as data:
            data['value'] = value
        await EditingProfil.begin.set()
        await callback.message.delete()
        await callback.message.answer(f'Введити новое {dict[value]} для вашего профиля')
    elif value in ('gender', 'personality', 'pain', 'disease'):
        await callback.message.delete()
        await EditingProfil.begin.set()
        await globals()[f'send_{value}_for_edit'](callback)
        async with state.proxy() as data:
            data['value'] = value


# сохранение редактирования messahe_handler
@dp.message_handler(state=EditingProfil.begin)
async def save(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        value = data['value']

        if value == 'age':
            if message.text.isdigit():
                if int(message.text) in range(0, 99):
                    await update_profil(data['value'], message.text, message.chat.id)
                    await message.answer('Профиль успешно отредактирован)))')
                    await shablon_send_new_profil(message)
                    await state.finish()
                else:
                    await message.answer('ВВеди корректный возраст')
            else:
                await message.answer('ВВеди корректный возраст')
        elif value == 'city-country':
            if len(message.text.split(',')) == 2:
                await update_profil('country', message.text.split(',')[0], message.chat.id)
                await update_profil('city', message.text.split(',')[1], message.chat.id)
                await message.answer('Профиль успешно отредактирован)))')
                await shablon_send_new_profil(message)
                await state.finish()
            else:
                await message.answer('Вы ошиблись, давайтк еще раз')
        else:
            await update_profil(data['value'], message.text, message.chat.id)
            await message.answer('Профиль успешно отредактирован)))')
            await shablon_send_new_profil(message)
            await state.finish()


# Сохранение редактирования выбора (callback-и)
@dp.callback_query_handler(Text(startswith='redact'), state=EditingProfil.begin)
async def save_for_callback(callback : types.CallbackQuery, state : FSMContext):

    async with state.proxy() as data:
        await update_profil(data['value'], callback.data.split('_')[1], callback.message.chat.id)
        await callback.message.delete()
        await callback.message.answer('Профиль успешно отредактирован)))')
        await shablon_send_new_profil(callback.message)
        await state.finish()


# Развлетвление редактирования выбора болезни
@dp.callback_query_handler(Text(startswith='change'), state=EditingProfil.begin)
async def edit_disease_choise_1(callback : types.CallbackQuery, state : FSMContext):

    value = callback.data.split('_')[1]

    if value == 'edit':
        await send_disease_for_redact(callback, value)
    elif value == 'add':
        await send_disease_for_redact(callback, value)
    elif value == 'physical':
        await send_disease_some_for_redact(callback, 'f')
    elif value == 'crazy':
        await send_disease_some_for_redact(callback, 'crazy')
    else:
        await send_disease_for_redact(callback)


# Сохранение редактирования выбора болезни
@dp.callback_query_handler(Text(startswith='SR'), state=EditingProfil.begin)
async def edit_disease_choise_1(callback : types.CallbackQuery, state : FSMContext):
    async with state.proxy() as data:

        if callback.data.split('_')[2] == 'edit':
            await update_profil(data['value'], callback.data.split('_')[1], callback.message.chat.id)
            await callback.message.delete()
            await callback.message.answer('Профиль успешно отредактирован)))')
            await shablon_send_new_profil(callback.message)
            await state.finish()
        elif callback.data.split('_')[2] == 'add':
            await update_profil_add(data['value'], callback.data.split('_')[1], callback.message.chat.id)
            await callback.message.delete()
            await callback.message.answer('Профиль успешно отредактирован)))')
            await shablon_send_new_profil(callback.message)
            await state.finish()


# Развертывание клавиши "другое"
@dp.callback_query_handler(Text(startswith='other'))
async def save_for_callback(callback : types.CallbackQuery, state : FSMContext):

    a = callback.data.split('_')[1]

    if a == 'review':
        await callback.message.answer('Напишите в одном сообщениии ваше дело. "Для дела" (с) Игорь Кайнара')
        await ProfilOther.begin.set()
    elif a == 'stop':
        await callback.message.answer('Мы ценим ваше желание побыть одной, ваш профиль не буудет виден други на протяжении'
                                      '30 дней, если хотите, чтобы вы вновь искались нажим на команду -> /search')
    else:
        await send_other_for_profil(callback)


@dp.message_handler(state=ProfilOther.begin)
async def send_review(message : types.Message, state : FSMContext):
    await message.answer('Благодарим, за помощь, мы учтем твое мнение')
    await state.finish()