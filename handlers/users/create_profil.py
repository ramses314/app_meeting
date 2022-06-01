from asyncio import sleep

import psycopg2

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from data.config import *
from keyboards.kb_auth import *
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
        if int(message.text) in range(14,100):
            async with state.proxy() as data:
                data['age'] = message.text

            await message.answer('Напиши свою страну и город через одну запятую\n'
                                 '*Например: "Россия, москва"*', parse_mode=ParseMode.MARKDOWN)
            await Registration.next()
        else:
            await message.answer('Введите корректный возраст 😅\nОн должен быть в промежутке 14-100 лет')
    else:
        await message.answer('Введите корректный возраст 😅\nОн должен быть в промежутке 14-100 лет')


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
        data['gender'] = callback.data

# интровертность
        await send_personality(callback)
        await Registration.next()


@dp.callback_query_handler(Text(startswith='mch3'), state=Registration.personality)
async def ask_diseas(callback: types.CallbackQuery, state: FSMContext):

    a = callback.data.split('_')[1]

    if a not in ('physical', 'crazy'):
        async with state.proxy() as data:
            data['personality'] = a

    if a == 'physical':
        await send_disease_some(callback, 'f')
    elif a == 'crazy':
        await send_disease_some(callback, 'crazy')
    else:
        await send_disease(callback)


@dp.callback_query_handler(Text(startswith='mch4'), state=Registration.personality)
async def ask_diseas(callback: types.CallbackQuery, state: FSMContext):

    print(2222222222, callback.data.split('_')[1])
    # может придумать более элегантное решение???
    if callback.data.split('_')[1] != 'Зависимость':
        async with state.proxy() as data:
            data['disease'] = callback.data.split('_')[1]

        await send_scale_of_pain(callback)
        await Registration.next()
    else:
        await send_disease_addiction(callback)


@dp.callback_query_handler(Text(startswith='mch5'), state=Registration.disease)
async def asc_personality(callback: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        data['scale_of_pain'] = callback.data.split('_')[1]
        # переменная внизу для проверки количества выполнения следующией в машине состояний
        # функции (иначе, если юзер отправляет несколько фотографий, все ломается!)
        data['check_for_photo'] = 0

    await Registration.next()
    await callback.message.edit_text('Выбери одну самую классную фотку 🤩  🔥🔥🔥')


@dp.message_handler(content_types=['photo'], state=Registration.photo)
async def ask_desk (message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        data['check_for_photo'] = data['check_for_photo'] + 1

    if data['check_for_photo'] == 1:
        await message.answer('Напиши 1-2 предложения о себе: что тебе нравится и что беспокоит))')
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
    n = message.chat.id
    o = data['desc_disease']

    with connection.cursor() as cur:
        cur.execute(f"INSERT INTO main_profil (name, age, country, city, gender, personality , disease,"
                    f"pain, photo, phone, indx, indy) VALUES ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}',"
                    f" '{k}', '{l}', '{m}', '{n}', '{o}')"
                    )
        connection.commit()

    # await message.delete()
    await message.answer('Сообщение-предупреждение')
    await message.answer('Ну вот и все 🥳 ищи единомышлеников 👉🏼 /search')
    await state.finish()

