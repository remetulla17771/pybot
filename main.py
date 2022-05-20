from distutils.util import execute
import imp
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import aiohttp
import json
from db import Database
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
# tokenOld='5315163231:AAHgp23m6BxpWDJbmL1RYUnu3bIW_4gW5Zg' 
token='5210982324:AAGe7wFIAa-N2JmuY6fvxmEQMREY7krhCYM'


bot = Bot(token=token)
dp = Dispatcher(bot)

db = Database('database.db')

@dp.message_handler(content_types=["new_chat_members"])
async def handler_new_member(message):
    user_name = message.new_chat_member.first_name
    await bot.send_message(message.chat.id, "Добро пожаловать, {0}!".format(user_name))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # "💁🏻‍♀️📝"
    tt = "Құрметті, Қызылорда облысының тұрғындары! Егер Сіз 18 жасқа толған Қазақстан Республикасының азаматы болсаңыз, ҚР Конституциясына түзетулер енгізу бойынша 2022 жылдың 5 маусымында өтетін республикалық референдумға қатыса аласыз. Өз дауыс беру учаскеңіз жайлы ақпарат алу үшін ЖСН енгізіңіз.\n\nУважаемые жители Кызылординской области!Если Вы гражданин Республики Казахстан, достигший 18-летнего возраста, Вы можете участвовать в республиканском референдуме по поправкам в Конституцию РК, назначенном на 5 июня 2022 года. Для получения сведения о своем участке голосования напишите свой ИИН."
    await bot.send_message(message.from_user.id, tt)

@dp.message_handler()
async def response_message(msg: types.Message):
    if db.user_exists(msg.text):
        user = db.get_user(msg.text)
        uchastok = user[1]
        surname = user[2]
        name = user[3]
        fam = user[4]
        region = db.get_region(uchastok)
        nomer = region[2]
        uchNameRu = region[6]
        uchNameKk = region[8]

        streetRu = region[7]
        streetKk = region[9]

        house = region[10]
        prefix = region[11]
        uchCity = region[1]
        city = db.get_city(uchCity)
        cityName = city[4]
        cityNameKK = city[5]
        contactPhone = region[12]
        comission = region[15]
        fullName = surname + " " + name + " " + fam

        fullText = fullName + " \n\n#⃣ Сіздің дауыс беретін учаскеңіз / Ваш участок для голосования: №" + str(uchastok) + "\n\n📍 Мекенжайы / Адрес: \n"+cityNameKK + ", "+streetKk + " " + str(house) + prefix + "\n\n🏢 Ғимарат / Здание: \n" + uchNameRu + "\n\n☎ Байланыс нөмірі / Контактный номер: \n" + contactPhone

        # fullText = surname + " " + name + " " + fam + ", Сіз мына мекен-жайда " + cityNameKK + ", "+streetKk + " " + str(house) + prefix +  " ("+uchNameKk+") орналасқан №"+str(uchastok) + " сайлау учаскесінде тіркелгенсіз. Сайлау учаскесінің байланыс телефоны: " + contactPhone
        # fullText += "\n\n"+surname + " " + name + " " + fam + ", Вы зарегистрированы на № " + str(uchastok) + " избирательном участке (" + uchNameRu+"), расположенном по адресу: " + cityName + ", "+streetRu + " " + str(house) + " " + prefix + ". Контактный телефон избирательного участка: "+contactPhone
        await bot.send_message(msg.from_user.id, fullText)
    else:
        text = "🚫 <b>Енгізілген ЖСН табылмады. Тексеріп қайта енгізіңіз.</b>\n\nӨзіңізді сайлаушылардың тізімінен таппадыңыз ба?\nМекен-жайыңыз бойынша хабарласыңыз. \n\n🚫 <b>Введенный ИИН не найден. Проверьте и введите заново</b>\n\nНе нашли себя в списке избирателей? \nВыберите регион для самостоятельного обращения по месту жительства"
        text += "\n\n<b>Арал ауданы/Аральский район</b>\n☎ 8 (777) 503-85-85 (whatsapp)\n\n<b>Қазалы ауданы/Казалинский район</b>\n☎ 8 (775) 688-63-89 (whatsapp)\n\n<b>Қармақшы ауданы/Кармакшинский район</b>\n☎ 8 (775) 752-14-18 (whatsapp)\n\n<b>Жалағаш ауданы/Жалагашский район</b> \n☎ 8 (705) 270-00-28 (whatsapp)\n\n<b>Сырдария ауданы/Сырдарьинский район</b>\n☎ 8 (776) 501-19-85 (whatsapp)\n\n <b>Шиелі аудан/ Шиелииский район</b>\n☎ 8 (702) 557-79-25 (whatsapp)\n\n <b>Жанакорған ауданы/Жанакорганский район</b>\n☎ 8 (702) 191-35-98 (whatsapp)\n\n<b>Қызылорда қаласы/Город Кызылорда</b>\n☎ 8 (707) 222-34-56 (whatsapp)"
        await bot.send_message(msg.from_user.id, text, parse_mode=types.ParseMode.HTML)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)