import string
import random
import secmail
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from buttons.buttons_layouts import unique_email_btns, email_btns
from database.emails import *


client = secmail.AsyncClient()


async def generate_email(update, context, user_id, mail_addr_count):
    if mail_addr_count < 10:
        domains = await client.get_active_domains()
        domain = random.choice(domains)
        username = "".join(random.choices(string.ascii_lowercase + string.digits, k=12))
        address = username + '@' + domain
        add_email(address, user_id)

        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your new email address: {address}.",
                                       reply_markup=unique_email_btns)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"You can't have more than 10 email addresses at once!.",
                                       reply_markup=email_btns)


async def send_email_addresses(update, user_id, context):
    addresses = [address[0] for address in get_mail_addr(user_id)]
    addresses_btns = []
    for address in addresses:
        addresses_btns.append([InlineKeyboardButton(text=address, callback_data=f'email_{address}')])
    addresses_btns.append([InlineKeyboardButton('Return ⬅️', callback_data='return_to_mail')])
    addresses = InlineKeyboardMarkup(addresses_btns)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Your available emails', reply_markup=addresses)


async def handle_email_actions(update, data, context):
    email_address = data[6:]
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'What action do you wish to perform for {email_address}:',
                                   reply_markup=unique_email_btns)


async def refresh_email_inbox(update, context):
    for word in update.callback_query.message.text.split():
        if '@' in word:
            email_address = word.strip(':')
    messages = await client.get_inbox(email_address)
    if len(messages) >= 1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{email_address} inbox📬:")
        for message in messages:
            msg = await client.get_message(email_address, message.id)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"From: {msg.from_address}\nDate: {msg.date}\nSubject: {msg.subject}\nMessage: {msg.text_body}")
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"Choose an action to perform for {email_address}", reply_markup=unique_email_btns)


async def delete_email_address(update, user_id, context):
    for word in update.callback_query.message.text.split():
        if '@' in word:
            email_address = word.strip(':')
            delete_addr(user_id, email_address)
            break
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Email deleted successfully.\nChoose an action to perform",
                                   reply_markup=email_btns)