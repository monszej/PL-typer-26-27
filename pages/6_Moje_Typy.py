import streamlit as st
import pandas as pd

from database import get_conn
from football_data import get_matches
from scoring import points

st.title("📝 Moje Typy")

if "username" not in st.session_state:
    st.warning("Najpierw się zaloguj.")
    st.stop()

username = st.session_state.username

conn = get_conn()

predictions = pd.read_sql_query(
    """
    SELECT *
    FROM predictions
    WHERE username = ?
    """,
    conn,
    params=(username,)
)

all_matches = (
    get_matches("SCHEDULED")
    + get_matches("FINISHED")
)

if len(predictions) == 0:

    st.info("Nie zapisano jeszcze żadnych typów.")
    st.stop()

for _, prediction in predictions.iterrows():

    match = next(
        (
            m
            for m in all_matches
            if m["id"] == prediction["match_id"]
        ),
        None
    )

    if not match:
        continue

    home = match["homeTeam"]["shortName"]
    away = match["awayTeam"]["shortName"]

    predicted_home = prediction["home_pred"]
    predicted_away = prediction["away_pred"]

    st.subheader(f"⚽ {home} vs {away}")

    st.write(
        f"Twój typ: **{predicted_home}:{predicted_away}**"
    )

    if match["status"] == "FINISHED":

        real_home = match["score"]["fullTime"]["home"]
        real_away = match["score"]["fullTime"]["away"]

        pts = points(
            predicted_home,
            predicted_away,
            real_home,
            real_away
        )

        st.write(
            f"Wynik końcowy: **{real_home}:{real_away}**"
        )

        if pts == 3:

            st.success(
                f"✅ Idealny wynik (+3 pkt)"
            )

        elif pts == 1:

            st.info(
                f"✅ Poprawny zwycięzca/remis (+1 pkt)"
            )

        else:

            st.error(
                "❌ Nietrafiony typ (0 pkt)"
            )

    else:

        st.warning(
            "⏳ Mecz jeszcze się nie zakończył"
        )

    st.divider()
