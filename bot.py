import os

import telebot
from dotenv import load_dotenv

from repl.service import execute_python_code

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHAT = os.getenv('CHAT')

START_AUTHENTICATED = 'Oh, hi {}!'
START_ANONIMUS = (
    'Hello! Sorry, you do not have permissions to use this bot.'
    'Contact @vilagov for permission request.'
)
HELP = 'Some help text'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # is authenticated
    bot.send_message(message.from_user.id, START_ANONIMUS)
    bot.send_message(
        CHAT, f'user with id:{message.from_user.id} has just called this bot.')


@bot.message_handler(commangs=['help'])
def send_help_text(message):
    # is authenticated
    bot.send_message(message.from_user.id, HELP)


@bot.message_handler(commands=['begin'])
def prapare_to_parce(message):
    # is authenticated
    message = bot.send_message(message.from_user.id, 'Send me your code.')
    bot.register_next_step_handler(message, parce_python_code)


def parce_python_code(message):
    output = execute_python_code(message.text)
    bot.send_message(message.from_user.id, output)


bot.polling()
