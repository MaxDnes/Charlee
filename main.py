import sys
import telegram.ext
from telegram.ext import CallbackQueryHandler, MessageHandler, filters
from handlers.handlers import *
from openai_chat.openai_chat import *

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
application = telegram.ext.ApplicationBuilder().token(TOKEN).build()


def main():
    try:
        connectToDB()
        handlers = [start, quote, fact, profile, email, tasks, ai, help, faq]
        for handler_func in handlers:
            application.add_handler(telegram.ext.CommandHandler(handler_func.__name__, handler_func))

        application.add_handler(CallbackQueryHandler(query_handler))

        application.add_handler(MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=enter_prompt))

        print('Bot started')
        application.run_polling()
    except mysql.connector.Error as e:
        print("Failed to connect to MySQL database:", e)
        log_event('Error', 'Failed to connect to the database')
        sys.exit(1)
    except Exception as e:
        print("Failed to start the bot: ", e)
        log_event('Error', 'Failed to start the bot')
        sys.exit(1)



if __name__ == '__main__':
    main()

