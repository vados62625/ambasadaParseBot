from aiogram import types
import ambasadaParser
import model

async def start(message: types.Message):
    
    await message.answer("Привет!\nВыбери команду из списка")    


async def echo(message: types.Message):

    await message.answer('Выбери команду из списка')

    
async def selectServices(message: types.Message):
    
    inline_kb = types.InlineKeyboardMarkup()
    answer = 'Выберите услугу из списка:'
    data = ambasadaParser.showAvailibleServices()
    for row in data:
        serviceId = row
        serviceName = data[row]["name"]
        inline_btn_1 = types.InlineKeyboardButton(f'{serviceName}', callback_data=f'subscribeService={serviceId}')
        inline_kb.add(inline_btn_1)
    await message.answer(answer, reply_markup=inline_kb)


async def showSelectedServices(message: types.Message):
    serviceAr = model.getSelectedServicesAr(message.from_user.id)
    answer = "Вы не подписаны на услуги"
    if len(serviceAr) > 0:
        answer = 'Ваши подписки:\n\n'
        for service in serviceAr:
            answer += f'{serviceAr[service]["name"]}\n\n'
    await message.answer(answer)

async def selectServiceToUnsubscribe(message: types.Message):
    serviceAr = model.getSelectedServicesAr(message.from_user.id)
    answer = "Вы не подписаны на услуги"
    if len(serviceAr) > 0:
        inline_kb = types.InlineKeyboardMarkup()
        answer = 'Выберите услугу от которой хотите отписаться:\n\n'
        for service in serviceAr:
            inline_btn_1 = types.InlineKeyboardButton(f'{serviceAr[service]["name"]}', callback_data=f'unsubscribeService={service}')
            inline_kb.add(inline_btn_1)
    await message.answer(answer, reply_markup=inline_kb)


async def subscribeService(callback_query: types.CallbackQuery):
    
    serviceId = callback_query.data.partition('=')[2]
    try:
        ambasadaParser.subscribeService(serviceId, callback_query)
        answer = 'Успешно!'
    except Exception as e:
        answer = f'Ошибка\n{e}'
    await callback_query.message.answer(answer)     
    await callback_query.answer()
    await callback_query.message.delete()

async def unsubscribeService(callback_query: types.CallbackQuery):
    
    serviceId = callback_query.data.partition('=')[2]
    try:
        ambasadaParser.unsubscribeService(serviceId, callback_query)
        answer = 'Успешно!'
    except Exception as e:
        answer = f'Ошибка\n{e}'
    await callback_query.message.answer(answer)     
    await callback_query.answer()
    await callback_query.message.delete()