import sqlite3
import bcrypt


def create_users_table():

    conn = sqlite3.connect("typer.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            is_admin INTEGER DEFAULT 0
        )
        """
    )

    # Migracja starej tabeli
    cursor.execute(
        "PRAGMA table_info(users)"
    )

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    if "is_admin" not in columns:

        cursor.execute(
            """
            ALTER TABLE users
            ADD COLUMN is_admin INTEGER DEFAULT 0
            """
        )

    conn.commit()
    conn.close()


def hash_password(password):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def add_user(username, password, is_admin=0):

    conn = sqlite3.connect("typer.db")
    cursor = conn.cursor()

    hashed = hash_password(password)

    cursor.execute(
        """
        INSERT OR REPLACE INTO users
        (username, password, is_admin)
        VALUES (?, ?, ?)
        """,
        (
            username,
            hashed,
            is_admin
        )
    )

    conn.commit()
    conn.close()


def verify_user(username, password):

    conn = sqlite3.connect("typer.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT password
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    if not result:
        return False

    return bcrypt.checkpw(
        password.encode(),
        result[0].encode()
    )


def get_all_
