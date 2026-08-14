import streamlit as st
from auth import (
    add_user,
    get_all_users,
    delete_user,
    count_user_predictions,
    admin_reset_password
)

st.title("🛠️ Panel Administratora")

import sqlite3

conn = sqlite3.connect("typer.db")
cursor = conn.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
)

st.write("Tabele:", cursor.fetchall())

cursor.execute(
    "SELECT * FROM users"
)

st.write("Users:", cursor.fetchall())

try:
    cursor.execute(
        "SELECT * FROM predictions LIMIT 10"
    )

    st.write(
        "Predictions:",
        cursor.fetchall()
    )

except Exception as e:

    st.write("Predictions error:", e)

conn.close()

if "username" not in st.session_state:
    st.warning("Najpierw się zaloguj.")
    st.stop()

if st.session_state.username != "admin":
    st.error("Brak uprawnień.")
    st.stop()

st.subheader("Dodaj użytkownika")

new_user = st.text_input("Nowy użytkownik")
new_password = st.text_input("Hasło", type="password")

if st.button("Dodaj użytkownika"):

    add_user(
        new_user,
        new_password,
        0
    )

    st.success(f"Użytkownik {new_user} został dodany.")

from auth import get_all_users

from auth import delete_user

st.subheader("👥 Użytkownicy")

for user in get_all_users():

    username = user[0]

    total_predictions = count_user_predictions(
        username
    )

    col1, col2, col3 = st.columns([4, 2, 2])

    col1.write(
        f"👤 {username}"
    )

    col2.write(
        f"Typy: {total_predictions}"
    )

    if username != "admin":

        if col3.button(
            "🗑 Usuń",
            key=f"del_{username}"
        ):

            delete_user(username)

            st.success(
                f"Usunięto użytkownika: {username}"
            )

            st.rerun()

st.divider()

st.subheader("🔐 Reset hasła użytkownika")

users_list = [
    user[0]
    for user in get_all_users()
    if user[0] != "admin"
]

selected_user = st.selectbox(
    "Wybierz użytkownika",
    users_list
)

new_password = st.text_input(
    "Nowe hasło",
    type="password",
    key="reset_password"
)

if st.button("Resetuj hasło"):

    if len(new_password) < 6:

        st.error(
            "Hasło musi mieć minimum 6 znaków"
        )

    else:

        admin_reset_password(
            selected_user,
            new_password
        )

        st.success(
            f"✅ Hasło użytkownika {selected_user} zostało zmienione"
        )
