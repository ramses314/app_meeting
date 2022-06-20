from asyncio import sleep

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from db.function_db import *
from keyboards.kb_create import *
from keyboards.kb_search import send_next_search
from loader import bot
from states.registration import *



# Распределитель колбеков от панели на просмотре профиля
# (как-то громоздко, позже вернуться и попытаться найти более простое решение)
@dp.callback_query_handler(Text(startswith='search'))
async def send_search(callback : types.CallbackQuery):
    split = callback.data.split('_')[1]
    own_profil = (await send_profil(callback.message.chat.id))

    if own_profil[0][15] != 1:
        if split == 'go':
            selected = (await send_search_db(callback.message.chat.id, own_profil[0][7].split(',\n'), own_profil[0][13]))
            await send_next_search(callback, selected)
        elif split == 'heart':
            selected = (await send_search_db(callback.message.chat.id, own_profil[0][7].split(',\n'), own_profil[0][13]))
            chat_id = callback.data.split('_')[2]

            text = [f'*{own_profil[0][1]}*, *{own_profil[0][2]}*, {own_profil[0][6]}',
                    f'*Чувствую себя на {10 - int(own_profil[0][8])} из 10*',
                    f'*Моя проблема*: {own_profil[0][7]}',
                    f'"{own_profil[0][12]}"',
                    f"\nТы можешь [👉🏼 написать 👈🏼](tg://user?id={callback.message.chat.id})"
                        ]
            try:
                await bot.send_photo(chat_id=chat_id, photo=own_profil[0][9], caption='\n'.join(text),
                                 parse_mode=ParseMode.MARKDOWN)
                await bot.send_message(chat_id=chat_id, text=f"👆🏼 Пользователь проявил к тебе интерес\n/stop_search -- сделать перерыв")
            except:
                pass
            await callback.message.answer('Симпатия отправлена ❤️')
            await sleep(0.7)
            await send_next_search(callback, selected)

        else:
            # await callback.message.delete()
            await callback.message.answer('Всего хорошего)))\n/search\n/profil')
    else:
        if split == 'heart':
            chat_id = callback.data.split('_')[2]
            text = [f'*{own_profil[0][1]}*, *{own_profil[0][2]}*, {own_profil[0][6]}',
                    f'*Чувствую себя на {10 - int(own_profil[0][8])} из 10*',
                    f'*Моя проблема*: {own_profil[0][7]}',
                    f'"{own_profil[0][12]}"',
                    f"\nТы можешь [👉🏼 написать 👈🏼](tg://user?id={callback.message.chat.id})"
                    ]
            try:
                await bot.send_photo(chat_id=chat_id, photo=own_profil[0][9], caption='\n'.join(text),
                                 parse_mode=ParseMode.MARKDOWN)
                await bot.send_message(chat_id=chat_id, text=f"👆🏼 Пользователь проявил к тебе интерес\n/stop_search -- сделать перерыв")
            except:
                pass
            await callback.message.answer('Симпатия отправлена ❤️')
            await reset_search(callback.message.chat.id)
            # await callback.message.delete()
            # await callback.message.answer('На сегодня люди с схожими с вашими проблемами кончились /search')

        await callback.message.delete()
        await reset_search(callback.message.chat.id)
        await callback.message.answer('На сегодня люди с схожими с вашими проблемами кончились /search')


@dp.callback_query_handler(Text(startswith='claim'))
async def rise_claim(callback : types.CallbackQuery, state : FSMContext):

    own_profil = (await send_profil(callback.message.chat.id))
    if own_profil[0][15] == 1:
        await reset_search(callback.message.chat.id)

    await callback.message.delete()
    await Claim.begin.set()
    async with state.proxy() as data:
        data['quilty'] = callback.data.split('_')[1]
    await callback.message.answer('Коротко опиши в чем проблема, мы проверим этот профиль')


# хэндоер (админка)
@dp.message_handler(state=Claim.begin)
async def claim_complite(message : types.Message, state : FSMContext):

    async with state.proxy() as data:
        await insert_claims(message.text, data['quilty'], message.chat.id)

    await message.answer('Спасибо за помощь, благодаря тебе это место будет чище и добрее)))'
                         '\nПродолжить поиск /search')
    await state.finish()

