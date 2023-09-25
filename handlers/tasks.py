import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from buttons.buttons_layouts import task_btns
import datetime
import calendar
from database.tasks import *


async def send_task_list(update: telegram.Update, user_id, context):
    tasks = get_tasks(user_id, 'todo')
    if len(tasks) >= 1:
        text = 'Your pending tasks:\n'
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Your pending tasks:")
        task_list = []
        for i, task in enumerate(tasks):
            text += f'{i + 1}. {task[2]}      Due🕒{task[6] if task[6] else "-"} {task[7] if task[7] else "-"}\n'
            task_list.append([InlineKeyboardButton(text=f'{i + 1}', callback_data=f'task_{task[0]}')])
        task_list.append([InlineKeyboardButton('Return ⬅️', callback_data='return_to_tasks')])
        buttons = InlineKeyboardMarkup(task_list)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{text}\nChoose a task",
                                       reply_markup=buttons)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You don't have any pending tasks!",
                                       reply_markup=task_btns)


async def send_calendar(update: telegram.Update, context, task_id, msg_id, month=None, year=None):
    if task_id is None:
        return
    now = datetime.datetime.now()
    year = now.year if year is None else year
    month = now.month if month is None else month
    markup = []
    if month > 12:
        year += 1
        month = 1
    elif month < 1:
        year -= 1
        month = 12
    header_btns = [
        InlineKeyboardButton(f"{calendar.month_name[month]}", callback_data="ignore"),
        InlineKeyboardButton(f"{year}", callback_data="year")
    ]
    markup.append(header_btns)

    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    markup.append([InlineKeyboardButton(day, callback_data="ignore") for day in days_of_week])

    for week in calendar.monthcalendar(year, month):
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data="ignore"))
            else:
                button_text = str(day)
                callback_data = f"calendar:{year}-{month:02d}-{day:02d}:{task_id}"
                row.append(InlineKeyboardButton(button_text, callback_data=callback_data))
        markup.append(row)
    footer_btns = [
        InlineKeyboardButton("◀️ Prev", callback_data=f"calendar:prev:{year}-{month:02d}-{task_id}"),
        InlineKeyboardButton("Cancel", callback_data="calendar:cancel"),
        InlineKeyboardButton("Remove", callback_data=f"calendar:remove_due_date_{task_id}"),
        InlineKeyboardButton("▶️ Next", callback_data=f"calendar:next:{year}-{month:02d}-{task_id}")
    ]
    markup.append(footer_btns)
    markup = InlineKeyboardMarkup(markup)
    await context.bot.editMessageText(chat_id=update.effective_chat.id, message_id=msg_id,
                                        text="Please pick a due date for your task",
                                        reply_markup=markup)


async def send_clock(update: telegram.Update, context, task_id, msg_id, hour=None, minutes=None):
    if task_id is None:
        return

    markup = []
    header_btns = [
        InlineKeyboardButton(f"Hours", callback_data="ignore")
    ]
    markup.append(header_btns)
    temp_row = []
    for i in range(24):
        text = f"[{i:02d}]" if hour == f'{i:02d}' else f"{i:02d}"
        temp_row.append(InlineKeyboardButton(text, callback_data=f"set_hour_{i:02d}"))
        if len(temp_row) == 6:
            markup.append(temp_row)
            temp_row = []

    markup.append([InlineKeyboardButton("Minutes", callback_data="ignore")])
    minutes_text = ["00", "15", "30", "45"]
    for i, minute in enumerate(minutes_text):
        text = f"[{minute}]" if minutes == minute else minute
        minutes_text[i] = text

    markup.append([
        InlineKeyboardButton(minutes_text[0], callback_data="set_minutes_00"),
        InlineKeyboardButton(minutes_text[1], callback_data="set_minutes_15"),
        InlineKeyboardButton(minutes_text[2], callback_data="set_minutes_30"),
        InlineKeyboardButton(minutes_text[3], callback_data="set_minutes_45")
    ])

    footer_btns = [
        InlineKeyboardButton("Cancel", callback_data="calendar:cancel"),
        InlineKeyboardButton("OK", callback_data="set_due_time:confirm")
    ]
    markup.append(footer_btns)
    markup = InlineKeyboardMarkup(markup)
    await context.bot.editMessageText(chat_id=update.effective_chat.id, message_id=msg_id,
                                          text="Please pick a due time for your task",
                                          reply_markup=markup)



async def send_completed_task_list(update: telegram.Update, user_id, context):
    tasks = get_tasks(user_id, 'done')
    if len(tasks) >= 1:
        text = 'Your completed tasks:\n'
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Your completed tasks:")
        for i, task in enumerate(tasks):
            text += f'{i + 1}. {task[2]}      Due🕒{task[6] if task[6] else "-"} {task[7] if task[7] else "-"}   was completed✅ at {task[5]} \n'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=task_btns)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You don't have any completed tasks!",
                                       reply_markup=task_btns)


async def get_task_info(task_id):
    task = get_task(task_id)
    text = f'Task:{task[2]}\n\nDue🕒  {task[6] if task[6] else "-"} {task[7] if task[7] else "-"}\n\nCreated at: {task[4]}'
    return text


async def handle_task_actions(update: telegram.Update, data, context):
    task_id = data[5:]
    text = await get_task_info(task_id)
    unique_task_btns = InlineKeyboardMarkup([
        [InlineKeyboardButton('Mark as complete✅', callback_data=f'complete_task_{task_id}')],
        [InlineKeyboardButton('Set due date📆', callback_data=f'set_due_date_task_{task_id}'),
         InlineKeyboardButton('Set due time⏰', callback_data=f'set_due_time_task_{task_id}')],
        [InlineKeyboardButton('Delete❌', callback_data=f'delete_task_{task_id}')],
        [InlineKeyboardButton('Return⬅️', callback_data='return_to_tasks')]
    ])
    msg_id = await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=unique_task_btns)
    return msg_id.message_id


async def get_task_markup(update: telegram.Update, data, context):
    task_id = data[5:]
    unique_task_btns = InlineKeyboardMarkup([
        [InlineKeyboardButton('Mark as complete✅', callback_data=f'complete_task_{task_id}')],
        [InlineKeyboardButton('Set due date📆', callback_data=f'set_due_date_task_{task_id}'),
         InlineKeyboardButton('Set due time⏰', callback_data=f'set_due_time_task_{task_id}')],
        [InlineKeyboardButton('Delete❌', callback_data=f'delete_task_{task_id}')],
        [InlineKeyboardButton('Return⬅️', callback_data='return_to_tasks')]
    ])
    return unique_task_btns
