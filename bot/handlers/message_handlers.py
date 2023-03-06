from aiogram import types, dispatcher, Dispatcher
from bot.core.api import verify_token
from bot.states.authorisation import AuthToken

async def set_token_event(message: types.Message, state: dispatcher.FSMContext):
    _message = await message.answer('Thank you!\nLet me moment to verify your token.')
    await message.delete()
    await state.finish()

    if verify_token(message.text):
       return await _message.edit_text('Welcome, mate!\nNow you\'re able to use all functions, use command /fetch to refresh your local profile.\nUse /help to get all other information')

    await _message.edit_text('Looks like your token are invalid, please try again.')    


async def message_event(message: types.Message, state: dispatcher.FSMContext):
    await message.answer('Hi!\nI\'ll check your request a soon as posible!')


def setup(dp: Dispatcher):
    dp.register_message_handler(set_token_event, content_types=['text'], state=AuthToken.token)
    dp.register_message_handler(message_event, content_types=['text'], state='*')

#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmUiOjE2ODAyODQ1NTIuMTY1MzE0LCJlbWFpbCI6ImNzaWdvcmVrQGdtYWlsLmNvbSJ9.c-qDfg_BAgd5WBLRYPtXyEaeHWNiuNAVfc3wLZ5qqg0