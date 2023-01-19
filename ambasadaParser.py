import requests
from bs4 import BeautifulSoup as bs
# import pandas as pd
import json

def showAvailibleServices ():
    servicesDict = {}
    data = ''
    URL_TEMPLATE = f"https://ambasada-r-moldova-in-f-rusa.reservio.com/"
    r = requests.get(URL_TEMPLATE, headers={"Content-Type":"application/json", "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"})

    soup = bs(r.text, "html.parser")

    jsonData = soup.find_all('script', id='__NEXT_DATA__')
    for name in jsonData:
        data = json.loads(name.text)

    for key in data["props"]["pageProps"]["initialApolloState"]:
        if key.startswith("service"):
            servicesDict[data["props"]["pageProps"]["initialApolloState"][key]["id"]] = {"name":data["props"]["pageProps"]["initialApolloState"][key]["description"].partition('ВАЖНО')[0]}
        # with open("data.json", "w", encoding='utf8') as file:
        #     json.dump(servicesDict, file, ensure_ascii=False, indent=4)

    return servicesDict

def subscribeService(serviceId, message):
    saveToFile(serviceId, message.from_user.id)
    return serviceId

def saveToFile (serviceId, chatId):
    with open("data.json", "r", encoding='utf8') as file:
        servicesData = json.load(file)
        if not serviceId in servicesData:
            servicesData[serviceId]["users"].append(chatId)
        elif chatId in servicesData[serviceId]["users"]:
            raise Exception("Вы уже добавили эту услугу")
        else:
            chatsAr = servicesData[serviceId]["users"]
            chatsAr.append(chatId)
        with open("data.json", "w", encoding='utf8') as file:
            json.dump(servicesData, file, ensure_ascii=False, indent=4)