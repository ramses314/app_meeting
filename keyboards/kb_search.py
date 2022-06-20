from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode

from loader import bot


async def send_first_search(message : types.Message, selected):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('жалоба 🤭', callback_data=f"claim_{selected[11]}")
    but2 = InlineKeyboardButton('❤️', callback_data=f"search_heart_{selected[11]}")
    but3 = InlineKeyboardButton('дальше', callback_data="search_go")
    but4 = InlineKeyboardButton('стоп', callback_data=f"search_stop")
    markup.row(but1, but2, but3).row(but4)

    text = [
        f'*{selected[1]}, {selected[2]}*, {selected[6]}',
        f"*Чувствую себя на {10 - int(selected[8])} из 10*",
        f"*Моя проблема*: {selected[7]}",
        f'"{selected[12]}"'
    ]

    await bot.send_photo(message.chat.id, selected[9], caption='\n'.join(text), parse_mode=ParseMode.MARKDOWN,
                         reply_markup=markup)


async def send_next_search(callback : types.CallbackQuery, selected):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('жалоба 🤭', callback_data=f"claim_{selected[11]}")
    but2 = InlineKeyboardButton('❤️', callback_data=f"search_heart_{selected[11]}")
    but3 = InlineKeyboardButton('дальше', callback_data=f"search_go")
    but4 = InlineKeyboardButton('стоп', callback_data=f"search_stop")
    markup.row(but1, but2, but3).row(but4)

    text = [
        f'*{selected[1]}, {selected[2]}*, {selected[6]}',
        f"*Чувствую себя на {10 - int(selected[8])} из 10*",
        f"*Моя проблема*: {selected[7]}",
        f'"{selected[12]}"'
    ]

    await callback.message.delete()
    await bot.send_photo(callback.message.chat.id, selected[9], caption='\n'.join(text), parse_mode=ParseMode.MARKDOWN,
                         reply_markup=markup)

