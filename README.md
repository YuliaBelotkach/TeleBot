# Feklabybot by pyTelegramBotAPI for Python
![python](https://img.shields.io/pypi/pyversions/py?color=orange)
![size](https://img.shields.io/bundlephobia/min/bot?color=red)
![files](https://img.shields.io/github/directory-file-count/YuliaBelotkach/TeleBot)
![lastcommit](https://img.shields.io/github/last-commit/YuliaBelotkach/TeleBot?color=blue)
## e-commerce *for the site fekla.by*
_____
# Photo presentation
![image_bot](https://github.com/YuliaBelotkach/TeleBot/blob/master/static/044d9715-abce-4f6e-accf-6248199cfc00.jpg)
_____
😄 This telegram bot is able to answer questions and helps you choose a bag or a belt for a bag.
_____
# Getting Started and modules
Assuming that you have a supported version of Python installed, you can first set up your environment with:
```python
import telebot, time  
from telebot import apihelper, types
import random  
import requests  
import config  
from bs4 import BeautifulSoup as b  
import logging  
from telebot import types  
import sqlite3
```
# Components of the code

This bot contains message templates (a regular keyboard) and an inline keyboard.

```
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
```
Also, as entertainment, we added a parser of quotes about bags from the site to the bot. The user enters any number from the keyboard and randomly shows him a quote.
```
URL = 'https://www.inpearls.ru/%D1%81%D1%83%D0%BC%D0%BE%D1%87%D0%BA%D0%B0'
def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    citaty = soup.find_all('div', class_='text')
    return [c.text for c in citaty]
list_of_citaty = parser(URL)
random.shuffle(list_of_citaty)
```
We finish our code with the standard command ```bot.polling()``` for continuous operation.

