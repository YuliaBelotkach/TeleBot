import random  # рандомные анекдоты
import requests
import telebot
import telebot, time
import config
from bs4 import BeautifulSoup as b
import logging

URL = 'https://www.anekdot.ru/last/good'

def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    anekdots = soup.find_all('div', class_='text')
    return [c.text for c in anekdots]

list_of_jokes = parser(URL)
random.shuffle(list_of_jokes)
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    photo = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, photo)
    # bot.send_message(message.chat.id, "Привет!") #сюда надо дабавить обращение по имени
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Привет', 'Пока', 'Информация')
    bot.send_message(message.chat.id, 'Привет, человек!', reply_markup=keyboard)

# @bot.message_handler(commands=['юля'])   #НЕ РАБОТАЕТ?
# def hello(message):
#     bot.send_message(message.chat.id, 'Цифру')

@bot.message_handler(content_types=['text'])
def jokes(message):
    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, list_of_jokes[0])
        del list_of_jokes[0]
    else:
        bot.send_message(message.chat.id, 'Введите любую цифру')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Ещё раз привет!')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока!')

while True:
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
