import os
import openai
from dotenv import load_dotenv
from telegram import Update
from logs.logs import error

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


async def ask(update: Update, prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=[
                {"role": "user", "content": " ".join(prompt)}
            ]
        )
        return completion.choices[0].message["content"]
    except openai.error.RateLimitError:
        await error(update, context)
    except Exception:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="We encountered an unexpected error, please report it and try again later!")
        await error(update, context)
        return "We encountered an unexpected error, please report it and try again later!"


async def generateimage(update, prompt):
    try:
        response = openai.Image.create(
            prompt=" ".join(prompt),
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return image_url
    except openai.error:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Something went wrong try again later.")
        await error(update, context)
        return "Something went wrong try again later."


