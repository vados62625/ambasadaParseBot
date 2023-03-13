from aiogram import Bot, Dispatcher, executor
import handlers
from tokenTG import TOKEN
from checkBooks import checkAvailableBooks
import asyncio
import model
import time

API_TOKEN = TOKEN
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.register_message_handler(handlers.start, commands=["start"])
dp.register_message_handler(handlers.selectServices, commands=["selectservices"])
dp.register_message_handler(handlers.showSelectedServices, commands=["showselectedservices"])
dp.register_message_handler(handlers.selectServiceToUnsubscribe, commands=["removeservice"])
dp.register_message_handler(handlers.echo)
dp.register_callback_query_handler(handlers.subscribeService, lambda c: c.data and c.data.startswith('subscribeService'))
dp.register_callback_query_handler(handlers.unsubscribeService, lambda c: c.data and c.data.startswith('unsubscribeService'))

async def send_message(chatId, text):
    await bot.send_message(chatId,text)
# asyncio.run(checkAvailableBooks ("8e13743d-076d-4aa0-b0c2-c8d3c2b64de2", 300, bot))
# loop = asyncio.new_event_loop()
# asyncio.ensure_future(checkAvailableBooks ("8e13743d-076d-4aa0-b0c2-c8d3c2b64de2", 10, bot))
# loop.run_in_executor(checkAvailableBooks ("8e13743d-076d-4aa0-b0c2-c8d3c2b64de2", 10, bot))
# checkAvailableBooks ("8e13743d-076d-4aa0-b0c2-c8d3c2b64de2", 10, bot)
if __name__ == '__main__':
    for service in model.getServicesAr():
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        asyncio.ensure_future(checkAvailableBooks(service, 180, bot))
        time.sleep(1)
        # asyncio.sleep(10)
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    asyncio.ensure_future(executor.start_polling(dp, skip_updates=False))
