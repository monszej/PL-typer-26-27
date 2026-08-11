import streamlit as st
from auth import create_users_table, add_user, verify_user

create_users_table()

# pierwszy administrator
add_user("admin", "admin123", 1)

st.title("🔐 Logowanie")

username = st.text_input("Użytkownik")
password = st.text_input("Hasło", type="password")

if st.button("Zaloguj"):

    if verify_user(username, password):

        st.session_state.logged_in = True
        st.session_state.username = username

        st.success(f"Witaj {username}")

    else:

        st.error("Błędny login lub hasło")
