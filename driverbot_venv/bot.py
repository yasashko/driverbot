# импортируем необходимые компоненты
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TG_TOKEN, TG_API_URL
from bs4 import BeautifulSoup
import requests




def sms(bot, update):
    print('Кто-то отправил команду /start. Что мне делать?') #вывод сообщения в консоль при отправке команды /start
    bot.message.reply_text('Здорово, {}! \nПоболтаем?'
                           .format(bot.message.chat.first_name), reply_markup=get_keyboard()) # отправим ответ
    print(bot.message)

def get_anekdote(bot, update):
    receive = requests.get('http://anekdotme.ru/random') #отправляем запрос к странице
    page = BeautifulSoup(receive.text, "html.parser") #подключаем html парсер, получаем текст страницы
    find = page.select('.anekdot_text') #из страницы html получаем class= "anekdot_text"
    for text in find:
        page = (text.getText().strip())  # из class= "anekdot_text" получаем текст и убираем пробелы по сторонам
    bot.message.reply_text(page) # отправляем один анекдот, последний
    print(bot.message)

# функция parrot, которая повторяет все, что пишет пользователь
def parrot(bot, update):
    print(bot.message.text) #печатаем на экран сообщение пользователя
    bot.message.reply_text(bot.message.text) # отправляем обратно текст, который послал пользователь

def get_contact(bot, update):
    print(bot.message.contact)
    bot.message.reply_text('{}, мы получили ваш номер телефона!'.format(bot.message.chat.first_name))
    print(bot.mesage)

def get_location(bot, update):
    print(bot.message.location)
    bot.message.reply_text('{}, мы получили ваше местоположение!'.format(bot.message.chat.first_name))
    print(bot.mesage)

def get_keyboard(): # объявляем новую функцию для клавиатуры
    contact_button = KeyboardButton('Отправить контакты', request_contact=True)
    location_button = KeyboardButton('Отправить геопозицию', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([['/start', 'Начать'], ['Анекдот'],
                                       [contact_button, location_button]], resize_keyboard=True)  # добавляем кнопку (сделал несколько для ознакомления с функционалом
    return my_keyboard

# создаем функцию main, которая соединяется с платформой Telegram
def main():
    #тело функции, описываем функцию (что она будет делать)
    # создадим переменную my_bot, с помощью которой будем взаимодействовать с нашим ботом
    my_bot = Updater (TG_TOKEN, TG_API_URL, use_context=True)

    my_bot.dispatcher.add_handler(CommandHandler('start', sms)) # обработчик команды start

    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Начать'), sms)) # назначаю команду для кнопки "Начать"

    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex("Анекдот"), get_anekdote)) # обрабатываем текст кнопки

    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, get_contact))  # обрабатчик контактов

    my_bot.dispatcher.add_handler(MessageHandler(Filters.location, get_location))  # обрабатчик локации

    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot)) # обработчик текстового сообщения



    my_bot.start_polling() #проверяем о наличии сообщений с платформы Telegram
    my_bot.idle() #бот будет работать, пока его не остановят


# вызываем и запускаем функицю main
main()