import os

import telebot
import psycopg2
from dotenv import load_dotenv

from service import db
from service.repl import execute_python_code

START_AUTHENTICATED = 'Oh, hi {}!'
START_ANONIMUS = (
    "Sorry, you don't have permissions to use this bot.\n"
    "Contact @vilagov if you sure that you need one."
)
HELP = 'Some help text'

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHAT = os.getenv('CHAT')

bot = telebot.TeleBot(TOKEN)
connect = psycopg2.connect(
    database=os.getenv('DATABASE'),
    user=os.getenv('POSTGRES_USERNAME'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTRGES_PORT')
)
cursor = connect.cursor()


def permission_check(func):
    def inner(message):
        if db.user_has_permissions(message.from_user.id, cursor):
            func(message)
        else:
            bot.send_message(message.from_user.id, START_ANONIMUS)
            bot.send_message(
                CHAT,
                'User has just called me.\n'
                f'name: {message.from_user.first_name}'
                f'username: @{message.from_user.username}\n'
                f'id: {message.from_user.id}\n'
            )
    return inner


@bot.message_handler(commands=['start'])
@permission_check
def send_welcome(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    bot.send_message(user_id, START_AUTHENTICATED.format(name))


@bot.message_handler(commangs=['help'])
@permission_check
def send_help_text(message):
    bot.send_message(message.from_user.id, HELP)


@bot.message_handler(commands=['begin'])
@permission_check
def prapare_to_parce(message):
    message = bot.send_message(message.from_user.id, 'Send me your code.')
    bot.register_next_step_handler(message, parce_python_code)


def parce_python_code(message):
    output = execute_python_code(message.text)
    bot.send_message(message.from_user.id, output)


bot.polling()
connect.close()
