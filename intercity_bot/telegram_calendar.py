import json
import datetime
from dateutil.relativedelta import relativedelta
from calendar import Calendar
from aiogram import types


def create_calendar(year, month):
    date = datetime.date(year, month, 1)
    today = datetime.date.today()
    calendar = Calendar()

    weeks = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Декабрь"]

    current_month = types.InlineKeyboardButton(
        text=months[date.month - 1],
        callback_data=json.dumps({"a": "dismiss"}),
    )

    week_buttons = map(
        lambda week: types.InlineKeyboardButton(
            text=week,
            callback_data=json.dumps({"a": "dismiss"}),
        ),
        weeks
    )

    date_buttons = map(
        lambda date: types.InlineKeyboardButton(
            text=str(date.day) if date >= today else "✖️",
            callback_data=json.dumps(
                {"a": "calendar", "date": date.isoformat()} if date >= today else {"a": "dismiss"}
            ),
        ),
        calendar.itermonthdates(year, month),
    )

    month_buttons = []
    prev_month = date + relativedelta(months=-1)
    if prev_month >= datetime.date(today.year, today.month, 1):
        month_buttons.append(
            types.InlineKeyboardButton(
                text="⬅️ {}".format(months[prev_month.month - 1]), 
                callback_data=json.dumps({"a": "calendar-month", "date": str(prev_month)})
            )
        )
    next_month = date + relativedelta(months=+1)
    month_buttons.append(
        types.InlineKeyboardButton(
            text="{} ➡️".format(months[next_month.month - 1]), 
            callback_data=json.dumps({"a": "calendar-month", "date": str(next_month)})
        )
    )

    calendar_markup = types.InlineKeyboardMarkup(row_width=7)
    calendar_markup.row(current_month)
    calendar_markup.add(*week_buttons)
    calendar_markup.add(*date_buttons)
    calendar_markup.row(*month_buttons)

    return calendar_markup
