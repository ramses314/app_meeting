from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, KeyboardButton, ReplyKeyboardMarkup

from db.create_db import send_db_sick, select_admin


async def send_admin_panel(message : types.Message):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('админы', callback_data="check_admin")
    but2 = InlineKeyboardButton('статистика', callback_data="mch2_девушка_gender")
    but3 = InlineKeyboardButton('удалить пользователя', callback_data="mch2_другое_gender")
    but4 = InlineKeyboardButton('блокировка', callback_data="mch2_парень_gender")
    but5 = InlineKeyboardButton('анкеты жалобы', callback_data="mch2_девушка_gender")
    but6 = InlineKeyboardButton('общие жалобы', callback_data="mch2_другое_gender")
    but7 = InlineKeyboardButton('Парень', callback_data="mch2_парень_gender")
    but8 = InlineKeyboardButton('Девушка', callback_data="mch2_девушка_gender")
    but9 = InlineKeyboardButton('Другое', callback_data="mch2_другое_gender")
    markup.row(but1, but2).row(but3, but4).row(but5, but6)
    await message.answer('Выбери нужные действия', reply_markup=markup)


async def send_admins_from_kb(callback : types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Отправить сообщение админам', callback_data="check_admin")
    but2 = InlineKeyboardButton('удалить админа', callback_data="check_admin")
    but3 = InlineKeyboardButton('показать код доступа', callback_data="check_admin")
    but4 = InlineKeyboardButton('Назад', callback_data="check_admin")
    markup.row(but1, but2).row(but3).row(but4)

    selected = await select_admin()
    text = ['Список админов:',]

    for i in selected:
        text.append(f'1. {i[1]}, ${i[2]}$')

    await callback.message.edit_text('\n'.join(text), reply_markup=markup)
