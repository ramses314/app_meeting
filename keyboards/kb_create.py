from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, KeyboardButton, ReplyKeyboardMarkup

from db.function_db import send_db_sick


async def send_gender(message : types.Message):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Мужской', callback_data="mch2_парень_gender")
    but2 = InlineKeyboardButton('Женский', callback_data="mch2_девушка_gender")
    # but3 = InlineKeyboardButton('Другое 🧬', callback_data="mch2_другое_gender")
    markup.row(but1, but2)
    await message.answer('Теперь выбери свой пол', reply_markup=markup)


async def send_personality(callback : types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Экстраверт', callback_data="mch3_экстраверт")
    but2 = InlineKeyboardButton('Интроверт', callback_data="mch3_интроверт")
    but3 = InlineKeyboardButton('Амбиветр', callback_data="mch3_амбиветр")
    markup.row(but1, but3, but2)
    await callback.message.edit_text('Какой у тебя тип характера? 🤔'
                                     '\n\nAмбиверт – это человек, которому свойственны '
                                     'проявления поведения и интроверта, и экстраверта.', reply_markup=markup)


async def send_disease(callback : types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Физические', callback_data="mch3_physical")
    but2 = InlineKeyboardButton('Психологнические', callback_data="mch3_crazy")
    markup.row(but1, but2)
    await callback.message.edit_text('С какой сложностью ты столкнулся? 🥺 Выбери одну основную проблему, потом ты сможешь '
                                      'добавить дополнительные симптомы', reply_markup=markup)
    await callback.answer()


async def send_disease_some(callback : types.CallbackQuery, type_of_table):
    markup = InlineKeyboardMarkup()
    a = await send_db_sick(type_of_table)
    for i in a:
        but = InlineKeyboardButton(f'{i[1]}', callback_data=f'mch4_{i[1]}')
        markup.row(but)
    but_x = InlineKeyboardButton('Назад', callback_data='mch3_null')
    markup.row(but_x)
    await callback.message.edit_text('Выбери подпункт 💁🏼‍♀️', reply_markup=markup)
    await callback.answer()


async def send_scale_of_pain(callback : types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('1', callback_data="mch5_1")
    but2 = InlineKeyboardButton('2', callback_data="mch5_2")
    but3 = InlineKeyboardButton('3', callback_data="mch5_3")
    but4 = InlineKeyboardButton('4', callback_data="mch5_4")
    but5 = InlineKeyboardButton('5', callback_data="mch5_5")
    but6 = InlineKeyboardButton('6', callback_data="mch5_6")
    but7 = InlineKeyboardButton('7', callback_data="mch5_7")
    but8 = InlineKeyboardButton('8', callback_data="mch5_8")
    but9 = InlineKeyboardButton('9', callback_data="mch5_9")
    but10 = InlineKeyboardButton('10', callback_data="mch5_10")
    markup.row(but1, but2, but3, but4, but5).row(but6, but7, but8, but9, but10)
    await callback.message.edit_text('Оцени свою боль по десятибальной шкале 😔', reply_markup=markup)


async def send_phone(message : types.Message):
    but_1 = KeyboardButton('👉🏼 Поделиться контактом 👈🏼', request_contact=True)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(but_1)
    await message.answer('Теперь поделись контактом для будущей верификации (нажми на кнопку ниже)👇🏼👇🏼👇🏼', reply_markup=markup)


async def send_ending(message : types.Message):
    markup = InlineKeyboardMarkup()
    but_1 = InlineKeyboardButton('Принимаю', callback_data='yes')
    but_2 = InlineKeyboardButton('Отказываюсь', callback_data='no')
    markup.add(but_1, but_2)
    await message.answer('❗️Помни, что в интернете люди могут выдавать себя за других и '
                         'опубликовывать недостоверную информацию. Продолжая ты соглашаешься с '
                         'возможными рисками и сам за себя несешь ответсвенность.', reply_markup=markup)




# Ниже на случай если пользователь не хочет загружать свое фото
# Сомневаюсь добавлять это в функционал, так как если появиться такая возможность, есть вероятность,
# что все станут ей пользоваться
# async def send_for_not_photo(message : types.Message):
#     markup = InlineKeyboardMarkup()
#     but1 = InlineKeyboardButton('Стесняюсь себя', callback_data="nofoto")
#     but2 = InlineKeyboardButton('Не люблю фотаться', callback_data="nofoto")
#     but3 = InlineKeyboardButton('Не хочу', callback_data="nofoto")
#     but4 = InlineKeyboardButton('Не важно', callback_data="nofoto")
#     markup.row(but1, but2, but4)
#     await message.answer('По какой причине не хочешь?', reply_markup=markup)
#
# async def send_for_not_photo_two(message : types.Message):
#     markup = InlineKeyboardMarkup()
#     but1 = InlineKeyboardButton('Животные', callback_data="nofoto")
#     but2 = InlineKeyboardButton('Аниме', callback_data="nofoto")
#     but3 = InlineKeyboardButton('Эмоджи', callback_data="nofoto")
#     markup.row(but1, but2, but3)
#     await message.answer('Ничего страшного, ты имеешь на это право, выбери лучше, какая тема тебе больше нравиться', reply_markup=markup)


