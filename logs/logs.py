from telegram import Update
from database.database import *
import telegram.ext


async def error(update: Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    if context != None:
        print(f'The event {update} raised the error {context.error}')
        log_event('Error', context.error)
    else:
        print(f'The event {update} raised the error {context}')
        log_event('Error', context)
