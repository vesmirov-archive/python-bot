import psycopg2


def connect_database(env):
    """Connect to database"""
    connect = psycopg2.connect(
        database=env.get('DATABASE'),
        user=env.get('POSTGRES_USERNAME'),
        password=env.get('POSTGRES_PASSWORD'),
        host=env.get('POSTGRES_HOST'),
        port=env.get('POSTRGES_PORT')
    )
    cursor = connect.cursor()
    return (connect, cursor)


def user_has_permissions(user_id, cursor):
    """Check if given id saved in databse"""
    cursor.execute("SELECT user_id FROM users")
    rows = cursor.fetchall()
    for row in rows:
        if user_id in row:
            return True
    return False
