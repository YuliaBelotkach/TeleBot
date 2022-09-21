import random  # рандомные анекдоты
import requests  # парсер

import telebot, time  # удалено просто import telebot
import config  # для файла конфиг, там лежит пока только токен
from bs4 import BeautifulSoup as b  # парсер
import logging  # для безостановочного бота
from telebot import types

# ________________________ПАРСИНГ ТУТ____________________________________________________
URL = 'https://www.anekdot.ru/last/good'
def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    anekdots = soup.find_all('div', class_='text')
    return [c.text for c in anekdots]
list_of_jokes = parser(URL)
random.shuffle(list_of_jokes)
bot = telebot.TeleBot(config.TOKEN)

# ________________________ТЕЛО БОТА________________________________________________________
@bot.message_handler(commands=['start'])
def welcome(message):
    photo = open('static/welcome.webp', 'rb') # адрес где лежит картинка
    bot.send_sticker(message.chat.id, photo) # отправляем одну и ту же картинку
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('💞Каталог💞', 'Инфо', 'Твоя скидка')
    bot.send_message(message.chat.id, 'Привет, {first}. Введи цифру или напиши привет или пока'.format(first=message.from_user.first_name), reply_markup=keyboard)

     # тут наши кнопочки на клавиатуре, можно добавить что угодно
    # bot.send_message(message.chat.id, 'Привет, человек! Введи цифру или напиши привет или пока', reply_markup=keyboard)



@bot.message_handler(content_types=['text'])
def jokes(message):
    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, list_of_jokes[0])
        del list_of_jokes[0]
    elif message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Ещё раз привет!')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока!')
    elif message.text.lower() == '💞каталог💞':

        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardMarkup("Сумка формата А4", callback_data='Сумка формата А4')
        item2 = types.InlineKeyboardMarkup("Сумка формата книги", callback_data='Сумка формата книги')

        markup.add(item1, item2)

        bot.send_message(message.chat.id, 'Смотрите', reply_markup=markup)
    elif message.text.lower() == 'инфо':
        bot.send_message(message.chat.id, 'типа информация!')
    elif message.text.lower() == 'твоя скидка':
        bot.send_message(message.chat.id, 'типа твоя скидка!')
    else:
        bot.send_message(message.chat.id, 'Введи цифру или напиши Привет или Пока')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'Сумка формата А4':
                bot.send_message(call.message.chat.id, 'https://fekla.by/product-category/sumki/')
            elif call.data == 'Сумка формата книги':
                bot.send_message(call.message.chat.id, 'https://fekla.by/product-category/remni-dlja-sumok/')


while True:   # для безостановочной отработки
    try:
        logging.info("Bot running..")
        bot.polling(none_stop=True, interval=2)

        # Предполагаю, что бот может мирно завершить работу, поэтому
        # даем выйти из цикла
        break
    except telebot.apihelper.ApiException as e:
        logging.error(e)
        bot.stop_polling()

        time.sleep(15)

        logging.info("Running again!")