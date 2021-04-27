import psycopg2


def connect_database(env):
    """Connect to database"""

    connect = psycopg2.connect(
        database=env.get('POSTGRES_DB'),
        user=env.get('POSTGRES_USER'),
        password=env.get('POSTGRES_PASSWORD'),
        host=env.get('POSTGRES_HOST'),
        port=env.get('POSTRGES_PORT')
    )
    cursor = connect.cursor()
    return (connect, cursor)


def user_has_permissions(cursor, user_id):
    """Check if given id saved in databse"""

    cursor.execute("SELECT user_id FROM users")
    rows = cursor.fetchall()
    for row in rows:
        if user_id in row:
            return True
    return False


def list_users(cursor):
    """Show list of users"""

    cursor.execute("SELECT username, is_admin FROM users")
    rows = cursor.fetchall()
    users = []
    for row in rows:
        role = '(admin)' if row[1] else ''
        users.append(f"user: {row[0]} {role}")
    return '\n'.join(users)
