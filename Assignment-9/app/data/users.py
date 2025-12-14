from app.data.db import connect_database

#insert
def insert_user(username, password_hash, role="user"):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
    """, (username, password_hash, role))

    conn.commit()
    conn.close()

#getting all users
def get_all_users():
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, role FROM users")
    rows = cursor.fetchall()

    conn.close()
    return rows

#selecting one user by username
def get_user_by_username(username):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    conn.close()
    return row

# changing user role
def update_user_role(username, new_role):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET role = ?
        WHERE username = ?
    """, (new_role, username))

    conn.commit()
    conn.close()

#deleting user
def delete_user(username):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()

import bcrypt

def register_user(username, password, role="user"):
    existing = get_user_by_username(username)
    if existing:
        return False, "Username already exists"

    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

    insert_user(username, hashed, role)
    return True, "Account created successfully"


def login_user(username, password):
    user = get_user_by_username(username)
    if not user:
        return False, "User not found"

    stored_hash = user[2]
    password_bytes = password.encode("utf-8")

    if bcrypt.checkpw(password_bytes, stored_hash.encode("utf-8")):
        return True, user[3]
    else:
        return False, "Incorrect password"
