from aiogram.dispatcher.filters.state import StatesGroup, State

class MessageForm(StatesGroup):
    photo = State()
    text = State()
   
class CategoryForm(StatesGroup):
    name = State()

class SendAll(StatesGroup):
    msg = State()
    forward = State()