from aiogram import Bot, Dispatcher, executor, types
from intercity_bot.database import Database
from intercity_bot.user import User

bot = Bot(token="1007238034:AAHQ-CEPrFkuReeUVlB9_9vm8X1kpLJ9AcA")
dispatcher = Dispatcher(bot)

db = Database()



@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    user = db.get_user_telegram(message.from_user.id)
    if user is None:
        user = db.create_user(message.from_user.id)

    answer = "Привет, {name}, я помогу тебе быстро купить билеты на Интерсити."
    answer = answer.format(name=message.from_user.first_name)
    await bot.send_message(message.chat.id, answer)

    await search_ticket(user)


@dispatcher.message_handler()
async def handle_message(message: types.Message):
    user = db.get_user_telegram(message.from_user.id)
    if user is None:
        user = db.create_user(message.from_user.id)

    if user.session[0] == 'ask-from':
        pass


async def search_ticket(user):
    answer = "Напиши станцию отправления."
    await bot.send_message(user.telegram_id, answer)

    user.update_session(['ask-from'])


def run():
    executor.start_polling(dispatcher)