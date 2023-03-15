from aiogram.dispatcher.filters.state import State, StatesGroup

class AuthToken(StatesGroup):
    token = State()

class Registration(StatesGroup):
    email = State()
    password = State()