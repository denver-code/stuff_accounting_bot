from aiogram import types, dispatcher, Dispatcher
from bot.core.api import get, verify_token
from bot.core.redis_db import get_user, is_token_exist, set_user
from bot.states.add import AddByUPC
from bot.states.authorisation import AuthToken

async def set_token_event(message: types.Message, state: dispatcher.FSMContext):
    _message = await message.answer('Thank you!\nLet me moment to verify your token.')
    await message.delete()
    await state.finish()

    if verify_token(message.text):
       set_user(message.from_id,{"token":message.text})
       return await _message.edit_text('Welcome, mate!\nNow you\'re able to use all functions, use command /fetch to refresh your local profile.\nUse /help to get all other information')

    await _message.edit_text('Looks like your token are invalid, please try again.')    


async def add_by_upc_event(message: types.Message, state: dispatcher.FSMContext):
    _message = await message.answer('Thank you!\nLet me moment to check if we have information about this item.')
    _token = is_token_exist(str(message.from_id))
    _request = get(f"/api/v1/private/items/upc/{message.text}", _token)
    if _request.status_code != 200:
        return await _message.edit_text('Looks like we can\'t get information about this item, please make sure you have a correct UPC')    
    await state.finish()
    await _message.edit_text(f"{_request.json()['title']} has been added successfully")



async def message_event(message: types.Message, state: dispatcher.FSMContext):
    _message = await message.answer('Hi!\nI\'ll check your request a soon as posible!')
    # 
    user = get_user(message.from_id)

    # result = next((item for item in user["saved"] if message.text.lower() in item["title"].lower()), None)
    result = list(filter(lambda item: message.text.lower() in item["title"].lower(), user["saved"]))
    if not result:
        return await _message.edit_text("Looks like you don't have this item in your collection.\nIf you think that's misstake, try something from this list:\n\
1. Change your search querry\n2. Make sure your querry are correct\nIf you still have this issue - use /issue to report about your problem.\n\
You also can add new item using command /add")
    _result = []
    for _i in result:
        _result.append(_i["title"])
    _items = "\n".join(_result)
    await _message.edit_text(f"Look's that you already have some stuff:\n{_items}")


def setup(dp: Dispatcher):
    dp.register_message_handler(set_token_event, content_types=['text'], state=AuthToken.token)
    dp.register_message_handler(add_by_upc_event, content_types=['text'], state=AddByUPC.upc_code)
    dp.register_message_handler(message_event, content_types=['text'], state='*')

#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmUiOjE2ODAyODQ1NTIuMTY1MzE0LCJlbWFpbCI6ImNzaWdvcmVrQGdtYWlsLmNvbSJ9.c-qDfg_BAgd5WBLRYPtXyEaeHWNiuNAVfc3wLZ5qqg0