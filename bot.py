import os

import telebot
import psycopg2
from dotenv import dotenv_values

from service import db
from service.repl import execute_python_code

START_AUTHENTICATED = 'Oh, hi {}!'
START_ANONIMUS = (
    "Sorry, you don't have permissions to use this bot.\n"
    "Contact @vilagov if you sure that you need one."
)
HELP_ADMIN = (
    'Commands:\n'
    '/repl - send and execute python code\n'
    '/users - show all users\n'
)
env = dotenv_values('.env')

TOKEN = env.get('TOKEN')
CHAT = env.get('USER_ID')

bot = telebot.TeleBot(TOKEN)
connect, cursor = db.connect_database(env)


def permission_check(func):
    """
    User permission check decorator.
    If user id not in database, send 'deny access' message.
    """
    def inner(message):
        if db.user_has_permissions(cursor, message.from_user.id):
            func(message)
        else:
            bot.send_message(message.from_user.id, START_ANONIMUS)
            bot.send_message(
                CHAT,
                'User has just called me.\n'
                f'first: {message.from_user.first_name}\n'
                f'last: {message.from_user.last_name}\n'
                f'username: @{message.from_user.username}\n'
                f'id: {message.from_user.id}\n'
            )
    return inner


@bot.message_handler(commands=['start'])
@permission_check
def send_welcome(message):
    """Say hi to user"""
    user_id = message.from_user.id
    name = message.from_user.first_name
    bot.send_message(user_id, START_AUTHENTICATED.format(name))


@bot.message_handler(commands=['help'])
@permission_check
def send_help_text(message):
    """Send help text with command list"""
    bot.send_message(message.from_user.id, HELP)


@bot.message_handler(commands=['repl'])
@permission_check
def prepare_to_parce_python_code(message):
    """Start pseudo REPL and wait for message with code"""
    message = bot.send_message(message.from_user.id, 'Send me your code')
    bot.register_next_step_handler(message, parce_python_code)


def parce_python_code(message):
    """Execute given code and send output (stdin, stderr) to user"""
    output = execute_python_code(message.text)
    bot.send_message(message.from_user.id, output)


@bot.message_handler(commands=['users'])
@permission_check
def send_list_users(message):
    """Send users list"""
    users = db.list_users(cursor)
    bot.send_message(message.from_user.id, users)


bot.polling()
connect.close()
