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

st.subheader("Użytkownicy")

for user in get_all_users():

    st.write(user[0])
