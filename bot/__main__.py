import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor       
from aiogram.dispatcher import FSMContext
from bot.core.config import settings
from bot.handlers import message_handlers 
from bot.handlers import commands_handlers
from bot.handlers import callback_handlers
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=settings.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# @dp.message_handler(state='*', commands='cancel')
# @dp.message_handler("cancel", state='*')
# async def cancel_handler(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.finish()
#     await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())

if __name__ == '__main__':
    commands_handlers.setup(dp)
    message_handlers.setup(dp)
    callback_handlers.setup(dp)
    executor.start_polling(dp, skip_updates=True)
