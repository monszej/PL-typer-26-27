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

if not matches:
    st.warning("Brak meczów do wyświetlenia.")
    st.stop()

# Lista kolejek
matchdays = sorted(
    list(
        set(
            match.get("matchday")
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

# Filtrowanie po kolejce
matches = [
    match
    for match in matches
    if str(match.get("matchday")) == str(selected_matchday)
]

st.subheader(f"🏆 Kolejka {selected_matchday}")

if len(matches) == 0:
    st.warning("Brak meczów w tej kolejce.")

for match in matches:

    match_id = match["id"]

    home = match["homeTeam"]["shortName"]
    away = match["awayTeam"]["shortName"]

    home_logo = match["homeTeam"].get("crest")
    away_logo = match["awayTeam"].get("crest")

    kickoff = datetime.fromisoformat(
        match["utcDate"].replace("Z", "+00:00")
    )

    now = datetime.now(timezone.utc)

    existing_prediction = get_prediction(
        username,
        match_id
    )

    if existing_prediction:
        default_home = existing_prediction[0]
        default_away = existing_prediction[1]
    else:
        default_home = 0
        default_away = 0

    st.divider()

    col_logo1, col_title, col_logo2 = st.columns(
        [1, 2, 1]
    )

    with col_logo1:
        if home_logo:
            st.image(home_logo, width=70)

    with col_title:
        st.subheader(
            f"{home} vs {away}"
        )

    with col_logo2:
        if away_logo:
            st.image(away_logo, width=70)

    st.caption(
        f"🕒 Start meczu: "
        f"{kickoff.strftime('%d-%m-%Y %H:%M UTC')}"
    )

    if now > kickoff:

        st.error(
            "⛔ Typowanie zamknięte"
        )

        if existing_prediction:
            st.info(
                f"Twój typ: "
                f"{default_home}:{default_away}"
            )

        continue

    col1, col2 = st.columns(2)

    home_pred = col1.number_input(
        home,
        min_value=0,
        max_value=20,
        value=default_home,
        key=f"home_{match_id}"
    )

    away_pred = col2.number_input(
        away,
        min_value=0,
        max_value=20,
        value=default_away,
        key=f"away_{match_id}"
    )

    if st.button(
        f"💾 Zapisz typ dla {home} vs {away}",
        key=f"save_{match_id}"
    ):

        conn.execute(
            """
            INSERT OR REPLACE INTO predictions
            VALUES (?, ?, ?, ?)
            """,
            (
                username,
                match_id,
                home_pred,
                away_pred
            )
        )

        conn.commit()

        st.success(
            f"✅ Zapisano typ: "
            f"{home} {home_pred}:{away_pred} {away}"
        )
