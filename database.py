import sqlite3


def get_conn():
    conn = sqlite3.connect(
        "typer.db",
        check_same_thread=False
    )

   conn.execute(
    """
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT,
        is_admin INTEGER DEFAULT 0
    )
    """
)

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS predictions(
            username TEXT,
            match_id INTEGER,
            home_pred INTEGER,
            away_pred INTEGER,
            PRIMARY KEY(username, match_id)
        )
        """
    )

    return conn


def get_prediction(username, match_id):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT home_pred, away_pred
        FROM predictions
        WHERE username = ?
        AND match_id = ?
        """,
        (username, match_id)
    )

    result = cursor.fetchone()

    conn.close()

    return result
