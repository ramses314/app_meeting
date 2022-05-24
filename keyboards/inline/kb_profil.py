from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, KeyboardButton, ReplyKeyboardMarkup

from db.create_db import send_db_sick


async def send_panel_profil():
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Смотреть все настройки', callback_data="mch2_парень")
    but2 = InlineKeyboardButton('Корректировтаь', callback_data="mch2_девушка")
    return markup.row(but1).row(but2)

async def send_panel_profil_for_edit():
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Имя', callback_data="edit_name")
    but2 = InlineKeyboardButton('Возраст', callback_data="edit_age")
    but3 = InlineKeyboardButton('Страна', callback_data="edit_country")
    but4 = InlineKeyboardButton('Город', callback_data="edit_city")
    but5 = InlineKeyboardButton('Пол', callback_data="edit_gender")
    but6 = InlineKeyboardButton('Характер', callback_data="edit_personality")
    but7 = InlineKeyboardButton('Болезнь', callback_data="edit_disease")
    but8 = InlineKeyboardButton('Степень боли', callback_data="edit_pain")
    butx = InlineKeyboardButton('Назад', callback_data="profil_same")
    but9 = InlineKeyboardButton('Описание', callback_data="edit_indy")
    # but10 = InlineKeyboardButton('Корректировтаь', callback_data="mch2_девушка")
    return markup.row(but1, but2).row(but3, but4).row(but5, but6).row(but7, but8).row(but9).row(butx)