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

        st.rerun()

st
