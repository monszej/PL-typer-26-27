import streamlit as st

st.title("🔐 Logowanie")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

users = {
    "Maciej": "haslo123",
    "Marcin": "haslo123",
    "Joanna": "haslo123",
    "Tomek": "haslo123"
}

username = st.text_input("Użytkownik")
password = st.text_input("Hasło", type="password")

if st.button("Zaloguj"):
    if username in users and users[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success(f"Witaj {username}")
    else:
        st.error("Nieprawidłowy login lub hasło")

if st.session_state.logged_in:
    st.success(f"Zalogowano jako: {st.session_state.username}")
