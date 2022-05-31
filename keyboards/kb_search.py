from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, KeyboardButton, ReplyKeyboardMarkup

from db.create_db import send_db_sick
from loader import bot


async def send_first_search(message : types.Message, selected):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('жалоба 🤭', callback_data="claim")
    # but2 = InlineKeyboardButton('❤️ + сообщение', callback_data="edit_age")
    but3 = InlineKeyboardButton('❤️', callback_data="search_heart")
    but4 = InlineKeyboardButton('дальше', callback_data="search_go")
    but5 = InlineKeyboardButton('стоп', callback_data="search_stop")
    markup.row(but1, but3, but4).row(but5)

    # text = [
    #     f'{selected[0][1]}, {selected[0][2]}',
    #     f'{selected[0][6]}',
    #     f"Моя проблема: {selected[0][7]}",
    #     f"Мне плохо на {selected[0][8]} из 10",
    #     f'"{selected[0][12]}"'
    # ]
    print(selected)
    text = [
        f'{selected[1]}, {selected[2]}',
        f'{selected[6]}',
        f"Моя проблема: {selected[7]}",
        f"Мне плохо на {selected[8]} из 10",
        f'"{selected[12]}"'
    ]

    await bot.send_photo(message.chat.id, selected[9], caption='\n'.join(text), parse_mode=ParseMode.MARKDOWN,
                         reply_markup=markup)


async def send_next_search(callback : types.CallbackQuery, selected):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('жалоба 🤭', callback_data="claim")
    # but2 = InlineKeyboardButton('❤️ + сообщение', callback_data="edit_age")
    but3 = InlineKeyboardButton('❤️', callback_data=f"search_heart")
    but4 = InlineKeyboardButton('дальше', callback_data=f"search_go")
    but5 = InlineKeyboardButton('стоп', callback_data=f"search_stop")
    markup.row(but1, but3, but4).row(but5)

    # text = [
    #     f'{selected[c][1]}, {selected[c][2]}',
    #     f'{selected[c][6]}',
    #     f"Моя проблема: {selected[c][7]}",
    #     f"Мне плохо на {selected[c][8]} из 10",
    #     f'"{selected[c][12]}"'
    # ]
    text = [
        f'{selected[1]}, {selected[2]}',
        f'{selected[6]}',
        f"Моя проблема: {selected[7]}",
        f"Мне плохо на {selected[8]} из 10",
        f'"{selected[12]}"'
    ]

    await callback.message.delete()
    await bot.send_photo(callback.message.chat.id, selected[9], caption='\n'.join(text), parse_mode=ParseMode.MARKDOWN,
                         reply_markup=markup)

