from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db_api import menu, menu_in_menu

def category_btn():
    markup = InlineKeyboardMarkup()
    for x in menu():
        markup.add(InlineKeyboardButton(f'➕{x[1]}', callback_data=f'menu_id={x[0]}'),
            InlineKeyboardButton('📂', callback_data=f'menu_IN={x[0]}'))
    markup.add(InlineKeyboardButton("Хабар тарқатыў", callback_data="send_message"))
    markup.add(InlineKeyboardButton("Узатпа хабар тарқатыў", callback_data="send_forward"))
    markup.add(InlineKeyboardButton('📥 Базаны жүклеп алыў', callback_data='download'))
    return markup

def menuIN_btn(menu_id):
    markup = InlineKeyboardMarkup()
    for x in menu_in_menu(menu_id):
        markup.add(InlineKeyboardButton(f'➕{x[2]}', callback_data=f'menuIN_id={x[0]}'), 
            InlineKeyboardButton('🗑', callback_data=f'deleteCategory={x[0]}'), 
            InlineKeyboardButton('📂', callback_data=f'CategoryOpen={x[0]}'))
    return markup

def order_btn(msg_id):
    return InlineKeyboardMarkup().add( InlineKeyboardButton("Буйыртпа бериў", callback_data=f'order_id={msg_id}'))

def order_delete_btn(msg_id):
    return InlineKeyboardMarkup().add( InlineKeyboardButton("🗑", callback_data=f'msg_del={msg_id}'))

cencel_btn = InlineKeyboardMarkup().add( InlineKeyboardButton("Бийкар етиў", callback_data='cencel') )