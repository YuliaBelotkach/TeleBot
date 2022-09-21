import telebot

bot = telebot.Telebot('5425907209:AAF23LpU_XyNgzY7GbTIlICeS2RsLOt6bdo')

@bot.message_handler(command=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет', parse_mod='html')


bot.polling(none_stop=True)
