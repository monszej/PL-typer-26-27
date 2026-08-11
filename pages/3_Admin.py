import streamlit as st
from auth import add_user

st.title("🛠️ Panel Administratora")

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

st.subheader("Użytkownicy")

for user in get_all_users():

    username = user[0]

    col1, col2 = st.columns([4, 1])

    col1.write(username)

    if username != "admin":

        if col2.button(
            "🗑 Usuń",
            key=f"del_{username}"
        ):

            delete_user(username)

            st.success(
                f"Usunięto użytkownika: {username}"
            )

            st.rerun()
