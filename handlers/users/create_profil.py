import random
import string

import psycopg2

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from data.config import *
from db.function_db import insert_login_web
from keyboards.kb_create import *
from loader import dp
from states.registration import Registration



@dp.message_handler(state=Registration.name)
async def ask_age(message: types.Message, state:FSMContext):

    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer('Сколько тебе лет?')
    await Registration.next()


@dp.message_handler(state=Registration.age)
async def ask_place(message: types.Message, state: FSMContext):

    if message.text.isdigit():
        if int(message.text) in range(18,100):
            async with state.proxy() as data:
                data['age'] = message.text

            await message.answer('Напиши свою страну и город через одну запятую\n'
                                 '*Например: "Россия, москва"*', parse_mode=ParseMode.MARKDOWN)
            await Registration.next()
        else:
            await message.answer('Введите корректный возраст 😅\nОн должен быть в промежутке 18-99 лет')
    else:
        await message.answer('Введите корректный возраст 😅\nОн должен быть в промежутке 18-99 лет')


@dp.message_handler(state=Registration.place)
async def ask_gender(message: types.Message, state: FSMContext):

    if len(message.text.split(',')) == 2:
        async with state.proxy() as data:
            data['country'] = message.text.split(',')[0]
            data['city'] = message.text.split(',')[1]
        await Registration.next()
        await send_gender(message)
    else:
        await message.answer('Внимание, страна и город должны разделяться одной запятой 🤓')


@dp.callback_query_handler(Text(startswith='mch2'),state=Registration.gender)
async def ask_personality(callback : types.CallbackQuery, state : FSMContext):

    async with state.proxy() as data:
        data['gender'] = callback.data.split('_')[1]

        await send_personality(callback)
        await Registration.next()


@dp.callback_query_handler(Text(startswith='mch3'), state=Registration.personality)
async def ask_diseas(callback: types.CallbackQuery, state: FSMContext):

    a = callback.data.split('_')[1]

    if a not in ('physical', 'crazy', 'null'):
        async with state.proxy() as data:
            data['personality'] = a

    if a == 'physical':
        await send_disease_some(callback, 'p')
    elif a == 'crazy':
        await send_disease_some(callback, 'c')
    else:
        await send_disease(callback)


@dp.callback_query_handler(Text(startswith='mch4'), state=Registration.personality)
async def ask_diseas(callback: types.CallbackQuery, state: FSMContext):

    # может придумать более элегантное решение???
    if callback.data.split('_')[1] == 'Зависимость':
        await send_disease_some(callback, 'a')
    elif callback.data.split('_')[1] == 'др. расстройства личности':
        await send_disease_some(callback, 'd')
    else:
        async with state.proxy() as data:
            data['disease'] = callback.data.split('_')[1]
        await send_scale_of_pain(callback)
        await Registration.next()


@dp.callback_query_handler(Text(startswith='mch5'), state=Registration.disease)
async def asc_personality(callback: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        data['scale_of_pain'] = callback.data.split('_')[1]
        # переменная внизу для проверки количества выполнения следующией функции в машине состояний
        # (иначе, если юзер отправляет несколько фотографий, все ломается!)
        data['check_for_photo'] = 0

    await Registration.next()
    await callback.message.edit_text('Выбери одну самую классную фотку 🔥🔥🔥')


# Можно добавить функционал, если пользователь не хочет выставлять свое фото (сомневаюсь нужно ли)
# @dp.message_handler(commands='nofoto', state=Registration.photo)
# async def ask_name(message : types.Message):
#
#     await send_for_not_photo(message)
#
# @dp.callback_query_handler(Text(startswith='nofoto'), state=Registration.photo)
# async def asc_personality(callback: types.CallbackQuery, state: FSMContext):
#
#     await send_for_not_photo_two(callback.message)


@dp.message_handler(content_types=['photo'], state=Registration.photo)
async def ask_desk (message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        data['check_for_photo'] = data['check_for_photo'] + 1

    if data['check_for_photo'] == 1:
        await message.answer('Напиши 1-2 предложения о себе: что тебе нравится и что беспокоит 💁🏼‍♀️')
        await Registration.next()


@dp.message_handler(state=Registration.desc_disease)
async def ask_contact(message : types.Message, state : FSMContext):

    async with state.proxy() as data:
        data['desc_disease'] = message.text
    await send_phone(message)
    await Registration.next()


@dp.message_handler(content_types=['contact'],  state=Registration.phone)
async def save_and_warning(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.contact.phone_number
    await send_ending(message)
    await Registration.next()


@dp.callback_query_handler(state=Registration.end)
async def send_happyend(callback: types.CallbackQuery, state: FSMContext):

    if callback.data == 'yes':
        async with state.proxy() as data:

            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )

            cursor = connection.cursor()
            a = data["name"]
            b = data["age"]
            c = data["country"]
            d = data["city"]
            e = data["gender"]
            f = data["personality"]
            g = data["disease"]
            k = data["scale_of_pain"]
            l = data["photo"]
            m = data["phone"]
            n = callback.message.chat.id
            o = data['desc_disease']


            with connection.cursor() as cur:
                cur.execute(f"INSERT INTO main_profil (name, age, country, city, gender, personality , disease,"
                            f"pain, photo, phone, indx, indy) VALUES ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}',"
                            f" '{k}', '{l}', '{m}', '{n}', '{o}')"
                            )

                cur.execute('UPDATE statistic SET all_user = all_user + 1 WHERE id = 1')
                connection.commit()
            await callback.message.delete()
            await callback.message.answer(text='Ну вот и все 🥳 ищи единомышлеников 👉🏼 /search',
                                          reply_markup=types.ReplyKeyboardRemove())

            letter1 = random.choice(string.ascii_letters)
            letter2 = random.choice(string.ascii_letters)
            passw = letter1 + letter2 + str(random.randint(1000, 9999))
            await insert_login_web(n, passw, m)
            await state.finish()
    else:
        await callback.message.delete()
        await callback.message.answer(text='Хорошо, твои данные не сохранены. Если что всегда рады тебя видеть 😋', reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
