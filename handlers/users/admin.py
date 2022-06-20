from asyncio import sleep

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from db.function_db import *
from keyboards.kb_admin import send_admins_from_kb, send_block, send_claims, send_admin_panel, send_wishes
from keyboards.kb_create import *
from loader import bot
from states.registration import *



# Распределитель колбеков панели админа
@dp.callback_query_handler(Text(startswith='check'))
async def send_admins(callback : types.CallbackQuery, state : FSMContext):

    split = callback.data.split('_')[1]

# Список админов, статистика, (бан \ разбан пользователей)
    if split == 'admins':
        await send_admins_from_kb(callback)
    elif split == 'statistic':
        statistic = await collect_statistic()
        markup = InlineKeyboardMarkup().row(InlineKeyboardButton('Назад', callback_data="check_same"))
        # text = [
        #     f'👤 Общее кол-во пользователей: {statistic[1]}',
        #     f'😴 Кол-во спящих пользователей: {statistic[2]}'
        # ]
        await callback.message.edit_text('\n'.join(statistic), reply_markup=markup)
    elif split == 'block':
        await send_block(callback)
        await ForAdmin.begin.set()
        async with state.proxy() as data:
            data['what_do'] = 'block/unblock'
# Просмотр жалоб на анкеты
    elif split == 'claims':
        check = int(callback.data.split('_')[2])
        await send_claims(callback, check)
    elif split == 'claimbl':
        check = int(callback.data.split('_')[2])
        await delete_block_user('block', callback.data.split('_')[3])
        await callback.message.answer('Пользователь заблокирован')
        await send_claims(callback, check)
    elif split == 'delclaim':
        check = int(callback.data.split('_')[2])
        await delete_claims(callback.data.split('_')[3])
        await callback.message.answer('Жалоба удалена')
        await send_claims(callback, check)
# Просмотр общих жалоб и пожеланий
    elif split == 'wishes':
        check = int(callback.data.split('_')[2])
        await send_wishes(callback, check)
    elif split == 'delwishes':
        print(callback.data)
        check = int(callback.data.split('_')[2])
        await delete_wishes(callback.data.split('_')[3])
        await callback.message.answer('Удалено из списка')
        await send_wishes(callback, check)
    elif split == 'answish':
        print(callback.data)
        await delete_wishes(callback.data.split('_')[4])
        check = int(callback.data.split('_')[2])
        await callback.message.edit_text('Напишите текст пользователю')
        await ForAdmin.begin.set()
        async with state.proxy() as data:
            data['chat_id'] = callback.data.split('_')[3]
            data['what_do'] = 'send_wishes'
# Работа кнопки "назад"
    elif split == 'same':
        await send_admin_panel(callback.message, 'editing')
    elif split == 'stop':
        await callback.message.delete()
        await send_admin_panel(callback.message, 'first')
# Активирует пользователей, которые отключили свою видимость на месяц
    elif split == 'activate':
        await callback.message.answer('Пользователи выведлены из тени')
        await activate_users()
        await callback.answer()

# Реализация функций находящиеся в кнопке "админы"
@dp.callback_query_handler(Text(startswith='admins'))
async def do_some(callback : types.CallbackQuery, state : FSMContext):

    split = callback.data.split('_')[1]

    if split == 'sendmessage':
        await callback.message.answer('Введите сообщение для всех админов')
        await ForAdmin.begin.set()
        await callback.answer()
        async with state.proxy() as data:
            data['what_do'] = 'send_message'
    elif split == 'showpass':
        await callback.message.answer('Код доступа: 7891')
        await callback.answer()
    elif split == 'deleteadmin':
        await callback.message.answer('Введи цифру удаляемого админа')
        await ForAdmin.begin.set()
        await callback.answer()
        async with state.proxy() as data:
            data['what_do'] = 'del_admin'
    elif split == 'default':
        await admin_default(callback.message.chat.id)
        await callback.message.answer('Произведен дефолт админского аккаунта')


@dp.callback_query_handler(Text(startswith='do'), state=ForAdmin.begin)
async def do_some(callback : types.CallbackQuery, state : FSMContext):

    split = callback.data.split('_')[1]

    if split in ('delete','block', 'unblock'):
        async with state.proxy() as data:
            data['some'] = split
        await callback.message.edit_text('Укажи его chat_id')
    if split == 'same':
        await state.finish()
        await send_admin_panel(callback.message, 'editing')


@dp.message_handler(state=ForAdmin.begin)
async def do_some(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        if data['what_do'] == 'send_wishes':
            text = ['🤓 Ответ администратора на ваше сообщение:',
                       f"'{message.text}'"]
            await bot.send_message(chat_id=data['chat_id'], text='\n'.join(text))
            await message.answer('Сообщение отправлено /admin')
            await state.finish()
        elif data['what_do'] == 'send_message':
            selected = await select_admin()
            for i in selected:
                text = ['📌 Сообщение для всех админов:',
                           f'"{message.text}"']
                await bot.send_message(chat_id=i[2], text='\n'.join(text))
                await state.finish()
        elif data['what_do'] == 'del_admin':
            try:
                x = int(message.text)
            except:
                x = False
            selected = await select_admin()
            if x:
                number = 1
                if int(message.text) <= len(selected):
                    for i in selected:
                        our_admin = i[2]
                        if number == x:
                            break
                        number += 1
                    await delete_admin(our_admin)
                    await message.answer('админ удален')
                else:
                    await message.answer('Неверные данные')
            else:
                await message.answer('Неверные данные')

        else:
            if len(message.text) == 10:
                await delete_block_user(data['some'], message.text)
                await message.answer(f'Пользователь status : {data["some"]}')

            else:
                await message.answer('Вы неправильно указали chat_id\n/admin')
        await state.finish()


# Регистрация адимна
@dp.message_handler(state=BeAdmin.begin)
async def send_search(message: types.Message, state : FSMContext):

    if message.text == '7891':
        if message.from_user.username:
            await make_admin(message.from_user.username, message.chat.id)
        else:
            await make_admin('someadmin', message.chat.id)
        await message.answer('Поздравляем, теперь вы админ /admin')
    else:
        await message.answer('Неверный код доступа')
    await state.finish()


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием (удалить????)
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    # state = await state.get_state()
    await message.answer(f"Ерунда")
    await state.finish()
