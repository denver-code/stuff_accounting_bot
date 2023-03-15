from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from bot.states.authorisation import AuthToken, Registration
from bot.states.add import AddByUPC, AddByUPCPicture

async def token_auth_callback_handler(callback_query: CallbackQuery):
    await AuthToken.token.set()
    await callback_query.message.answer("Please paste your Authorisation Token from platform.\nPlease note that message will be deleted because of security methods, and will be stored in-bot cache memory.")
    await callback_query.message.delete()


async def create_account_callback_handler(callback_query: CallbackQuery):
    await Registration.email.set()
    await callback_query.message.answer("Please enter email which will be used for access to the platform.")
    await callback_query.message.delete()


async def ucp_code_callback_handler(callback_query: CallbackQuery):
    await AddByUPC.upc_code.set()
    await callback_query.message.answer("Please enter your UPC code.\nPlease note that we could not find your product, in that case you will need create item by yourself")
    await callback_query.message.delete()


async def ucp_code_picture_callback_handler(callback_query: CallbackQuery):
    await AddByUPCPicture.upc_picture.set()
    await callback_query.message.answer("Please send picture of your UPC barcode.\nPlease note that we could not find your product, in that case you will need create item by yourself")
    await callback_query.message.delete() 


async def custom_item_callback_handler(callback_query: CallbackQuery):
    await callback_query.message.answer("Yo! This function are not implemented yet, please come back later.")
    await callback_query.message.delete() 


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(token_auth_callback_handler, lambda c: c.data == "login_via_token")
    dp.register_callback_query_handler(create_account_callback_handler, lambda c: c.data == "create_account")
    dp.register_callback_query_handler(ucp_code_callback_handler, lambda c: c.data == "create_using_upc")
    dp.register_callback_query_handler(ucp_code_picture_callback_handler, lambda c: c.data == "create_using_upc_picture")
    dp.register_callback_query_handler(custom_item_callback_handler, lambda c: c.data == "create_custom_item")