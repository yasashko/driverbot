from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_keyboard(): # объявляем новую функцию для клавиатуры
    contact_button = KeyboardButton('Отправить контакты', request_contact=True)
    location_button = KeyboardButton('Отправить геопозицию', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([['/start', 'Начать'], ['Анекдот'],
                                       [contact_button, location_button],
                                      ['Заполнить анкету']
                                       ], resize_keyboard=True)  # добавляем кнопку (сделал несколько для ознакомления с функционалом
    return my_keyboard
