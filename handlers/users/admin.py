from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from states import MessageForm, CategoryForm, SendAll
from keyboards.inline import category_btn, cencel_btn, menuIN_btn, order_delete_btn
from utils.db_api import create_message, create_category, get_message, delete_message, delete_category, get_users, get_xls,\
users_count
from loader import dp
import re
import asyncio
from data.config import ADMINS

@dp.message_handler(commands=['admin'], user_id=ADMINS)
async def hello_admin(msg: types.Message):
    await msg.answer("Hello admin", reply_markup=category_btn())

@dp.callback_query_handler(lambda call: call.data == 'download')
async def xsl_down_send(call: types.CallbackQuery):
    user_count = users_count()[0][0]
    get_xls()
    await call.message.answer_document(open('./users.xlsx', 'rb'), caption=f"Users: {user_count}")

@dp.callback_query_handler(lambda call: call.data == 'send_message')
async def send_message(call: types.CallbackQuery):
    await call.message.answer("Send me message:", reply_markup=cencel_btn)
    await SendAll.msg.set()

@dp.callback_query_handler(lambda call: call.data == 'send_forward')
async def send_message_frwd(call: types.CallbackQuery):
    await call.message.answer("Send me message:", reply_markup=cencel_btn)
    await SendAll.forward.set()

@dp.callback_query_handler(lambda call: call.data == 'cencel', state='*')
async def cencel(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    await call.message.answer("Бийкар етилди")

@dp.callback_query_handler(lambda call: 'menu_id=' in call.data)
async def add_category_for_msg(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    menu_id = call.data.split('=')[1]
    await state.update_data(menu_id=menu_id)
    await CategoryForm.name.set()
    await call.message.answer("Меню атын киритиң:", reply_markup=cencel_btn)

@dp.message_handler(state=CategoryForm.name, content_types=['text'])
async def set_text_category(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    create_category(data['menu_id'], msg.text)
    await msg.answer("Қосылды ✅")
    await state.finish()
    await msg.answer("Hello admin", reply_markup=category_btn())   

@dp.callback_query_handler(lambda call: 'menu_IN=' in call.data)
async def add_category_for_msg(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    menu_id = call.data.split('=')[1]
    await call.message.answer("Менюдиң ишки бөлими!", reply_markup=menuIN_btn(menu_id))

@dp.callback_query_handler(lambda call: 'menuIN_id=' in call.data)
async def add_category_for_msg(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    category_id = call.data.split('=')[1]
    await state.update_data(cat_id=category_id)
    await MessageForm.photo.set()
    await call.message.answer("Сүўрет жибериң:", reply_markup=cencel_btn)

@dp.message_handler(state=MessageForm.photo, content_types=['photo'])
async def set_photo(msg: types.Message, state: FSMContext):
    await msg.answer("Пост ушын текст киритиң:", reply_markup=cencel_btn)
    photo_id = msg.photo[0].file_id
    await state.update_data(photo=photo_id)
    await MessageForm.next()

@dp.message_handler(state=MessageForm.text, content_types=['text'])
async def set_photo(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    create_message(data['cat_id'], msg.text, data['photo'])
    await msg.answer("Қосылды ✅")
    await state.finish()
    await msg.answer("Hello admin", reply_markup=category_btn())

@dp.message_handler(state=SendAll.msg)
async def send_messge_users(msg: types.Message, state: FSMContext):
    s, n = 0, 0
    await msg.answer("seding...")
    await state.finish()
  
    for x in get_users():    
        try:
            await msg.copy_to(x[0], reply_markup=msg.reply_markup)
            await asyncio.sleep(.07)
            s +=1
        except: n +=1
    await msg.reply(f"Жиберилди: {s}\nЖиберилмеди: {n}")

@dp.message_handler(state=SendAll.forward)
async def send_messge_forward(msg: types.Message, state: FSMContext):
    s, n = 0, 0
    await msg.answer("seding...")
    await state.finish()
  
    for x in get_users():    
        try:
            await msg.forward(x[0])
            await asyncio.sleep(.07)
            s +=1
        except: n +=1
    await msg.reply(f"Жиберилди: {s}\nЖиберилмеди: {n}")


@dp.callback_query_handler(lambda call: 'CategoryOpen=' in call.data)
async def set_cat_open(call: types.CallbackQuery):
    category_id = call.data.split('=')[1]
    data = get_message(cate_id=category_id)
    if len(data) > 0:
        for x in data:
            await call.message.answer_photo(x[3], x[2], reply_markup=order_delete_btn(x[0]))
    else: await call.answer("Мағлыўмат жоқ", True)

@dp.callback_query_handler(lambda call: 'msg_del' in call.data)
async def delete_product(call: types.CallbackQuery):
    await call.answer("deleted")
    msg_id = call.data.split('=')[1]
    delete_message(msg_id)
    await call.message.delete()


@dp.callback_query_handler(lambda call: 'deleteCategory=' in call.data)
async def delete_category_func(call: types.CallbackQuery):
    cat_id = call.data.split('=')[1]
    delete_category(cat_id)
    await call.answer("deleted")
    await call.message.delete()
