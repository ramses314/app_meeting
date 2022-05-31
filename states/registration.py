from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp

class Registration(StatesGroup):
    name = State()
    age = State()
    place = State()
    gender = State()
    # drags = State()
    # religion = State()
    personality = State()
    disease = State()
    photo = State()
    desc_disease = State()
    phone = State()

class EditingProfil(StatesGroup):
    begin = State()
    save = State()

class ProfilOther(StatesGroup):
    begin = State()

class Claim(StatesGroup):
    begin = State()