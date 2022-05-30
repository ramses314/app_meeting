from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, KeyboardButton, ReplyKeyboardMarkup

from db.create_db import send_db_sick
from loader import bot


async def send_first_search(message : types.Message, selected):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('жалоба 🤭', callback_data="edit_name")
    # but2 = InlineKeyboardButton('️💔', callback_data="edit_age")
    but3 = InlineKeyboardButton('❤️', callback_data="edit_city-country")
    but4 = InlineKeyboardButton('дальше', callback_data="search_0")
    but5 = InlineKeyboardButton('стоп', callback_data="ыу")
    markup.row(but1, but3, but4).row(but5)

    text = [
        f'{selected[0][1]}, {selected[0][2]}',
        f'{selected[0][6]}',
        f"Моя проблема: {selected[0][7]}",
        f"Мне плохо на {selected[0][8]} из 10",
        f'"{selected[0][12]}"'
    ]

    await bot.send_photo(message.chat.id, selected[0][9], caption='\n'.join(text), parse_mode=ParseMode.MARKDOWN,
                         reply_markup=markup)


async def send_next_search(callback : types.CallbackQuery, selected, c):
    c = int(c) + 1
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('жалоба 🤭', callback_data="edit_name")
    # but2 = InlineKeyboardButton('❤️ + сообщение', callback_data="edit_age")
    but3 = InlineKeyboardButton('❤️', callback_data="edit_city-country")
    but4 = InlineKeyboardButton('дальше', callback_data=f"search_{c}")
    but5 = InlineKeyboardButton('стоп', callback_data="ыу")
    markup.row(but1, but3, but4).row(but5)

    text = [
        f'{selected[c][1]}, {selected[c][2]}',
        f'{selected[c][6]}',
        f"Моя проблема: {selected[c][7]}",
        f"Мне плохо на {selected[c][8]} из 10",
        f'"{selected[c][12]}"'
    ]

    await callback.message.delete()
    await bot.send_photo(callback.message.chat.id, selected[c][9], caption='\n'.join(text), parse_mode=ParseMode.MARKDOWN,
                         reply_markup=markup)

