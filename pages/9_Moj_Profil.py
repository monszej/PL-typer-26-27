import streamlit as st

from auth import (
    verify_user,
    change_password
)

st.title("👤 Mój Profil")

if "username" not in st.session_state:
    st.warning("Najpierw się zaloguj.")
    st.stop()

username = st.session_state.username

st.write(f"Zalogowany użytkownik: **{username}**")

old_password = st.text_input(
    "Obecne hasło",
    type="password"
)

new_password = st.text_input(
    "Nowe hasło",
    type="password"
)

confirm_password = st.text_input(
    "Powtórz nowe hasło",
    type="password"
)

if st.button("Zmień hasło"):

    if not verify_user(
        username,
        old_password
    ):
        st.error("Nieprawidłowe obecne hasło")

    elif new_password != confirm_password:
        st.error("Hasła nie są identyczne")

    elif len(new_password) < 6:
        st.error(
            "Hasło musi mieć minimum 6 znaków"
        )

    else:

        change_password(
            username,
            new_password
        )

        st.success(
            "✅ Hasło zostało zmienione"
        )
