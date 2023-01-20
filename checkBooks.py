import requests
from datetime import datetime, timedelta
import json
import asyncio
import model


async def checkAvailableBooks(bookId, interval, bot):
    while True:
        current_datetime = datetime.now()
        target_datetime = current_datetime + timedelta(days=31)
        URL_TEMPLATE = f"https://ambasada-r-moldova-in-f-rusa.reservio.com/api/v2/businesses/09250556-2450-437f-aede-82e78712f114/availability/booking-days?filter[from]={current_datetime.date()}T{current_datetime.time()}&filter[resourceId]=&filter[serviceId]={bookId}&filter[to]={target_datetime.date()}T{target_datetime.time()}"
        try:
            r = requests.get(URL_TEMPLATE, headers={"Content-Type":"application/json", "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"})
            dictData = json.loads(r.text)
            available = False
            nearestDate = ""
            for data in dictData["data"]:
                if data["attributes"]["isAvailable"]:
                    if not available:
                        available = True
                        nearestDate = data["attributes"]["date"]
                        date_time_obj = datetime.strptime(nearestDate, '%Y-%m-%d')
                        nearestDate = date_time_obj.strftime('%d.%m.%Y')
            if available:
                chatIdArray = getChatIdArray(bookId)
                message = f"Доступна запись в посольство на {nearestDate}\nhttps://ambasada-r-moldova-in-f-rusa.reservio.com/services/{bookId}"
                if not chatIdArray == None:
                    for chatId in chatIdArray:
                        await send_message(bot, chatId, message)
                        model.cancelSubscribe(bookId, chatId)
        # except:
        #     raise
        finally:
            # return
            await asyncio.sleep(interval)
            # await checkAvailableBooks (bookId, interval, bot)
            continue

def getChatIdArray(bookId):
    with open("data.json", "r", encoding='utf8') as file:
        bookData = json.load(file)
        if bookId in bookData:
            return bookData[bookId]["users"]
        else: return None

async def send_message(bot, chatId, text):
    await bot.send_message(chatId,text)