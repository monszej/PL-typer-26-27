import streamlit as st
from football_data import get_matches
from database import get_conn, get_prediction
from datetime import datetime, timezone

st.title("⚽ Typowanie")

if "username" not in st.session_state:
    st.warning("Najpierw się zaloguj.")
    st.stop()

username = st.session_state.username

if username == "admin":
    st.info(
        "Konto administratora nie bierze udziału w typowaniu."
    )
    st.stop()

st.success(f"Zalogowano jako: {username}")

conn = get_conn()

matches = get_matches("SCHEDULED")

st.write("Liczba meczów:", len(matches))

if not matches:
    st.warning("Brak meczów do wyświetlenia.")
    st.stop()

# Lista kolejek
matchdays = sorted(
    list(
        set(
            match["matchday"]
            for match in matches
            if match.get("matchday")
        )
    )
)

if not matchdays:
    st.warning("Nie znaleziono kolejek.")
    st.stop()

selected_matchday = st.selectbox(
    "🏆 Wybierz kolejkę",
    matchdays,
    index=0
)

matches = [
    match
    for match in matches
    if match.get("matchday") == selected_matchday
]

st.subheader(f"🏆 Kolejka {selected_matchday}")

for match in matches:

    match_id = match["id"]

    home = match["homeTeam"]["shortName"]
    away = match["awayTeam"]["shortName"]

    home_logo = match["homeTeam"].get
