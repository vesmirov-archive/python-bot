#!/usr/bin/env python
import psycopg2
from dotenv import dotenv_values

from service.db import connect_database


def main():
    """Create 'users' table in database and adds user from .env file"""

    env = dotenv_values('.env')
    connect, cursor = connect_database(env)

    try:
        cursor.execute(
            'CREATE TABLE users ('
            'user_id INT NOT NULL,'
            'username VARCHAR(100),'
            'is_admin BOOL NOT NULL);'
        )
        print('Table "users" created.')
    except psycopg2.errors.DuplicateTable:
        print('Table "users" already has been created.')
    else:
        user_id = env.get('USER_ID')
        username = env.get('USER_USERNAME')
        if user_id:
            cursor.execute(
                f"INSERT INTO users VALUES ({user_id}, '{username}', True);")

    connect.commit()
    connect.close()


if __name__ == '__main__':
    main()
