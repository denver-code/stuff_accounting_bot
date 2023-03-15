from aiogram import types, dispatcher, Dispatcher
from bot.core.fetch import fetch
from bot.core.middlewares import auth_required, auto_fetch
from bot.core.redis_db import get_user, is_token_exist, set_user
from bot.core.api import get, verify_token


async def start_event(message: types.Message, state: dispatcher.FSMContext):
    _message = await message.answer('Please wait while we check your authorisation data.')
    _token = is_token_exist(str(message.from_id))
    if _token and verify_token(_token):
        await _message.edit_text('Welcome, mate!\nNow you\'re able to use all functions, use command /fetch to refresh your local profile.\nUse /help to get all other information')
    else:
        buttons = [
            types.InlineKeyboardButton(text='Create Account', callback_data='create_account'),
            types.InlineKeyboardButton(text='Login to Account', callback_data='login_to_account'),
            types.InlineKeyboardButton(text='Auth via API Token', callback_data='login_via_token')
        ]
        keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
        keyboard_markup.add(*buttons)

        return await _message.edit_text('Welcome, do you have account?', reply_markup=keyboard_markup)
    

@auth_required
async def fetch_event(message: types.Message, state: dispatcher.FSMContext):
    _message = await message.answer('Please wait while we fetch your data.')
    fetch(message)
    await _message.edit_text("We're succefully got your data! Type /my or /collection to check your collection.")


@auth_required
@auto_fetch
async def display_in_bot_profile_event(message: types.Message, state: dispatcher.FSMContext):
    _message = await message.answer('Please wait till we fetch your data.')
    user = get_user(message.from_id)
    await _message.edit_text(user)


@auth_required
@auto_fetch
async def my_collection_event(message: types.Message, state: dispatcher.FSMContext):
    _message = await message.answer('Please wait till we get your data.')
    user = get_user(message.from_id)
    _saved = []
    for item in user["saved"]:
        _saved.append(item["title"])
    _items = "\n\n- ".join(_saved)
    await _message.edit_text(f"Your Collection:\n- {_items}")


@auth_required
async def add_new_event(message: types.Message, state: dispatcher.FSMContext):
    buttons = [
        types.InlineKeyboardButton(text='Custom Item', callback_data='create_custom_item'),
        types.InlineKeyboardButton(text='UPC', callback_data='create_using_upc'),
        types.InlineKeyboardButton(text='UPC(Picture)', callback_data='create_using_upc_picture'),
    ]
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    keyboard_markup.add(*buttons)
    await message.answer('Please select method of creating:\nAlso just want to let you know that you cannot change item details created via UPC.', reply_markup=keyboard_markup)


def setup(dp: Dispatcher):
    dp.register_message_handler(start_event, commands=["start"], state='*')
    dp.register_message_handler(fetch_event, commands=["fetch"], state='*')
    dp.register_message_handler(display_in_bot_profile_event, commands=["in-bot-profile"], state='*')
    dp.register_message_handler(my_collection_event, commands=["my", "collection"], state='*')
    dp.register_message_handler(add_new_event, commands=["add", "new", "create"], state='*')