import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

from auth import (
    verify_user,
    change_password
)

cookies = EncryptedCookieManager(
    prefix="pl_typer_",
    password="zmien_to_na_bardzo_dlugi_losowy_ciag"
)

if not cookies.ready():
    st.stop()

st.title("👤 Mój Profil")

if "username" not in st.session_state:
    st.warning("Najpierw się zaloguj.")
    st.stop()

username = st.session_state.username

st.write(
    f"Zalogowany użytkownik: **{username}**"
)

st.subheader("🔒 Zmiana hasła")

old_password = st.text_input(
    "Obecne hasło",
    type="password",
    key="old_password"
)

new_password = st.text_input(
    "Nowe hasło",
    type="password",
    key="new_password"
)

confirm_password = st.text_input(
    "Powtórz nowe hasło",
    type="password",
    key="confirm_password"
)

if st.button("Zmień hasło"):

    if not verify_user(
        username,
        old_password
    ):
        st.error(
            "Nieprawidłowe obecne hasło"
        )

    elif new_password.strip() != confirm_password.strip():
        st.error(
            "Hasła nie są identyczne"
        )

    elif not new_password.strip():
        st.error(
            "Hasło nie może być puste"
        )

    else:

        change_password(
            username,
            new_password.strip()
        )

        st.success(
            "✅ Hasło zostało zmienione"
        )

st.divider()

st.subheader("🚪 Wylogowanie")

if st.button("Wyloguj"):

    if cookies.get("username"):
        del cookies["username"]

    cookies.save()

    st.session_state.clear()

    st.rerun()
