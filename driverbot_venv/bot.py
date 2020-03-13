# импортируем необходимые компоненты

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TG_TOKEN, TG_API_URL
from handlers import *

import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')




# создаем функцию main, которая соединяется с платформой Telegram
def main():
    #тело функции, описываем функцию (что она будет делать)
    # создадим переменную my_bot, с помощью которой будем взаимодействовать с нашим ботом
    my_bot = Updater (TG_TOKEN, TG_API_URL, use_context=True)
    logging.info('Start bot')
    my_bot.dispatcher.add_handler(CommandHandler('start', sms)) # обработчик команды start

    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Начать'), sms)) # назначаю команду для кнопки "Начать"

    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex("Анекдот"), get_anekdote)) # обрабатываем текст кнопки

    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, get_contact))  # обрабатчик контактов

    my_bot.dispatcher.add_handler(MessageHandler(Filters.location, get_location))  # обрабатчик локации

    my_bot.dispatcher.add_handler(
        ConversationHandler(entry_points=[MessageHandler(Filters.regex('Заполнить анкету'), anketa_start)],
                            states={
                                "user_name": [MessageHandler(Filters.text, anketa_get_name)],
                                "user_age": [MessageHandler(Filters.text, anketa_get_age)],
                                "evaluation": [MessageHandler(Filters.regex('1|2|3|4|5'), anketa_get_evaluation)],
                                "comment": [MessageHandler(Filters.regex('Пропустить'), anketa_exit_comment),
                                            MessageHandler(Filters.text, anketa_comment)],
                            },
                            fallbacks=[MessageHandler(
                                Filters.text | Filters.video | Filters.photo | Filters.document, dontknow)]
                            )
    )

    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot)) # обработчик текстового сообщения



    my_bot.start_polling() #проверяем о наличии сообщений с платформы Telegram
    my_bot.idle() #бот будет работать, пока его не остановят


# вызываем и запускаем функицю main
if __name__ == "__main__":
    main()