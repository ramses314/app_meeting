from asyncio import sleep

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from db.create_db import *
from keyboards.kb_profil import *
from keyboards.kb_auth import *
from keyboards.kb_search import send_next_search
from loader import bot
from states.registration import *


# Распределитель колбеков от панели на просмотре профиля
@dp.callback_query_handler(Text(startswith='search'))
async def send_search(callback : types.CallbackQuery):
    split = callback.data.split('_')[1]
    own_profil = (await send_profil(callback.message.chat.id))

    if own_profil[0][15] != '1':
        if split == 'go':
            selected = (await send_search_db(callback.message.chat.id, own_profil[0][7].split(',\n'), own_profil[0][13]))
            await send_next_search(callback, selected)
        elif split == 'heart':
            selected = (await send_search_db(callback.message.chat.id, own_profil[0][7].split(',\n'), own_profil[0][13]))
            await callback.message.answer('Симпатия отправлена ❤️')
            await sleep(1)
            await send_next_search(callback, selected)
        else:
            await callback.message.delete()
            await callback.message.answer('Всего хорошего)))\n/search\n/profil')
    else:
        await callback.message.delete()
        await reset_search(callback.message.chat.id)
        await callback.message.answer('На сегодня люди схожими с вашими проблемами кончились /search')


@dp.callback_query_handler(Text(startswith='claim'))
async def rise_claim(callback : types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Коротко опиши в чем проблема, мы проверим этот профиль')
    await Claim.begin.set()


# Доделать хэндоер (админка)
@dp.message_handler(state=Claim.begin)
async def claim_complite(message : types.Message, state : FSMContext):
    await message.answer('Спасибо за помощь, благодаря тебе это место будет чище и добрее)))'
                         '\nПродолжить поиск /search')
    await state.finish()

