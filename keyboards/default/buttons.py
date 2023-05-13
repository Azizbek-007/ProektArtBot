from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.db_api import menu, menu_in_menu

phone_number = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Телефон номерди жибериў", request_contact=True)
)

def menu_btn():
    a = []
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for x in menu():
        a.append(KeyboardButton(x[1]))
    a.append(KeyboardButton("Биз қандай ислеймиз"))
    a.append(KeyboardButton("Бийпул маглыумат"))
    return markup.add(*a)

def category_btn(menu_id):
    a = []
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for x in menu_in_menu(menu_id):
        a.append(KeyboardButton(x[2]))
    return markup.add(*a).add(KeyboardButton("➡️ Бас бөлимге қайтыў"))
