from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)

folder_path = 'assets'
orderActive = False
packetName = ""

priceList = []
templateForm = ('Заполнение формы (Пример):\n'
                'Введите: \n'
                '\t\t\t- Дата,\n'
                '\t\t\t- Время (В какое время?),\n'
                '\t\t\t- Адрес\n' 
                '\t\t\t- Номер телефона\n\n'
           
                'Образец: 10.07.23, 17:45, Мамыр-4, дом 302, кв 41, 8(707)233-23-23)')


desclist = ["Набор ‘Базовый’ за 6 000₸\n"
             "⚡️HDMI кабель\n"
             "⚡️Штатив (1, 8 метр)\n"
             "⚡️Удлинитель (4 метр)\n",


            "Набор ‘Базовый + Экран ’ за 9 000₸\n"
            "⚡️HDMI кабель\n"
            "⚡️Штатив (1, 8 метр)\n"
            "⚡️Указка (переключатель)\n"
            "⚡️Удлинитель (4 метр)\n"
            "➕Проекционный экран (2 х 1,5 метр)\n",

            "Набор ‘Полный ’ за 12 000₸\n"
            "⚡️HDMI кабель\n"
            "⚡️Штатив (1, 8 метр)\n"
            "⚡️Указка (переключатель)\n"
            "⚡️Удлинитель (4 метр)\n"
            "➕Проекционный экран (2 х 1,5 метр)\n"
            "🎶 Колонка LG xBoom (600Вт)\n"
            "🎤 Беспроводной Микрофон\n"]

# First level elements (MENU)
firstLevel = types.ReplyKeyboardMarkup(resize_keyboard=True)
firstLevel.add('🍿Арендовать проектор!').add('☎️ Заказать звонок').add('🪩Мы в Instagram')

# Second level [🍿Арендовать проектор!]
secondLevelOne = types.InlineKeyboardMarkup(row_width=1)
secondLevelOne.add(InlineKeyboardButton(text='Базовый набор за (6 000₸)', callback_data='basic'),
                  InlineKeyboardButton(text='Базовый + Экран за (9 000₸)', callback_data='prestige'),
                  InlineKeyboardButton(text='Полный набор за (12 000₸)', callback_data='full'),
                  InlineKeyboardButton(text='Назад', callback_data='backmenu'))

# Fourth level [Каждый Пакет]
fourthLevelOne = types.InlineKeyboardMarkup(row_width=1)
fourthLevelOne.add(InlineKeyboardButton(text='Заказать', callback_data='order'),
                  InlineKeyboardButton(text='Назад', callback_data='back'))

# Second level ['☎️ Заказать звонок']
secondLevelTwo = types.ReplyKeyboardMarkup(resize_keyboard=True)
secondLevelTwo.add(types.KeyboardButton('📞 Отправить мой номер', request_contact=True),
                   types.KeyboardButton('🔙Назад'))

# Second level [Button 'Назад']
secondLevelTwoInline = types.InlineKeyboardMarkup()
secondLevelTwoInline.add(types.InlineKeyboardButton(text='Назад', callback_data='outremoveback'))

# Second level [🪩Мы в Instagram]
secondLevelThree = types.InlineKeyboardMarkup(row_width=1)
secondLevelThree.add(InlineKeyboardButton(text='Перейти в Instagram', url='https://www.instagram.com/kinorent.kz/'))

# Deleting last
additionalBack = InlineKeyboardMarkup(row_width=1)
additionalBack.add(InlineKeyboardButton(text="Назад", callback_data='additionalBack'))

# Show map
mapDetails = InlineKeyboardMarkup(row_width=1)
mapDetails.add(InlineKeyboardButton(text="Показать карту", callback_data='shmap'))

# Menu [/start]
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Главный меню", reply_markup=firstLevel)

# Menu [/rent]
@dp.message_handler(text='🍿Арендовать проектор!')
async def rent(message: types.Message):
    await message.answer("Выберите один из них ", reply_markup=secondLevelOne)

@dp.message_handler(text='🔙Назад')
async def goBack(message: types.Message):
    await message.answer("Главный меню", reply_markup=firstLevel)


@dp.message_handler(text='☎️ Заказать звонок')
async def order(message: types.Message):
    await message.answer("Нажмите на кнопку ниже", reply_markup=secondLevelTwo)


@dp.message_handler(text='🪩Мы в Instagram')
async def rent(message: types.Message):
    await message.answer('Ссылка на Instagram', reply_markup=secondLevelThree)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def process_contact(message: types.Message):
    phone_number = message.contact.phone_number
    await message.answer(
        f"Спасибо {message.from_user.first_name}! \n"
        f"В ближайшее время на указанный вами номер будет совершен звонок. \n"
        f"Номер: {phone_number}", reply_markup=secondLevelTwoInline)

    await bot.forward_message(os.getenv('GROUP_ID'), message.from_user.id, message.message_id)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def text_handler(message: types.Message):
    global orderActive


    await bot.forward_message(os.getenv('GROUP_ID'), message.from_user.id, message.message_id)


    if orderActive:
        fname = message.from_user.first_name
        await message.answer(
            f"\t{fname}, убедитесь в правильности введенных вами данных.\n\n"
            "\tДля уточнения деталей с вами свяжутся операторы\n"
            "в течение одной минуты.\n\n"
            "\tНажмите кнопку «Показать карту», чтобы увидеть зону бесплатной доставки \n",
            reply_markup=mapDetails)

        orderActive = False
    else:
        await message.answer("Я вас не понимаю")

    await bot.send_message(os.getenv('GROUP_ID'), text=packetName)





@dp.callback_query_handler()
async def callbackFunctions(call: types.CallbackQuery):
    global priceList
    global desclist
    global templateForm
    global orderActive
    global packetName

    if call.data == 'basic':
        with open(f'./{folder_path}/classic.jpg', 'rb') as basicPrice:
            await bot.send_photo(chat_id=call.from_user.id, photo=basicPrice, caption=desclist[0], reply_markup=fourthLevelOne)
            packetName = "🟢 Заказ на набор 'Basic' - проектор со штативом"
    elif call.data == 'prestige':
        with open(f'./{folder_path}/prestige.jpg', 'rb') as prestigePrice:
            await bot.send_photo(chat_id=call.from_user.id, photo=prestigePrice, caption=desclist[1], reply_markup=fourthLevelOne)
            packetName = "🟡 Заказ на набор 'Prestige' - проектор c экраном"
    elif call.data == 'full':
        with open(f'./{folder_path}/full.jpg', 'rb') as fullPrice:
            await bot.send_photo(chat_id=call.from_user.id, photo=fullPrice, caption=desclist[2],
                                 reply_markup=fourthLevelOne)
            packetName = "🔴 Заказ на набор 'Full' - Полный набор"
    elif call.data == 'shmap':
        with open(f'./{folder_path}/map.jpg', 'rb') as mapScreen:
            await bot.send_photo(chat_id=call.from_user.id, photo=mapScreen, caption="Зона бесплатной доставки")
    elif call.data == 'backmenu':
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text="Главный меню")
        await bot.delete_message(chat_id=call.from_user.id, message_id=(call.message.message_id))
    elif call.data == 'order':
        await bot.send_message(chat_id=call.from_user.id, text=templateForm, reply_markup=additionalBack)
        orderActive = True
    elif call.data == 'back' or 'additionalBack':
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        orderActive = False
    elif call.data == 'outremoveback':
        await bot.send_message(chat_id=call.from_user.id, text="Главный меню", reply_markup=firstLevel)

@dp.message_handler()
async def noidea(message: types.Message):
    await message.answer('Я вас не понимаю!')


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
