import requests
import telegram.ext
from database.database import log_event
from database.feedback import add_bug_report, add_user_review
from database.users import *
from handlers.emails import *
from handlers.tasks import *
from openai_chat.openai_chat import *
from buttons.buttons_layouts import *
from help_meesages.messages import *


user_states = {}
user_task_msg_data = {}


async def start(update: Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    if not checkUserInDB(update.effective_user.id):
        addUser(update.effective_user.id, update.effective_user.username, update.effective_user.language_code,
                update.effective_user.first_name, update.effective_user.last_name)
        await update.message.reply_text(f"Hello {update.effective_user.first_name}, it's great to have you here!",
                                        reply_markup=start_btns)
    else:
        await update.message.reply_text("No need you've already started the bot.", reply_markup=start_btns)


async def query_handler(update: Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in user_states:
        user_states[update.effective_user.id] = {}
        user_states[update.effective_user.id]['ENTER_TASK'] = 0
        user_states[update.effective_user.id]['ASK_AI'] = 0
        user_states[update.effective_user.id]['GENERATE_IMG_AI'] = 0
        user_states[update.effective_user.id]['REPORT_BUG'] = 0
        user_states[update.effective_user.id]['LEAVE_REVIEW'] = 0
    if update.effective_user.id not in user_task_msg_data:
        user_task_msg_data[update.effective_user.id] = {}
        user_task_msg_data[update.effective_user.id]['id'] = None
        user_task_msg_data[update.effective_user.id]['markup'] = None
        user_task_msg_data[update.effective_user.id]['hour'] = None
        user_task_msg_data[update.effective_user.id]['minutes'] = None
        user_task_msg_data[update.effective_user.id]['task_id'] = None
    if any(val == 1 for val in user_states[update.effective_user.id].values()):
        if 'cancel_input' in update.callback_query.data:
            user_states[update.effective_user.id] = {key: 0 for key in user_states[update.effective_user.id]}
            await send_message(update, 'Operation canceled\nChoose an action to perform', start_btns, context)
            await context.bot.answer_callback_query(update.callback_query.id)
            return
        else:
            if user_states[update.effective_user.id]['ENTER_TASK'] == 1:
                prompt = 'entering the task'
            elif user_states[update.effective_user.id]['ASK_AI'] == 1:
                prompt = 'asking the bot your question'
            elif user_states[update.effective_user.id]['GENERATE_IMG_AI'] == 1:
                prompt = 'giving the prompt for the image you wish to generate'
            elif user_states[update.effective_user.id]['REPORT_BUG'] == 1:
                prompt = 'reporting the bug'
            elif user_states[update.effective_user.id]['LEAVE_REVIEW'] == 1:
                prompt = 'leaving a review'
            else:
                prompt = 'giving an input'
            await send_message(update, f'Please either finish {prompt} or cancel the operation', await_input_btns, context)
            await context.bot.answer_callback_query(update.callback_query.id)
            return


    data = update.callback_query.data
    t_id = update.effective_user.id
    user_id = get_user_info(t_id)['id']
    mail_addr_count = get_mail_addr_count(user_id)

    actions = {
        'help': lambda: send_message(update, help_msg, start_btns, context),
        'faq': lambda: send_message(update, faq_msg, start_btns, context),
        'contact_us': lambda: send_message(update, "What do you wish to tell us", feedback_btns, context),
        'help_contact': lambda: send_message(update, contact_help, feedback_btns, context),
        'email': lambda: send_message(update, "What action do you want to perform.", email_btns, context),
        'tasks': lambda: send_message(update, "Choose an action to perform", task_btns, context),
        'misc': lambda: send_message(update, "Choose a command:", misc_btns, context),
        'return': lambda: send_message(update, "Choose an action to perform", start_btns, context),
        'return_to_mail': lambda: send_message(update, "Choose an action to perform", email_btns, context),
        'add_task': lambda: await_response(update, "Please enter the task you want to add.", None, context, 'add_task'),
        'tasks_list': lambda: send_task_list(update, user_id, context),
        'completed_task_list': lambda: send_completed_task_list(update, user_id, context),
        'help_tasks': lambda: send_message(update, task_help, start_btns, context),
        'generate': lambda: generate_email(update, context, user_id, mail_addr_count),
        'help_emails': lambda: send_message(update, email_help, email_btns, context),
        'fact': lambda: fact(update, context),
        'quote': lambda: quote(update, context),
        'joke': lambda: get_joke(update, context),
        'dice_roll': lambda: get_dice_roll(update, context),
        'cat_fact': lambda: get_random_cat_fact(update, context),
        'dog_fact': lambda: get_random_dog_fact(update, context),
        'view_profile': lambda: profile(update, context),
        'ai': lambda: send_message(update, "Please select a command: ", ai_btns, context),
        'ask': lambda: await_response(update, "Please enter your question below: ", None, context, 'ask'),
        'generate_image': lambda: await_response(update, "Please enter your image prompt below: ", None, context, 'generate_img'),
        'bug_report': lambda: await_response(update, "Please describe your bug below:", None, context, 'bug_report'),
        'review': lambda: await_response(update, "We will gladly take note of your review!", None, context, 'leave_review')
    }

    if data in actions:
        await actions[data]()

    if data == 'return_to_tasks':
        await send_message(update, 'Choose a task', task_btns, context)
        user_task_msg_data[update.effective_user.id] = {key: None for key in user_task_msg_data[update.effective_user.id]}


    if len(get_tasks(user_id, 'todo')) >= 1:
        if data.startswith('task_'):
            user_task_msg_data[update.effective_user.id]['id'] = await handle_task_actions(update, data, context)
            user_task_msg_data[update.effective_user.id]['markup'] = await get_task_markup(update, data, context)
            user_task_msg_data[update.effective_user.id]['task_id'] = data[5:]
        if user_task_msg_data[update.effective_user.id]['id'] is not None and user_task_msg_data[update.effective_user.id]['markup'] is not None:
            if data.startswith('complete_task_'):
                complete_task(data.replace('complete_task_', ''))
                await context.bot.editMessageText(chat_id=update.effective_chat.id, message_id=user_task_msg_data[update.effective_user.id]['id'],
                                                  text="✅Task successfully marked as completed!", reply_markup=task_btns)
                user_task_msg_data[update.effective_user.id] = {key: None for key in user_task_msg_data.get(update.effective_user.id, {})}
            elif data.startswith('delete_task'):
                delete_task(data[12:])
                await context.bot.editMessageText(chat_id=update.effective_chat.id, text="❌Task deleted successfully!", message_id=user_task_msg_data[update.effective_user.id]['id'],
                                                  reply_markup=task_btns)
                user_task_msg_data[update.effective_user.id] = {key: None for key in user_task_msg_data[update.effective_user.id]}

            elif data.startswith('set_due_date_task_'):
                task_id = data.replace('set_due_date_task_', '')
                await send_calendar(update, context, task_id, user_task_msg_data[update.effective_user.id]['id'])
            elif data.startswith('set_due_time_task_'):
                task_id = data.replace('set_due_time_task_', '')
                await send_clock(update, context, task_id, user_task_msg_data[update.effective_user.id]['id'])
                user_task_msg_data[update.effective_user.id]['task_id'] = task_id
            elif data.startswith('set_hour_'):
                hour = data[9:]
                await context.bot.editMessageText(chat_id=update.effective_chat.id,
                                                  message_id=user_task_msg_data[update.effective_user.id]['id'],
                                                  text=f"Due date has been removed successfully\n{await get_task_info(user_task_msg_data[update.effective_user.id]['task_id'])}",
                                                  reply_markup=user_task_msg_data[update.effective_user.id]['markup'])
                await send_clock(update, context,user_task_msg_data[update.effective_user.id]['task_id'], user_task_msg_data[update.effective_user.id]['id'], hour)
                user_task_msg_data[update.effective_user.id]['hour'] = hour
            elif data.startswith('set_minutes_'):
                minutes = data[12:]
                await context.bot.editMessageText(chat_id=update.effective_chat.id,
                                                  message_id=user_task_msg_data[update.effective_user.id]['id'],
                                                  text=f"Due date has been removed successfully\n{await get_task_info(user_task_msg_data[update.effective_user.id]['task_id'])}",
                                                  reply_markup=user_task_msg_data[update.effective_user.id]['markup'])
                await send_clock(update, context, user_task_msg_data[update.effective_user.id]['task_id'],
                                 user_task_msg_data[update.effective_user.id]['id'], None, minutes)
                user_task_msg_data[update.effective_user.id]['minutes'] = minutes
            elif data.startswith('set_due_time:confirm'):
                if user_task_msg_data[update.effective_user.id]['minutes'] is not None and user_task_msg_data[update.effective_user.id]['hour'] is not None:
                    set_due_time(user_task_msg_data[update.effective_user.id]['task_id'], user_task_msg_data[update.effective_user.id]['hour'], user_task_msg_data[update.effective_user.id]['minutes'])
                    user_task_msg_data[update.effective_user.id]['hour'] = None
                    user_task_msg_data[update.effective_user.id]['minutes'] = None
                    await context.bot.editMessageText(chat_id=update.effective_chat.id, text=f"Task due time changed successfully\n{await get_task_info(user_task_msg_data[update.effective_user.id]['task_id'])}", message_id=user_task_msg_data[update.effective_user.id]['id'], reply_markup=user_task_msg_data[update.effective_user.id]['markup'])


            if data.startswith('calendar:'):
                if data.startswith('calendar:prev:'):
                    year = int(data[14:18])
                    month = int(data[19:21]) - 1
                    task_id = data[22:]
                    await send_calendar(update, context, task_id, month, year, user_task_msg_data[update.effective_user.id]['id'])
                elif data.startswith('calendar:next:'):
                    year = int(data[14:18])
                    month = int(data[19:21]) + 1
                    task_id = data[22:]
                    await send_calendar(update, context, task_id, month, year, user_task_msg_data[update.effective_user.id]['id'])
                elif data.startswith('calendar:cancel'):
                    await context.bot.editMessageText(chat_id=update.effective_chat.id, message_id=user_task_msg_data[update.effective_user.id]['id'], text=f"Operation cancelled successfully\n{await get_task_info(user_task_msg_data[update.effective_user.id]['task_id'])}", reply_markup=user_task_msg_data[update.effective_user.id]['markup'])
                elif data.startswith('calendar:remove_due_date_'):
                    task_id = data.replace('calendar:remove_due_date_', '')
                    remove_due_date(task_id)
                    await context.bot.editMessageText(chat_id=update.effective_chat.id, message_id=user_task_msg_data[update.effective_user.id]['id'], text=f"Due date has been removed successfully\n{await get_task_info(user_task_msg_data[update.effective_user.id]['task_id'])}", reply_markup=user_task_msg_data[update.effective_user.id]['markup'])
                else:
                    date = data[9:19]
                    task_id = data[20:]
                    set_due_date(task_id, date)
                    await context.bot.editMessageText(chat_id=update.effective_chat.id, text=f"Task date changed successfully\n{await get_task_info(user_task_msg_data[update.effective_user.id]['task_id'])}", message_id=user_task_msg_data[update.effective_user.id]['id'], reply_markup=user_task_msg_data[update.effective_user.id]['markup'])



    if mail_addr_count >= 1:
        if data == 'list':
            await send_email_addresses(update, user_id, context)
        elif data.startswith('email_'):
            await handle_email_actions(update, data, context)
        elif data == 'refresh':
            await refresh_email_inbox(update, context)
        elif data == 'delete':
            await delete_email_address(update, user_id, context)

    if mail_addr_count == 0:
        await send_message(update, "You don't have any emails, generate one first!", email_btns, context)
    await context.bot.answer_callback_query(update.callback_query.id)


async def send_message(update, text, reply_markup, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)


async def enter_prompt(update: Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    user_id = get_user_info(update.effective_user.id)['id']
    if user_states[update.effective_user.id]['ENTER_TASK'] == 1:
        task_content = update.message.text
        user_states[update.effective_user.id]['ENTER_TASK'] = 1
        if add_user_task(user_id, task_content):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Task added successfully!", reply_markup=task_btns)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to add task.")
        user_states[update.effective_user.id]['ENTER_TASK'] = 0
    elif user_states[update.effective_user.id]['ASK_AI'] == 1:
        prompt = update.message.text
        resp = await ask(update, prompt)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp, reply_markup=ai_btns)
        user_states[update.effective_user.id]['ASK_AI'] = 0
    elif user_states[update.effective_user.id]['GENERATE_IMG_AI'] == 1:
        prompt = update.message.text
        img = await generateimage(update, prompt)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=img, reply_markup=ai_btns)
        user_states[update.effective_user.id]['GENERATE_IMG_AI'] = 0
    elif user_states[update.effective_user.id]['REPORT_BUG'] == 1:
        bug = update.message.text
        add_bug_report(user_id, bug)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="We will look into the issue you described shortly!", reply_markup=feedback_btns)
        user_states[update.effective_user.id]['REPORT_BUG'] = 0
    elif user_states[update.effective_user.id]['LEAVE_REVIEW'] == 1:
        review = update.message.text
        add_user_review(user_id, review)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Thank you for your review!", reply_markup=feedback_btns)
        user_states[update.effective_user.id]['LEAVE_REVIEW'] = 0


async def await_response(update, text, reply_markup, context, type):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    if type == 'add_task':
        user_states[update.effective_user.id]['ENTER_TASK'] = 1
    elif type == 'ask':
        user_states[update.effective_user.id]['ASK_AI'] = 1
    elif type == 'generate_img':
        user_states[update.effective_user.id]['GENERATE_IMG_AI'] = 1
    elif type == 'bug_report':
        user_states[update.effective_user.id]['REPORT_BUG'] = 1
    elif type == 'leave_review':
        user_states[update.effective_user.id]['LEAVE_REVIEW'] = 1
    else:
        await error(update, context)


async def quote(update: Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    url = 'https://api.quotable.io/random'
    response = requests.get(url)
    if response.status_code == 200:
        quote = response.json()["content"]
        author = response.json()["author"]
        await send_message(update, f"\"{quote}\" - {author}", misc_btns, context)
    else:
        await send_message(update, "Something went wrong, try again later.", misc_btns, context)


async def fact(update: Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    url = 'http://numbersapi.com/random'
    response = requests.get(url)
    if response.status_code == 200:
        await send_message(update, response.text, misc_btns, context)
    else:
        await send_message(update, "Something went wrong, try again later.", misc_btns, context)


async def get_joke(update, context):
    url = 'https://official-joke-api.appspot.com/random_joke'
    response = requests.get(url)
    if response.status_code == 200:
        joke_data = response.json()
        await send_message(update, f"{joke_data['setup']}\n{joke_data['punchline']}", misc_btns, context)
    else:
        await send_message(update, "Something went wrong, try again later.", misc_btns, context)


async def get_random_cat_fact(update, context):
    url = 'https://meowfacts.herokuapp.com/'
    response = requests.get(url)
    if response.status_code == 200:
        cat_data = response.json()
        await send_message(update, f"Here's a random cat fact:\n{cat_data['data'][0]}", misc_btns, context)
    else:
        await send_message(update, "Something went wrong, try again later.", misc_btns, context)


async def get_random_dog_fact(update, context):
    url = 'http://dog-api.kinduff.com/api/facts'
    response = requests.get(url)

    if response.status_code == 200:
        dog_data = response.json()
        await send_message(update, f"Here's a random dog fact:\n{dog_data['facts'][0]}", misc_btns, context)
    else:
        await send_message(update, "Sorry, I couldn't fetch a random dog fact. Please try again later.", misc_btns,
                           context)


async def get_dice_roll(update, context):
    roll_result = random.randint(1, 6)
    await send_message(update, f"You rolled a {roll_result}!", misc_btns, context)



async def profile(update: Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_info = get_user_info(user.id)
    if user_info:
        profile_text = f"Your Profile:\n"
        profile_text += f"First Name: {user_info['first_name']}\n"
        profile_text += f"Last Name: {user_info['last_name']}\n"
        profile_text += f"Username: {user_info['username']}\n"
        profile_text += f"Language Code: {user_info['lang_code']}\n"
        await send_message(update, profile_text, misc_btns, context)
    else:
        await send_message(update, "Your profile information is not available.", misc_btns, context)


async def email(update: Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    await send_message(update, "What action do you want to perform.", email_btns, context)


async def tasks(update: Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    await send_message(update, "What action do you want to perform.", task_btns, context)


async def error(update: Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    log_event('Error', context.error)


async def ai(update: Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    await send_message(update, "Choose an action to perform", ai_btns, context)


async def help(update: Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    await send_message(update, help_msg, start_btns, context)


async def faq(update: Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    await send_message(update, faq_msg, start_btns, context)

