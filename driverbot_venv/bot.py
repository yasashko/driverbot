# импортируем необходимые компоненты
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from settings import TG_TOKEN, TG_API_URL
# создаем функцию main, которая соединяется с платформой Telegram
def sms(bot, update):
    print('Кто-то отправил команду /start. Что мне делать?') #вывод сообщения в консоль при отправке команды /start
    bot.message.reply_text('Здорово, {}! \nПоговорите со мной!' .format(bot.message.chat.first_name)) # отправим ответ
    print(bot.message)
def parrot(bot, update):
    print(bot.message.text) #печатаем на экран сообщение пользователя
    bot.message.reply_text(bot.message.text) # отправляем обратно текст, который послал пользователь

def main():
    #тело функции, описываем функцию (что она будет делать)
    # создадим переменную my_bot, с помощью которой будем взаимодействовать с нашим ботом
    my_bot = Updater (TG_TOKEN, TG_API_URL, use_context=True)

    my_bot.dispatcher.add_handler(CommandHandler('start', sms)) # обработчик команды start

    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot)) # обработчик текстового сообщения

    my_bot.start_polling() #проверяем о наличии сообщений с платформы Telegram
    my_bot.idle() #бот будет работать, пока его не остановят


# вызываем и запускаем функицю main
main()