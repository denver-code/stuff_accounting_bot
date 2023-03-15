from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from bot.states.authorisation import AuthToken
from bot.states.add import AddByUPC

async def token_auth_callback_handler(callback_query: CallbackQuery):
    await AuthToken.token.set()
    await callback_query.message.answer("Please paste your Authorisation Token from platform.\nPlease note that message will be deleted because of security methods, and will be stored in-bot cache memory.")
    await callback_query.message.delete()


async def ucp_code_callback_handler(callback_query: CallbackQuery):
    await AddByUPC.upc_code.set()
    await callback_query.message.answer("Please enter your UPC code.\nPlease note that we could not find your product, in that case you will need create item by yourself")
    await callback_query.message.delete()


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(token_auth_callback_handler, lambda c: c.data == "login_via_token")
    dp.register_callback_query_handler(ucp_code_callback_handler, lambda c: c.data == "create_using_upc")