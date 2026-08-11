import streamlit as st
from football_data import get_matches
from database import get_conn

st.title("⚽ Typowanie")

if "username" not in st.session_state:
    st.warning("Najpierw się zaloguj")
    st.stop()

st.write(f"Zalogowano jako: **{st.session_state.username}**")

conn = get_conn()

matches = get_matches("SCHEDULED")

if not matches:
    st.warning("Brak meczów do wyświetlenia")
    st.stop()

for match in matches[:20]:

    match_id = match["id"]

    home = match["homeTeam"]["shortName"]
    away = match["awayTeam"]["shortName"]

    from datetime import datetime, timezone

kickoff = datetime.fromisoformat(
    match["utcDate"].replace("Z", "+00:00")
)

now = datetime.now(timezone.utc)

st.subheader(f"{home} vs {away}")

st.caption(f"Start: {kickoff}")

    col1, col2 = st.columns(2)

    home_pred = col1.number_input(
        f"{home}",
        min_value=0,
        max_value=20,
        key=f"home_{match_id}"
    )

    away_pred = col2.number_input(
        f"{away}",
        min_value=0,
        max_value=20,
        key=f"away_{match_id}"
    )

   if now > kickoff:

    st.error("⛔ Typowanie zamknięte")

else:

    if st.button(f"Zapisz typ {match_id}"):

        conn.execute(
            """
            INSERT OR REPLACE INTO predictions
            VALUES (?, ?, ?, ?)
            """,
            (
                st.session_state.username,
                match_id,
                home_pred,
                away_pred
            )
        )

        conn.commit()

        st.success("✅ Typ zapisany")
