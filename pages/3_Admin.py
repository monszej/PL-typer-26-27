import streamlit as st

from auth import (
    add_user,
    get_all_users,
    delete_user,
    count_user_predictions,
    admin_reset_password
)

from database import get_conn

st.title("🛠️ Panel Administratora")

if "username" not in st.session_state:
    st.warning("Najpierw się zaloguj.")
    st.stop()

if st.session_state.username != "admin":
    st.error("Brak uprawnień.")
    st.stop()

# Naprawa bazy
if st.button("🔧 Napraw bazę"):

    conn = get_conn()
    conn.commit()
    conn.close()

    st.success(
        "Tabele zostały utworzone lub sprawdzone."
    )

st.divider()

st.subheader("➕ Dodaj użytkownika")

new_user = st.text_input(
    "Nowy użytkownik"
)

new_password = st.text_input(
    "Hasło",
    type="password"
)

if st.button("Dodaj użytkownika"):

    if len(new_password) < 6:

        st.error(
            "Hasło musi mieć minimum 6 znaków"
        )

    else:

        add_user(
            new_user,
            new_password,
            0
        )

        st.success(
            f"✅ Użytkownik {new_user} został dodany."
        )

st.divider()

st.subheader("👥 Użytkownicy")

users = get_all_users()

for user in users:

    username = user[0]

    try:
        total_predictions = count_user_predictions(
            username
        )
    except Exception:
        total_predictions = 0

    col1, col2, col3 = st.columns(
        [4, 2, 2]
    )

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

users
