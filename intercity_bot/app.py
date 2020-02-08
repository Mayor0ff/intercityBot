import json
import datetime
from aiogram import Bot, Dispatcher, executor, types
from intercity_bot import uz
from intercity_bot.database import Database
from intercity_bot.user import User
from intercity_bot.telegram_calendar import create_calendar

bot = Bot(token="1007238034:AAHQ-CEPrFkuReeUVlB9_9vm8X1kpLJ9AcA")
dispatcher = Dispatcher(bot)

db = Database()
cache = {"stations": {}}


@dispatcher.message_handler(commands=["start"])
async def start(message: types.Message):
    user = db.get_user_telegram(message.from_user.id)
    if user is None:
        user = db.create_user(message.from_user.id)

    answer = "Привет, {name}, я помогу тебе быстро купить билеты на Интерсити."
    answer = answer.format(name=message.from_user.first_name)
    await bot.send_message(message.chat.id, answer)

    await search_station_from(user)


@dispatcher.message_handler(commands=["stop"])
async def stop(message: types.Message):
    db.connection.close()


@dispatcher.message_handler()
async def handle_message(message: types.Message):
    user = db.get_user_telegram(message.from_user.id)
    if user is None:
        user = db.create_user(message.from_user.id)

    if "0" in user.session:
        if user.session["0"] == "ask-from":
            stations = await uz.search_stations(message.text)

            for station in stations:
                cache["stations"][station.id] = station

            if len(stations) == 0:
                answer = "Не могу найти станции с таким названием 😞"
                await bot.send_message(user.telegram_id, answer, parse_mode="html")
            elif len(stations) == 1:
                station = stations[0]
                user.session["station-from"] = station.toDict()
                user.update_session(user.session)
                await search_station_to(user)
            else:
                buttons = map(
                    lambda station: types.InlineKeyboardButton(
                        text=station.title,
                        callback_data=json.dumps({"a": "st-from", "st": station.id}),
                    ),
                    stations,
                )

                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(*buttons)

                answer = "🚉 Выбери станцию из предложенных вариантов"
                await bot.send_message(user.telegram_id, answer, reply_markup=markup)
        elif user.session["0"] == "ask-to":
            stations = await uz.search_stations(message.text)

            for station in stations:
                cache["stations"][station.id] = station

            if len(stations) == 0:
                answer = "Не могу найти станции с таким названием 😞"
                await bot.send_message(user.telegram_id, answer)
            elif len(stations) == 1:
                station = stations[0]
                user.session["station-to"] = station.toDict()
                user.update_session(user.session)
                await search_station_to(user)
            else:
                buttons = map(
                    lambda station: types.InlineKeyboardButton(
                        text=station.title,
                        callback_data=json.dumps({"a": "st-to", "st": station.id}),
                    ),
                    stations,
                )

                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(*buttons)

                answer = "🚉 Выбери станцию из предложенных вариантов"
                await bot.send_message(user.telegram_id, answer, reply_markup=markup)


@dispatcher.callback_query_handler()
async def handle_callback_query(callback_query: types.CallbackQuery):
    user = db.get_user_telegram(callback_query.from_user.id)
    if user is None:
        user = db.create_user(callback_query.from_user.id)

    callback_data = json.loads(callback_query.data)
    if callback_data["a"] == "dismiss":
        await callback_query.answer()
    elif callback_data["a"] == "st-from":
        if callback_data["st"] in cache["stations"]:
            station = cache["stations"][callback_data["st"]]
            user.session["station-from"] = station.toDict()
            user.update_session(user.session)

            await callback_query.answer()
            await search_station_to(user)
        else:
            await callback_query.answer("❌ Ошибка. Напиши станцию отправления снова.")
    elif callback_data["a"] == "st-to":
        if callback_data["st"] in cache["stations"]:
            station = cache["stations"][callback_data["st"]]
            user.session["station-to"] = station.toDict()
            user.update_session(user.session)

            await callback_query.answer()
            await ask_tickets_amount(user)
        else:
            await callback_query.answer("❌ Ошибка. Напиши станцию назначения снова.")
    elif callback_data["a"] == "ts-am":
        tickets_amount = callback_data["am"]
        user.session["tickets-amount"] = tickets_amount
        user.update_session(user.session)

        await callback_query.answer()
        await ask_date(user)
    elif callback_data["a"] == "calendar-month":
        message = callback_query.message
        date = datetime.datetime.strptime(callback_data["date"], "%Y-%m-%d")

        await callback_query.answer()
        await ask_date(user, message, date)
    elif callback_data["a"] == "calendar":
        date = datetime.datetime.strptime(callback_data["date"], "%Y-%m-%d")
        user.session["date"] = callback_data["date"]
        user.update_session(user.session)


async def search_station_from(user):
    answer = "✍️ Напиши станцию отправления\nНапример: <b>Киев</b>"
    await bot.send_message(user.telegram_id, answer, parse_mode="html")

    user.session[0] = "ask-from"
    user.update_session(user.session)


async def search_station_to(user):
    answer = "✍️ Напиши станцию прибытия\nНапример: <b>Днепр</b>"
    await bot.send_message(user.telegram_id, answer, parse_mode="html")

    user.session[0] = "ask-to"
    user.update_session(user.session)


async def ask_tickets_amount(user):
    markup = types.InlineKeyboardMarkup(row_width=5)
    buttons = map(
        lambda num: types.InlineKeyboardButton(
            text=num, callback_data=json.dumps({"a": "ts-am", "am": num})
        ),
        range(1, 11),
    )
    markup.add(*buttons)

    answer = "🎫 Теперь выбери сколько билетов нужно купить.\nЯ выберу места рядом."
    await bot.send_message(
        user.telegram_id, answer, reply_markup=markup, parse_mode="html"
    )


async def ask_date(user, old_message: types.Message = None, date: datetime.date = None):
    if date is None:
        date = datetime.date.today()

    calendar_markup = create_calendar(date.year, date.month)

    if old_message is None:
        answer = "📅 Теперь выбери дату <b>отправления</b>"
        await bot.send_message(
            user.telegram_id, answer, reply_markup=calendar_markup, parse_mode="html"
        )
    else:
        await bot.edit_message_reply_markup(
            user.telegram_id, old_message.message_id, reply_markup=calendar_markup
        )


def run():
    executor.start_polling(dispatcher)
