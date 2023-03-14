from aiogram.dispatcher.filters.state import State, StatesGroup

class AddByUPC(StatesGroup):
    upc_code = State()