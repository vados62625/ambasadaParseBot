import json

def getServicesAr():
    try:
        with open("data.json", "r", encoding='utf8') as file:
            servicesData = json.load(file)
            servicesAr = []
            if len(servicesData) > 0:
                for service in servicesData:
                    servicesAr.append(service)
                return servicesAr
            else:
                return []
    except:
        return []

def cancelSubscribe(serviceId, chatId):
    try:
        with open("data.json", "r", encoding='utf8') as file:
            servicesData = json.load(file)
            if serviceId in servicesData:
                servicesData[serviceId]["users"].remove(chatId)
                with open("data.json", "w", encoding='utf8') as file:
                    json.dump(servicesData, file, ensure_ascii=False, indent=4)
                return True
    except:
        return False

def getSelectedServicesAr(chatId: int):
    try:
        with open("data.json", "r", encoding='utf8') as file:
            servicesData = json.load(file)
            servicesAr = {}
            if len(servicesData) > 0:
                for service in servicesData:
                    if chatId in servicesData[service]["users"]:
                        servicesAr[service] = servicesData[service]
                return servicesAr
            else:
                return {}
    except:
        return {}
        # raise Exception("Вы уже добавили эту услугу")