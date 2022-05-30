
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
async def send_full_profil(callback : types.CallbackQuery):
    own_profil = (await send_profil(callback.message.chat.id))[0][7]
    selected = (await send_search_db(callback.message.chat.id, own_profil.split(',\n')))
    await send_next_search(callback, selected, callback.data.split('_')[1])