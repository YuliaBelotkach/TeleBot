import telebot, time  # удалено просто import telebot
from telebot import apihelper, types
import random  # рандомные цитаты
import requests  # парсер
import config  # для файла конфиг, там лежит пока только токен
from bs4 import BeautifulSoup as b  # парсер
import logging  # для безостановочного бота
from telebot import types  # для клавиатуры
import sqlite3


bot = telebot.TeleBot(config.TOKEN)
print(bot.get_me())


# __________ПАРСИНГ ТУТ____________________________________________________
URL = 'https://www.inpearls.ru/%D1%81%D1%83%D0%BC%D0%BE%D1%87%D0%BA%D0%B0'

def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    citaty = soup.find_all('div', class_='text')
    return [c.text for c in citaty]
list_of_citaty = parser(URL)
random.shuffle(list_of_citaty)

# ______________ТЕЛО БОТА________________________________________________________
@bot.message_handler(commands=['start', 'restart'])
def start(message):
    photo = open('static/welcome.webp', 'rb')  # адрес где лежит картинка
    bot.send_sticker(message.chat.id, photo)  # отправляем одну и ту же картинку
    keyboard = telebot.types.ReplyKeyboardMarkup(True) #добавляем кнопки внизу
    keyboard.row('Каталог', 'Доставка', 'Оплата') #первая полоска
    keyboard.row('Ссылки') #вторая полоска
    bot.send_message(message.chat.id, 'Привет, {first}.\nЯ-бот, который:\n-поможет выбрать сумку\n-ответит на все твои вопросы\n-добавит тебе бонусы\n-покажет трек-номер посылки \n/restart'.format(first=message.from_user.first_name), parse_mode='html', reply_markup=keyboard)
    bot.send_message(message.chat.id, 'Сделай свой выбор, нажав на кнопку ниже.\nИли...может, почитаем цитаты про женскую сумочку? Отправь мне любую цифру')

@bot.message_handler(content_types=['text'])
def main(message):
    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, list_of_citaty[0]) #показываем первую цитату из списка и удаляем ее
        del list_of_citaty[0]
    elif message.text.lower() == 'каталог':
        markup1 = types.InlineKeyboardMarkup() #кнопки под сообщением
        item1 = types.InlineKeyboardButton("Сумки", url='https://fekla.by/product-category/sumki/')
        item2 = types.InlineKeyboardButton("Плечевые ремни", url='https://fekla.by/product-category/remni-dlja-sumok/')
        markup1.add(item1, item2)
        bot.send_message(message.chat.id, text='Выбери нужную категорию:', reply_markup=markup1)
    elif message.text.lower() == 'сумки':
        bot.send_message(message.chat.id, 'Нажмите на кнопку с названием Сумки в разделе Каталог!') #обрабатвае возможные ошибки
    elif message.text.lower() == 'плечевые ремни':
        bot.send_message(message.chat.id, 'Нажмите на кнопку с названием Плечевые ремни в разделе Каталог!')
    elif message.text.lower() == 'доставка':
        markup2 = types.InlineKeyboardMarkup()
        item3 = types.InlineKeyboardButton("В отделение почты", callback_data='сам')
        item4 = types.InlineKeyboardButton("Курьером до двери", callback_data='дверь')
        markup2.add(item3, item4)
        bot.send_message(message.chat.id, text='Выбери нужный вариант:', reply_markup=markup2)
    elif message.text.lower() == 'оплата':
        markup3 = types.InlineKeyboardMarkup()
        item5 = types.InlineKeyboardButton("Инстаграм", url='https://www.instagram.com/fekla.by/')
        item6 = types.InlineKeyboardButton("Сайт", url='https://fekla.by')
        markup3.add(item5, item6)
        # bot.send_message(message.chat.id, text='Оплатить можно при получении в почтовом отделении или заранее на нашем сайте.\nЗаказ можно оформить через корзину на сайте или в директе инстаграм.\nЖми кнопку ниже.')
        bot.send_message(message.chat.id, text='Оплатить можно:\n🔘при получении в почтовом отделении наличными или картой.\n🔘заранее на нашем сайте обычной картой, картой Покупок, картой Халва, через сервис ОПЛАТИ.\n\nЗаказ можно оформить через корзину на сайте или в директе инстаграм.\nВыбери нужный вариант👇', reply_markup=markup3)
        photo = open('static/payment.jpg', 'rb')  # адрес где лежит картинка
        bot.send_sticker(message.chat.id, photo)
    elif message.text.lower() == 'ссылки':
        markup4 = types.InlineKeyboardMarkup()
        item7 = types.InlineKeyboardButton("Instagram", url='https://www.instagram.com/fekla.by/')
        item8 = types.InlineKeyboardButton("Сайт", url='https://fekla.by')
        markup4.add(item7, item8)
        bot.send_message(message.chat.id, text='Выбери нужную категорию:', reply_markup=markup4)
    elif message.text.lower() == 'в отделение почты':
        markup5 = types.InlineKeyboardMarkup()
        item9 = types.InlineKeyboardButton("Белпочта", callback_data='евро')
        item10 = types.InlineKeyboardButton("Европочта", callback_data='бел')
        bot.send_message(message.chat.id, text='Выбери нужный вариант:', reply_markup=markup5)
    elif message.text.lower() == 'европочта':
        markup6 = types.InlineKeyboardMarkup()
        item11 = types.InlineKeyboardButton("Список отделений", url='https://www.instagram.com/fekla.by/')
        bot.send_message(message.chat.id, text='лишний текст', reply_markup=markup6)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'сам':
                markup5 = types.InlineKeyboardMarkup()
                item9 = types.InlineKeyboardButton("Европочтa", callback_data='евро')
                item10 = types.InlineKeyboardButton("Белпочта", callback_data='бел')
                markup5.add(item9, item10)
                bot.send_message(call.message.chat.id, 'Какой почтой удобнее?', reply_markup=markup5)
        if call.message:
            if call.data == 'дверь':
                bot.send_message(call.message.chat.id, 'Доставка курьером Европочты занимает 2-3 дня.\n1️⃣Мы отправляем посылку с доставкой курьером до двери.\n2️⃣Примерно через 1 день Вам на телефон придет смс от Европочты со ссылкой на выбор даты и времени доставки на их сайте.\n3️⃣Вы сами выберете удобный день и интервал времени доставки.\n4️⃣Почтовый курьер принесёт посылку.')
        if call.message:
            if call.data == 'евро':
                bot.send_message(call.message.chat.id, 'Высылаем в удобное для Вас отделение с наложенным платежом,\nпересылка за наш счет, бесплатная, комиссию почте за перевод денег платить не нужно.\nВсе расходы мы берём на себя.')
                markup6 = types.InlineKeyboardMarkup()
                item11 = types.InlineKeyboardButton("Нажми здесь", url='https://evropochta.by/about/offices/')
                markup6.add(item11)
                bot.send_message(call.message.chat.id, 'Посмотреть адреса отделений👇', reply_markup=markup6)
        if call.message:
            if call.data == 'бел':
                bot.send_message(call.message.chat.id, 'Высылаем в удобное для Вас отделение с наложенным платежом,\nпересылка за наш счет, бесплатная, комиссию почте за перевод денег платить не нужно.\nВсе расходы мы берём на себя.')


    except Exception as e:
        print(repr(e))


bot.polling()