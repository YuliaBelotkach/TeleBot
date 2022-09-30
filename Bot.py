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
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Каталог', 'Доставка', 'Оплата')
    keyboard.row('Ссылки', 'Запишите меня', 'Штрихкод')
    bot.send_message(message.chat.id, 'Привет, {first}.\nЯ-бот, который:\n-поможет выбрать сумку\n-ответит на все твои вопросы\n-добавит тебе бонусы\n-покажет трек-номер посылки \n/restart'.format(first=message.from_user.first_name), parse_mode='html', reply_markup=keyboard)
    bot.send_message(message.chat.id, 'Сделай свой выбор, нажав на кнопку ниже.\nИли...может, почитаем цитаты про женскую сумочку? Отправь мне любую цифру')




@bot.message_handler(content_types=['text'])
def main(message):
    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, list_of_citaty[0])
        del list_of_citaty[0]
    elif message.text.lower() == 'каталог':
        markup1 = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Сумки", callback_data='сумки')
        item2 = types.InlineKeyboardButton("Плечевые ремни", url='https://fekla.by/product-category/remni-dlja-sumok/')
        markup1.add(item1, item2)
        bot.send_message(message.chat.id, text='Выбери нужную категорию:', reply_markup=markup1)
    elif message.text.lower() == 'сумки':
        bot.send_message(message.chat.id, 'Нажмите на кнопку с названием Сумки в разделе Каталог!')
    elif message.text.lower() == 'плечевые ремни':
        bot.send_message(message.chat.id, 'Нажмите на кнопку с названием Плечевые ремни в разделе Каталог!')
    elif message.text.lower() == 'доставка':
        markup2 = types.InlineKeyboardMarkup()
        item3 = types.InlineKeyboardButton("В отделение почты", callback_data='сам')
        item4 = types.InlineKeyboardButton("Курьером до двери", callback_data='дверь')
        markup2.add(item3, item4)
        bot.send_message(message.chat.id, text='Выбери нужный вариант:', reply_markup=markup2)
    elif message.text.lower() == 'оплата':
        bot.send_message(message.chat.id, text='какая-то инфа по оплате')
    elif message.text.lower() == 'ссылки':
        markup3 = types.InlineKeyboardMarkup()
        item5 = types.InlineKeyboardButton("Instagram", url='https://www.instagram.com/fekla.by/')
        item6 = types.InlineKeyboardButton("Сайт", url='https://fekla.by')
        markup3.add(item5, item6)
        bot.send_message(message.chat.id, text='Выбери нужную категорию:', reply_markup=markup3)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'сумки':
                bot.send_message(call.message.chat.id, 'тут покажем сумки')
        if call.message:
            if call.data == 'сам':
                bot.send_message(call.message.chat.id, 'тут покажем евро и белпочта')
        if call.message:
            if call.data == 'дверь':
                bot.send_message(call.message.chat.id, 'тут покажем тоже евро и белпочта')



    except Exception as e:
        print(repr(e))


bot.polling()
