import subprocess

from telegram.ext import CommandHandler
from telegram.ext import Updater

from .config import BOT_TOKEN, TG_ID, MAC

def power_on(update, context):
    user_id = update.effective_chat.id
    if str(user_id) == TG_ID:
        p = subprocess.run(["wakeonlan", MAC])
        context.bot.send_message(chat_id=user_id, text="Done!")

def start_bot():
    updater = Updater(token=BOT_TOKEN)
    power_on_handler = CommandHandler('on', power_on)
    updater.dispatcher.add_handler(power_on_handler)
    updater.start_polling()
