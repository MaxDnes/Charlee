# To send a message
# await context.bot.send_message(chat_id=update.effective_chat.id, text='Launched successfuly')
# await update.message.reply_text('Launched successfuly')
import openai

a = {"role": "assistant",
     "content": "I'm sorry, as an AI language model, I do not have access to real-time information. Please provide the current date or time and timezone so that I can help you accordingly."}
print(a["content"])

try:
    # eException var = openai.error.RateLimitError
    print(1 + 1)
except openai.error.RateLimitError as d:
    print(d.error)
