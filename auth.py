import sqlite3

def create_users_table():
    conn = sqlite3.connect("typer.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        is_admin INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def add_user(username, password, is_admin=0):
    conn = sqlite3.connect("typer.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR REPLACE INTO users VALUES (?, ?, ?)",
        (username, password, is_admin)
    )

    conn.commit()
    conn.close()


def verify_user(username, password):
    conn = sqlite3.connect("typer.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    return user is not None

def get_all_users():

    conn = sqlite3.connect("typer.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users")

    users = cursor.fetchall()

    conn.close()

    return users

def delete_user(username):

    conn = sqlite3.connect("typer.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE username=?",
        (username,)
    )

    conn.commit()
    conn.close()

def count_user_predictions(username):

    conn = sqlite3.connect("typer.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM predictions
        WHERE username = ?
        """,
        (username,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count
