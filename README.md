# Python Bot
## Description
Python Bot allows you to execute python code remotly on your server through telegram bot.

Before each request the user is verified by ID, which are stored in the local database.
Users whose identifiers are not present in the database do not have access to bot.

At the same time, bot admin can optionally receive notifications of any unwanted requests to the bot.

## Usage
Bot unsersteands next commands:
* `/start` - greet user (if bot knows his ID);
* `/users` - get bot users list;
* `/repl` - execute python code;
* `/list` - show the list of installed pip packages;
* `/install` - install pip package;
* `/uninstall` - uninstall pip package.

On every command from unknown user bot sends him "deny message" with author username for directly access request.
Additionaly, if you want to be aware of all requests from unknown users, you can setup `LOGIN_ATTEMPT_ALERT=True` in your .env file.
With this option bot sends you unknown user's information on his every request.

### /repl
On `/repl` command bot is waiting python code to execute it in pseudo REPL mode (code executes in a tempfile, which deletes immediately after executing).
This avoids the accumulation of garbage inside the project, and is suitable for executing small chunks of code.

### /install
On this command bot will ask user what pip package he wants to install and send the result in next message.

### /uninstall
Works same as `/install` command, but removes pip package.

Be careful! Don't delete any packages you didn't install manually!

## Deploying
Bot works with PostgreSQL database system, so before installing project to your machine you must be sure, that postgresql works correctly on port `5432`.

If you don't have it, you can download client from [official website](https://www.postgresql.org/download/), or run it in [docker container](https://hub.docker.com/_/postgres) (don't forget to open `5432` ports for your host machine).

1. [Create](https://core.telegram.org/bots#6-botfather) your telegram bot with [@BotFather](https://t.me/BotFather)
2. Clone repository to your server.
3. Create .env file with next wariables:
* `TOKEN` - your bot api token;
* `USER_ID` - your telegram user ID;
* `USER_USERNAME` - your telegram user username;
* `LOGIN_ATTEMPT_ALERT` -  `True` if you want to recieve messages from bot on every unwanted request, otherwice do not specify at all;
* `POSTGRES_DB` - postgres database;
* `POSTGRES_USER` - your postgres username;
* `POSTGRES_PASSWORD` - your postgres password;
* `POSTGRES_HOST` - postgers host;
* `POSTRGES_PORT` - posrgres port.
4. Check if postgres is currently running on your machine or container and available for connections.
5. Create virtual environment and activate it through `python -m venv venv` and `source venv/bin/activate` (highly recommended). If you using [Poetry](https://python-poetry.org/), you are able to use Make commands on next steps.
6. Install packages: `pip install -r requirements.txt` or `make install`.
7. Prepate your datbase: `python prepare.py` or `make prepare` (script connects to your database and creates table "users" with first and only values - your username and telegram ID).
8. Activate your bot: `python bot.py` or `make up`.
9. Congradulations! Now you can check your bot and let him execute your python commands.

## System requirements

* Ubuntu 16.^
* macOS High Sierra 10.13.6

## Stack

* [Python 3.9](https://www.python.org/)
* [PostgreSQL 13.2](https://www.postgresql.org)
* [pyTelegramBotAPI 0.3.0](https://pypi.org/project/pyTelegramBotAPI/0.3.0/)

## Author

Evan Vilagov

Linkedin: https://www.linkedin.com/in/vilagov/

Email: evan.vilagov@gmail.com
