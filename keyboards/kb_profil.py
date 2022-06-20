from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, KeyboardButton, ReplyKeyboardMarkup

from db.function_db import send_db_sick


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
    but7 = InlineKeyboardButton('Моя проблема', callback_data="edit_disease")
    but8 = InlineKeyboardButton('Степень боли', callback_data="edit_pain")
    but9 = InlineKeyboardButton('О себе', callback_data="edit_indy")
    but10 = InlineKeyboardButton('Фото', callback_data="edit_photo")
    butx = InlineKeyboardButton('Назад', callback_data="profil_same")
    return markup.row(but1, but2).row(but3, but4).row(but5, but6).row(but7, but8).row(but10, but9).row(butx)


async def send_gender_for_edit(callback : types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Мужской', callback_data="redact_парень")
    but2 = InlineKeyboardButton('Женский', callback_data="redact_девушка")
    # but3 = InlineKeyboardButton('Другое 🧬', callback_data="redact_другое")
    markup.row(but1, but2)
    await callback.message.answer('Выбери свой пол', reply_markup=markup)
    await callback.answer()


async def send_personality_for_edit(callback : types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Экстраверт', callback_data="redact_экстраверт")
    but2 = InlineKeyboardButton('Интроверт', callback_data="redact_интроверт")
    but3 = InlineKeyboardButton('Амбиветр', callback_data="redact_амбиветр")
    markup.row(but1, but3, but2)
    await callback.message.answer('Какой у тебя тип характера', reply_markup=markup)


async def send_pain_for_edit(callback : types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('1', callback_data="redact_1")
    but2 = InlineKeyboardButton('2', callback_data="redact_2")
    but3 = InlineKeyboardButton('3', callback_data="redact_3")
    but4 = InlineKeyboardButton('4', callback_data="redact_4")
    but5 = InlineKeyboardButton('5', callback_data="redact_5")
    but6 = InlineKeyboardButton('6', callback_data="redact_6")
    but7 = InlineKeyboardButton('7', callback_data="redact_7")
    but8 = InlineKeyboardButton('8', callback_data="redact_8")
    but9 = InlineKeyboardButton('9', callback_data="redact_9")
    but10 = InlineKeyboardButton('10', callback_data="redact_10")
    markup.row(but1, but2, but3, but4, but5).row(but6, but7, but8, but9, but10)
    await callback.message.answer('Оцени свою боль по десятибальной шкале 😔', reply_markup=markup)


async def send_disease_for_edit(callback : types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Выбрать заново', callback_data="change_edit")
    but2 = InlineKeyboardButton('Добавить симптом', callback_data="change_add")
    markup.row(but1, but2)
    await callback.message.answer('Ты хочешь выбрать заново свою проблему или добавить симптом? 🙄', reply_markup=markup)


async def send_disease_for_redact(callback : types.CallbackQuery, value):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Физические', callback_data=f"change_physical_{value}")
    but2 = InlineKeyboardButton('Психологнические', callback_data=f"change_crazy_{value}")
    markup.row(but1, but2)
    await callback.message.edit_text('Какого рода проблема?', reply_markup=markup)
    await callback.answer()


async def send_disease_some_for_redact(callback : types.CallbackQuery, type_of_table):
    markup = InlineKeyboardMarkup()
    a = await send_db_sick(type_of_table)

    for i in a:
        but = InlineKeyboardButton(f'{i[1]}', callback_data=f'SR_{i[1]}_{callback.data.split("_")[2]}')
        markup.row(but)
    but_x = InlineKeyboardButton('Назад', callback_data='edit_disease')
    markup.row(but_x)

    await callback.message.edit_text('выбери подпункт', reply_markup=markup)
    await callback.answer()


async def send_other_for_profil(callback : types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Оставить пожелание, жалобу, просьбу', callback_data=f"other_review")
    but2 = InlineKeyboardButton('Остановить серчинг', callback_data=f"other_stop")
    but3 = InlineKeyboardButton('Назад', callback_data=f"profil_same")
    markup.row(but1).row(but2).row(but3)
    await callback.message.edit_caption('Выбери', reply_markup=markup)
    await callback.answer()