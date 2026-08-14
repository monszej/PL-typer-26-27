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

    if not new_user.strip():

        st.error(
            "Podaj nazwę użytkownika"
        )

    elif not new_password.strip():

        st.error(
            "Hasło nie może być puste"
        )

    else:

        add_user(
            new_user.strip(),
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

users_list = [
    user[0]
    for user in users
    if user[0] != "admin"
]

if users_list:

    selected_user = st.selectbox(
        "Wybierz użytkownika",
        users_list
    )

    reset_password = st.text_input(
        "Nowe hasło",
        type="password",
        key="reset_password"
    )

    if st.button("Resetuj hasło"):

        if not reset_password.strip():

            st.error(
                "Hasło nie może być puste"
            )

        else:

            admin_reset_password(
                selected_user,
                reset_password
            )

            st.success(
                f"✅ Hasło użytkownika {selected_user} zostało zmienione."
            )

else:

    st.info(
        "Brak użytkowników do resetu hasła."
    )
