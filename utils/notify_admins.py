import logging

from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(chat_id=admin, text="Bot on")
        except Exception as err:
            logging.exception(err)
