import sqlite3

def get_conn():
    conn=sqlite3.connect('typer.db',check_same_thread=False)
    conn.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY,password TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS predictions(username TEXT,match_id INTEGER,home_pred INTEGER,away_pred INTEGER,PRIMARY KEY(username,match_id))")
    return conn
