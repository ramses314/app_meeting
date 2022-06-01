from asyncio import sleep

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from db.create_db import *
from keyboards.kb_admin import send_admins_from_kb
from keyboards.kb_profil import *
from keyboards.kb_auth import *
from keyboards.kb_search import send_next_search
from loader import bot
from states.registration import *


# Распределитель колбеков от панели на просмотре профиля
@dp.callback_query_handler(Text(startswith='check'))
async def send_admins(callback : types.CallbackQuery):

    await send_admins_from_kb(callback)
