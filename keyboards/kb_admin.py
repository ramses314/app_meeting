from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, KeyboardButton, ReplyKeyboardMarkup

from db.function_db import send_db_sick, select_admin, check_claims, check_wishes, send_search_db, send_profil
from loader import bot


async def send_admin_panel(message : types.Message, some):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Админы', callback_data="check_admins")
    but2 = InlineKeyboardButton('Статистика', callback_data="check_statistic")
    but3 = InlineKeyboardButton('block/del пользователя', callback_data="check_block")
    but4 = InlineKeyboardButton('Жалобы на анкеты', callback_data="check_claims_0")
    but5 = InlineKeyboardButton('Общие пожелания-жалобы ', callback_data="check_wishes_0")
    but6 = InlineKeyboardButton("Активировать 'спящих'", callback_data="check_activate")

    markup.row(but1, but2).row(but3, but4).row(but5, but6)
    if some == 'editing':
        await message.edit_text('Выбери нужные действия', reply_markup=markup)
    else:
        await message.answer('Выбери нужные действия', reply_markup=markup)


async def send_admins_from_kb(callback : types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Отправить сообщение админам', callback_data="admins_sendmessage")
    but2 = InlineKeyboardButton('Удалить админа', callback_data="admins_deleteadmin")
    but3 = InlineKeyboardButton('Показать код доступа', callback_data="admins_showpass")
    but4 = InlineKeyboardButton('Назад', callback_data="check_same")
    markup.row(but1, but2).row(but3).row(but4)

    selected = await select_admin()
    text = ['Список админов:',]
    number = 1
    for i in selected:
        text.append(f'{number}. {i[1]}, chat_id : {i[2]};')
        number += 1
    await callback.message.edit_text('\n'.join(text), reply_markup=markup)
    await callback.answer()


async def send_block(callback : types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Удалить', callback_data="do_delete")
    but2 = InlineKeyboardButton('Заблочить', callback_data="do_block")
    but3 = InlineKeyboardButton('Разблочить', callback_data="do_unblock")
    but4 = InlineKeyboardButton('Назад', callback_data="do_same")
    markup.row(but1, but2, but3).row(but4)
    await callback.message.edit_text('Выбери нужное действие', reply_markup=markup)


async  def send_claims(callback : types.CallbackQuery,  check):
    claims = await check_claims(check)
    print(3434, claims)
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Удалить жалобу', callback_data=f"check_delclaim_{check}_{claims[2]}")
    but2 = InlineKeyboardButton('Заблочить', callback_data=f"check_claimbl_{check + 1}_{claims[2]}")
    but3 = InlineKeyboardButton('Пропустить', callback_data=f"check_claims_{check + 1}")
    but4 = InlineKeyboardButton('Назад', callback_data="check_stop")
    markup.row(but1, but2, but3).row(but4)
    await callback.message.delete()
    if claims == 'pop':
        await callback.message.answer('Список жалоб пуст /admin')
    else:
        a = (await send_profil(claims[2]))[0]
        text = [f'*Профиль из ЖАЛОБЫ:🔻\n**{a[1]}*, *{a[2]}*, {a[6]}',
                f'*Чувствую себя на {a[8]} из 10*',
                f'*Моя проблема*: {a[7]}',
                f'"{a[12]}"',
                f'\nЖалоба : {claims[1]}\nОставил жалобу : {claims[3]}']

        await bot.send_photo(callback.message.chat.id, a[9], caption='\n'.join(text), parse_mode=ParseMode.MARKDOWN,
                             reply_markup=markup)
        await callback.answer()


async def send_wishes(callback : types.CallbackQuery, check):

    wishes = await check_wishes(check)
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Удалить', callback_data=f"check_delwishes_{check}_{wishes[0]}")
    but2 = InlineKeyboardButton('Ответить', callback_data=f"check_answish_{check + 1}_{wishes[2]}_{wishes[0]}")
    but3 = InlineKeyboardButton('Пропустить', callback_data=f"check_wishes_{check + 1}")
    but4 = InlineKeyboardButton('Назад', callback_data="check_same")
    markup.row(but1, but2, but3).row(but4)

    if wishes == 'empty':
        await callback.message.edit_text('Список жалоб-пожеланий пуст /admin')
    else:
        await callback.message.edit_text(f"Сообщние : '{wishes[1]}'\nОт пользователя : {wishes[2]}", reply_markup=markup)
        await callback.answer()
