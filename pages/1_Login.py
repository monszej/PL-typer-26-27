import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

from auth import (
    create_users_table,
    add_user,
    verify_user
)

# Cookies
cookies = EncryptedCookieManager(
    prefix="pl_typer_",
    password="zmien_to_na_bardzo_dlugi_losowy_ciag"
)

if not cookies.ready():
    st.stop()

create_users_table()

# Administrator
add_user("admin", "admin123", 1)

# Automatyczne logowanie z cookie
if cookies.get("username"):

    st.session_state.logged_in = True
    st.session_state.username = cookies["username"]

    st.success(
        f"✅ Automatycznie zalogowano jako {cookies['username']}"
    )

    st.stop()

st.title("🔐 Logowanie")

username = st.text_input("Użytkownik")
password = st.text_input(
    "Hasło",
    type="password"
)

if st.button("Zaloguj"):

    if verify_user(
        username,
        password
    ):

        st.session_state.logged_in = True
        st.session_state.username = username

        cookies["username"] = username
        cookies.save()

        st.success(
            f"Witaj {username}"
        )

        st.rerun()

    else:

        st.error(
            "Błędny login lub hasło"
        )
        from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(
    prefix="pl_typer_",
    password="zmien_to_na_bardzo_dlugi_losowy_ciag"
)

if cookies.ready():

    st.divider()

    if st.button("🚪 Wyloguj"):

        if "username" in cookies:
            del cookies["username"]

        cookies.save()

        st.session_state.clear()

        st.success(
            "Zostałeś wylogowany."
        )

        st.rerun()
