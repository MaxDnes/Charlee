from telegram import InlineKeyboardMarkup, InlineKeyboardButton

start_btns = InlineKeyboardMarkup([
    [InlineKeyboardButton('Help❓', callback_data='help'),
     InlineKeyboardButton('FAQ❔', callback_data='faq')],
    [InlineKeyboardButton('Email📬', callback_data='email'),
     InlineKeyboardButton('Tasks📋', callback_data='tasks')],
    [InlineKeyboardButton('Contact us💭', callback_data='contact_us')],
    [InlineKeyboardButton('Miscellaneous commands🎲', callback_data='misc'),
     InlineKeyboardButton('AI commands🤖', callback_data='ai')]
])

feedback_btns = InlineKeyboardMarkup([
    [InlineKeyboardButton('Report a bug❗️', callback_data='bug_report')],
    [InlineKeyboardButton('Leave a review🌟', callback_data='review')],
    [InlineKeyboardButton('Help❓', callback_data='help_contact')],
    [InlineKeyboardButton('Return ⬅️', callback_data='return')]
])

await_input_btns = InlineKeyboardMarkup([
    [InlineKeyboardButton('Cancel❌', callback_data='cancel_input')]
])

email_btns = InlineKeyboardMarkup([
    [InlineKeyboardButton('Generate📥', callback_data='generate')],
    [InlineKeyboardButton('List📧', callback_data='list')],
    [InlineKeyboardButton('Help❓', callback_data='help_emails')],
    [InlineKeyboardButton('Return ⬅️', callback_data='return')]
])

unique_email_btns = InlineKeyboardMarkup([
    [InlineKeyboardButton('Refresh🔄', callback_data='refresh')],
    [InlineKeyboardButton('Delete🚫', callback_data='delete')],
    [InlineKeyboardButton('Return ⬅️', callback_data='return_to_mail')]
])

task_btns = InlineKeyboardMarkup([
    [InlineKeyboardButton('Add task➕', callback_data='add_task')],
    [InlineKeyboardButton('View active tasks📋', callback_data='tasks_list')],
    [InlineKeyboardButton('View completed tasks✅', callback_data='completed_task_list')],
    [InlineKeyboardButton('Help❓', callback_data='help_tasks')],
    [InlineKeyboardButton('Return ⬅️', callback_data='return')]
])

misc_btns = InlineKeyboardMarkup([
    [InlineKeyboardButton('Fact📚', callback_data='fact'),
     InlineKeyboardButton('Quote💬', callback_data='quote')],
    [InlineKeyboardButton('Joke🎭', callback_data='joke'),
     InlineKeyboardButton('Roll a dice🎲', callback_data='dice_roll')],
    [InlineKeyboardButton('Cat fact🐈', callback_data='cat_fact'),
     InlineKeyboardButton('Dog fact🐕', callback_data='dog_fact')],
    [InlineKeyboardButton('View profile👤', callback_data='view_profile')],
    [InlineKeyboardButton('Return ⬅️', callback_data='return')]
])

ai_btns = InlineKeyboardMarkup([
    [InlineKeyboardButton('Ask❔', callback_data='ask')],
    [InlineKeyboardButton('Generate Image🎨', callback_data='generate_image')],
    [InlineKeyboardButton('Return ⬅️', callback_data='return')]
])
