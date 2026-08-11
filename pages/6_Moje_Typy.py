import streamlit as st
import pandas as pd

from database import get_conn
from football_data import get_matches

st.title("📝 Moje Typy")

if "username" not in st.session_state:
    st.warning("Najpierw się zaloguj")
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

matches = (
    get_matches("SCHEDULED")
    + get_matches("FINISHED")
)

if len(predictions) == 0:

    st.info("Nie zapisano jeszcze żadnych typów.")

else:

    for _, row in predictions.iterrows():

        match = next(
            (
                m
                for m in matches
                if m["id"] == row["match_id"]
            ),
            None
        )

        if match:

            home = match["homeTeam"]["shortName"]
            away = match["awayTeam"]["shortName"]

            st.markdown(
                f"""
### ⚽ {home} vs {away}

Typ: **{row['home_pred']} : {row['away_pred']}**
"""
            )

            st.divider()
