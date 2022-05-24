import psycopg2
from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Text

from data.config import *
from db.create_db import send_profil, update_profil
from keyboards.inline.kb_profil import send_panel_profil_for_edit
from keyboards.kb_auth import *
from loader import dp, bot
from states.registration import Registration, EditingProfil


@dp.callback_query_handler(Text(startswith='profil'))
async def send_full_profil(callback : types.CallbackQuery):
    value = callback.data.split('_')[1]
    if value == 'all':
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
    elif value == 'edit':
        a = await send_panel_profil_for_edit()
        await callback.message.edit_reply_markup(reply_markup=a)
    elif value == 'same':
        a = (await send_profil(callback.message.chat.id))[0]
        markup = InlineKeyboardMarkup()
        but1 = InlineKeyboardButton('Смотреть все параметры', callback_data="profil_all")
        but2 = InlineKeyboardButton('другое', callback_data="profil_null")
        markup.row(but1).row(but2)

        text = [f'*{a[1]}* - {a[2]} года',
                f'*характер*: {a[6]}',
                f'*Моя проблема*: {a[7]}',
                '"Здесь пара слов о том, как мне  нелегко, думаю это сообщение можно ограничить 100 символами"'
                ]

        await callback.message.edit_caption(caption='\n'.join(text), reply_markup=markup)


@dp.callback_query_handler(Text(startswith='edit'), state=None)
async def editing_profil(callback : types.CallbackQuery, state : FSMContext):
    value = callback.data.split('_')[1]

    if value == 'name':
        await EditingProfil.begin.set()
        await callback.message.delete()
        await callback.message.answer('Введити новое имя для вашего профиля')
        async with state.proxy() as data:
            data['value'] = value


    elif value == 'age':
        await callback.message.delete()
        await EditingProfil.begin.set()
        await callback.message.answer('Введити новый возраст для вашего профиля')
        async with state.proxy() as data:
            data['value'] = value

    elif value == 'country':
        await callback.message.delete()
        await EditingProfil.begin.set()
        await callback.message.answer('Введити новую страну для вашего профиля')
        async with state.proxy() as data:
            data['value'] = value

    elif value == 'city':
        await callback.message.delete()
        await EditingProfil.begin.set()
        await callback.message.answer('Введити новый город для вашего профиля')
        async with state.proxy() as data:
            data['value'] = value

    elif value == 'gender':
        await send_gender(callback.message)
    elif value == 'personality':
        pass
    elif value == 'disease':
        pass
    elif value == 'pain':
        await callback.message.delete()
        await EditingProfil.begin.set()
        await callback.message.answer('Введите новое значение того как ты себя чувствуешь')
        async with state.proxy() as data:
            data['value'] = value
    elif value == 'indy':
        await callback.message.delete()
        await EditingProfil.begin.set()
        await callback.message.answer('Введите новое описание себя')
        async with state.proxy() as data:
            data['value'] = value

@dp.message_handler(state=EditingProfil.begin)
async def save(message : types.Message, state : FSMContext):

    async with state.proxy() as data:
        a = data['value']
        print(a)

        if a in ('name', 'age', 'country', 'city', 'pain', 'indy'):

            await update_profil(data['value'], message.text, message.chat.id)

            await message.answer('Профиль успешно отредактирован)))')

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

            await bot.send_photo(message.from_user.id, a[9], caption='\n'.join(text), parse_mode=ParseMode.MARKDOWN,
                                 reply_markup=markup)
            await state.finish()
        elif a == 'gender':
            pass






