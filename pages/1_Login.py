import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

from auth import (
    create_users_table,
    verify_user,
    ensure_admin_exists
)

# Cookies
cookies = EncryptedCookieManager(
    prefix="pl_typer_",
    password="zmien_to_na_bardzo_dlugi_losowy_ciag"
)

if not cookies.ready():
    st.stop()

create_users_table()
from auth import add_user

if st.button("Utwórz administratora"):

    add_user(
        "admin",
        "admin123",
        1
    )

    st.success(
        "Administrator został utworzony"
    )
# ensure_admin_exists()

# Administrator


st.title("🔐 Logowanie")

from auth import get_all_users

st.write("Users:", get_all_users())

# Automatyczne logowanie z cookie
if cookies.get("username"):

    st.session_state.logged_in = True
    st.session_state.username = cookies["username"]

    st.success(
        f"✅ Aktualnie zalogowany: {cookies['username']}"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("🚪 Wyloguj"):

            del cookies["username"]

            cookies.save()

            st.session_state.clear()

            st.rerun()

    with col2:

        if st.button("👤 Zaloguj na inne konto"):

            del cookies["username"]

            cookies.save()

            st.session_state.clear()

            st.rerun()

    st.divider()

st.subheader("Logowanie")

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
