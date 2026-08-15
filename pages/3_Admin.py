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
