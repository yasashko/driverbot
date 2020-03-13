from bs4 import BeautifulSoup
from glob import glob
from random import choice
import requests
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import ParseMode
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from utility import get_keyboard


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

def anketa_start(bot, update):
    bot.message.reply_text('Как вас зовут?', reply_markup=ReplyKeyboardRemove()) #вопрос и убираем основную клавиатуру
    return "user_name" # ключ для определения следующего шага

def anketa_get_name(bot, update):
    update.user_data['name'] = bot.message.text  # временно сохраняем ответ
    bot.message.reply_text("Сколько вам лет?")  # задаем вопрос
    return "user_age"  # ключ для определения следующего шага


def anketa_get_age(bot, update):
    update.user_data['age'] = bot.message.text  # временно сохраняем ответ
    reply_keyboard = [["1", "2", "3", "4", "5"]]  # создаем клавиатуру
    bot.message.reply_text(
        "Оцените статью от 1 до 5",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True, one_time_keyboard=True))  # при нажатии клавиатура исчезает
    return "evaluation"  # ключ для определения следующего шага


def anketa_get_evaluation(bot, update):
    update.user_data['evaluation'] = bot.message.text  # временно сохраняем ответ
    reply_keyboard = [["Пропустить"]]  # создаем клавиатуру
    bot.message.reply_text("Напишите отзыв или нажмите кнопку пропустить этот шаг.",
                           reply_markup=ReplyKeyboardMarkup(
                               reply_keyboard, resize_keyboard=True, one_time_keyboard=True))  # клава исчезает
    return "comment"  # ключ для определения следующего шага


def anketa_comment(bot, update):
    update.user_data['comment'] = bot.message.text  # временно сохраняем ответ
    text = """Результат опроса:
    <b>Имя:</b> {name}
    <b>Возраст:</b> {age}
    <b>Оценка:</b> {evaluation}
    <b>Комментарий:</b> {comment}
    """.format(**update.user_data)
    bot.message.reply_text(text, parse_mode=ParseMode.HTML)  # текстовое сообщение с форматированием HTML
    bot.message.reply_text("Спасибо вам за комментарий!", reply_markup=get_keyboard())  # сообщение и возвр. осн. клаву
    return ConversationHandler.END  # выходим из диалога


def anketa_exit_comment(bot, update):
    text = """Результат опроса:
    <b>Имя:</b> {name}
    <b>Возраст:</b> {age}
    <b>Оценка:</b> {evaluation}""".format(**update.user_data)
    bot.message.reply_text(text, parse_mode=ParseMode.HTML)  # текстовое сообщение с форматированием HTML
    bot.message.reply_text("Спасибо!", reply_markup=get_keyboard())  # отправляем сообщение и возвращаем осн. клаву
    return ConversationHandler.END  # выходим из диалога


def dontknow(bot, update):
    bot.message.reply_text("Я вас не понимаю, выберите оценку на клавиатуре!")