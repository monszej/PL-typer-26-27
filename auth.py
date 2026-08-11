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
        VALUES (?, ?, ?)
        """,
        (username, hashed, is_admin)
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
        WHERE username=?
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


def get_all_users():

    conn = sqlite3.connect("typer.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM users"
    )

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
        WHERE username=?
        """,
        (username,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def change_password(username, new_password):

    conn = sqlite3.connect("typer.db")
    cursor = conn.cursor()

    hashed = hash_password(new_password)

    cursor.execute(
        """
        UPDATE users
        SET password=?
        WHERE username=?
        """,
        (hashed, username)
    )

    conn.commit()
    conn.close()
def ensure_admin_exists():

    conn = sqlite3.connect("typer.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username
        FROM users
        WHERE username = 'admin'
        """
    )

    admin = cursor.fetchone()

    if not admin:

        hashed = hash_password("admin123")

        cursor.execute(
            """
            INSERT INTO users
            VALUES (?, ?, ?)
            """,
            (
                "admin",
                hashed,
                1
            )
        )

        conn.commit()

    conn.close()
