from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from states import PhoneForm
from keyboards.default import phone_number, menu_btn, category_btn
from keyboards.inline import order_btn
from utils.db_api import register_user, get_phone_number, update_phone_number, menu, by_menu,\
get_category, get_message, get_user, by_message
from loader import dp
import re
import asyncio

@dp.message_handler(CommandStart())
async def bot_start(msg: types.Message):
    register_user(msg.from_id, msg.from_user.username, msg.from_user.first_name, msg.from_user.last_name)
    if get_phone_number(msg.from_id):
       await msg.answer_photo(
            photo='https://t.me/biypulmagliwmat/4', 
            caption="Ассалаўма әлейкум", reply_markup=menu_btn())
    else:
        await msg.answer("Ассалаўма әлейкум! Боттан толық пайдаланыў ушын телефон номериңиз арқалы дизимнен өтиң!", reply_markup=phone_number)
        await PhoneForm.next()

@dp.message_handler(state=PhoneForm, content_types=['text', 'contact'])
async def Bot_Phone_Form(msg: types.Message, state: FSMContext):
    try:
        phone = msg.contact.phone_number
    except: phone = msg.text
  
    regex = "^[\+]?(998)?([- (])?(90|91|93|94|95|98|99|33|97|71|75)([- )])?(\d{3})([- ])?(\d{2})([- ])?(\d{2})$"
    if re.search(regex, phone):
        update_phone_number(msg.from_id, phone)
        await msg.answer_photo(
                photo='https://t.me/biypulmagliwmat/14', 
                caption="Ассалаўма әлейкум",
                reply_markup=menu_btn())
        await state.finish()
    else: await msg.reply("Номер қәте киритилди! Төмендеги Телефон номерди жибериў түймесин басың!")

@dp.callback_query_handler(lambda call: 'order_id=' in call.data)
async def set_order(call: types.CallbackQuery):
    await call.message.answer('💬 Рахмет, муражатыныз қабыл қылынды, қанийгемиз сиз бенен тез арада байланысады!')
    m_id = call.data.split('=')[1]
    data_user = get_user(call.from_user.id)[0]
    data_msg = by_message(m_id)
    await dp.bot.send_photo(-1001887267192, 
        photo=data_msg[0][3],
        caption=f"{data_msg[0][2]}\n\n👤 {data_user[2]}\n🌐 @{data_user[1]}\n📞 {data_user[4]}")
    await call.message.delete()
    
@dp.message_handler(content_types=['text'])
async def qeuiz_answer(msg: types.Message):
    if msg.text == '➡️ Бас бөлимге қайтыў':
        await msg.answer("Ассалаўма әлейкум", reply_markup=menu_btn())
    if msg.text == 'Биз қандай ислеймиз':
        await msg.answer_photo(
                photo='https://t.me/biypulmagliwmat/6', 
                caption="<b>Рабочее время:</b>\n<b>Часы каждый день: \n🕰 9:00-19:00</b> \n\n<a href='https://www.google.com/maps?q=42.460496,59.610029&ll=42.460496,59.610029&z=16'>Локация</a> \n\n<b>Наш подход</b> \n\n<b>Пошаговая методика работы:</b>\nНад проектом работает команда: архитектор и дизайнер занимаются дизайном и чертежами, комплектатор подбирает материалы, а технадзор следит за строителями. \n\n<b>Следим за бюджетом проектов:</b>\nМы заботимся о том, чтобы все отделочные материалы и мебель, которые будут использоваться, были реальны и имели адекватную бюджету стоимость. Цель–максимальное соответствие реализации к дизайну.\n\n<b>Нерешаемых задач не существует:</b>\nКаждый год в нашей сфере появляются новые материалы, приёмы и технологии. Мы погружаемся в тему, находим нужных специалистов и реализуем.", 
                reply_markup=menu_btn())
    if msg.text == 'Бийпул маглыумат':
        data_user = get_user(msg.from_id)[0]
        await msg.reply("Сиз бенен тез арада админлеримиз байланысады!", reply_markup=menu_btn())
        await dp.bot.send_message(-1001857875483, f"👤 {data_user[2]}\n🌐 @{data_user[1]}\n📞 {data_user[4]}")
    data = get_category(msg.text)
    if data:
        category_id = data[0][0]
        data_2 = get_message(cate_id=category_id)
        for x in data_2:
            await msg.answer_photo(x[3], x[2], reply_markup=order_btn(x[0]))
            await asyncio.sleep(.07)
    else:
        for x in menu():
            if x[1] == msg.text:
                menu_id = by_menu(msg.text)[0][0]
                await msg.answer(msg.text, reply_markup=category_btn(menu_id))
                await asyncio.sleep(.07)

