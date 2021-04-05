from telegram.ext import CommandHandler
from telegram.ext import Updater

from .cmd import global_ip, power_on, power_off
from .config import BOT_TOKEN


def start_bot():
    updater = Updater(token=BOT_TOKEN)
    power_on_handler  = CommandHandler('on',  power_on)
    power_off_handler = CommandHandler('off', power_off)
    global_ip_handler = CommandHandler('ip',  global_ip)
    updater.dispatcher.add_handler(power_on_handler)
    updater.dispatcher.add_handler(power_off_handler)
    updater.dispatcher.add_handler(global_ip_handler)
    updater.start_polling()
