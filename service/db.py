

def user_has_permissions(user_id, cursor):
    cursor.execute("SELECT user_id FROM users")
    rows = cursor.fetchall()
    for row in rows:
        if user_id in row:
            return True
    return False
