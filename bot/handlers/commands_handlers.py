from aiogram import types, dispatcher, Dispatcher
from bot.core.redis_db import is_token_exist
from bot.core.api import verify_token


async def start_event(message: types.Message, state: dispatcher.FSMContext):
    _message = await message.answer('Please wait while we check your authorisation data.')
    _token = is_token_exist(str(message.from_id))
    if _token and verify_token(_token):
        await _message.edit_text('Welcome, mate!')
    else:
        buttons = [
            types.InlineKeyboardButton(text='Create Account', callback_data='create_account'),
            types.InlineKeyboardButton(text='Login to Account', callback_data='login_to_account'),
            types.InlineKeyboardButton(text='Auth via API Token', callback_data='login_via_token')
        ]
        keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
        keyboard_markup.add(*buttons)

        return await _message.edit_text('Welcome, do you have account?', reply_markup=keyboard_markup)
    


def setup(dp: Dispatcher):
    dp.register_message_handler(start_event, commands=["start"], state='*')