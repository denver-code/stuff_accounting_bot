from io import BytesIO
from aiogram import types, dispatcher, Dispatcher
import cv2
import numpy as np
from bot.core.api import get, post, verify_token
from bot.core.barcode_reader import retval_code
from bot.core.email_validate import is_valid_email
from bot.core.hash import sha256_encode
from bot.core.middlewares import auth_required, auto_fetch
from bot.core.redis_db import get_user, is_token_exist, logout, set_user
from bot.states.add import AddByUPC, AddByUPCPicture
from bot.states.authorisation import AuthToken, Authorisation, Registration


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


@auth_required
async def add_by_upc_picture_event(message: types.Message, state: dispatcher.FSMContext):
    await state.finish()
    _message = await message.answer('Thank you!\nLet me moment to parse data from picture')

    photo_io = BytesIO()
    await message.photo[-1].download(destination_file=photo_io)
    photo_io.seek(0)
    img = cv2.imdecode(np.frombuffer(photo_io.read(), np.uint8), 1)
    ret_code = retval_code(img)
    if ret_code[0] != 200:
        return await _message.edit_text(ret_code[1])
    await _message.edit_text('Let me moment to check if we have information about this item.')    

    _token = is_token_exist(str(message.from_id))
    _request = get(f"/api/v1/private/items/upc/{ret_code[1]}", _token)
    if _request.status_code != 200:
        return await _message.edit_text('Looks like we can\'t get information about this item, please make sure you have a correct UPC') 
       
    await _message.edit_text(f"{_request.json()['title']} has been added successfully")


@auth_required
@auto_fetch
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
    _items = "\n\n- ".join(_result)
    await _message.edit_text(f"Look's that you already have some stuff:\n- {_items}")


async def email_registration_event(message: types.Message, state: dispatcher.FSMContext):
    _message = await message.answer('Thank you!')
    if not is_valid_email(message.text):
        await message.delete()
        return await _message.edit_text('Entered email are invalid, please try again.')    

    async with state.proxy() as data:
        data["email"] = message.text
        data["message"] = _message
        await message.delete()
        await Registration.next()
    await _message.edit_text('Fine! Now we need password.')

async def password_registration_event(message: types.Message, state: dispatcher.FSMContext):
    async with state.proxy() as data:
        await message.delete()
        _message = data["message"]
        await _message.edit_text('Fabulous! Wait while we process everything.')
        _result = post("/api/v1/public/authorisation/signup", body={
            "email": data["email"],
            "password": sha256_encode(message.text)
        })
        await state.finish()
    if _result.status_code != 200:
        return await _message.edit_text(f"Error: {_result.json()['detail']}")
    _token = _result.json()["token"]
    if verify_token(_token):
       set_user(message.from_id, {"token":_token})
       return await _message.edit_text('Welcome, mate!\nNow you\'re able to use all functions, use command /fetch to refresh your local profile.\nUse /help to get all other information')



async def email_authorisation_event(message: types.Message, state: dispatcher.FSMContext):
    _message = await message.answer('Thank you!')
    if not is_valid_email(message.text):
        await message.delete()
        return await _message.edit_text('Entered email are invalid, please try again.')    

    async with state.proxy() as data:
        data["email"] = message.text
        data["message"] = _message
        await message.delete()
        await Authorisation.next()
    await _message.edit_text('Fine! Now we need password.')

async def password_authorisation_event(message: types.Message, state: dispatcher.FSMContext):
    async with state.proxy() as data:
        await message.delete()
        _message = data["message"]
        await _message.edit_text('Fabulous! Wait while we process everything.')
        _result = post("/api/v1/public/authorisation/signin", body={
            "email": data["email"],
            "password": sha256_encode(message.text)
        })
        await state.finish()
    if _result.status_code != 200:
        return await _message.edit_text(f"Error: {_result.json()['detail']}")
    _token = _result.json()["token"]
    if verify_token(_token):
       set_user(message.from_id, {"token":_token})
       return await _message.edit_text('Welcome, mate!\nNow you\'re able to use all functions, use command /fetch to refresh your local profile.\nUse /help to get all other information')


def setup(dp: Dispatcher):
    dp.register_message_handler(set_token_event, content_types=['text'], state=AuthToken.token)
    dp.register_message_handler(email_registration_event, content_types=['text'], state=Registration.email)
    dp.register_message_handler(password_registration_event, content_types=['text'], state=Registration.password)
    dp.register_message_handler(email_authorisation_event, content_types=['text'], state=Authorisation.email)
    dp.register_message_handler(password_authorisation_event, content_types=['text'], state=Authorisation.password)
    dp.register_message_handler(add_by_upc_event, content_types=['text'], state=AddByUPC.upc_code)
    dp.register_message_handler(add_by_upc_picture_event, content_types=['photo'], state=AddByUPCPicture.upc_picture)
    dp.register_message_handler(add_by_upc_picture_event, content_types=['photo'], state='*')
    dp.register_message_handler(message_event, content_types=['text'], state='*')