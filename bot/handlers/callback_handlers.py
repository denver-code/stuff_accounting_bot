from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from bot.states.authorisation import AuthToken

async def token_auth_callback_handler(callback_query: CallbackQuery):
    await AuthToken.token.set()
    await callback_query.message.answer("Please paste your Authorisation Token from platform.\nPlease note that message will be deleted because of security methods, and will be stored in-bot cache memory.")
    await callback_query.message.delete()


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(token_auth_callback_handler, lambda c: c.data == "login_via_token")