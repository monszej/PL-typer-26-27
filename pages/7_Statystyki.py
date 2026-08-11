import streamlit as st
import pandas as pd

from database import get_conn
from football_data import get_matches
from scoring import points

st.title("📊 Statystyki")

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

finished_matches = get_matches("FINISHED")

total_points = 0
exact_scores = 0
correct_winners = 0

for _, prediction in predictions.iterrows():

    match = next(
        (
            m
            for m in finished_matches
            if m["id"] == prediction["match_id"]
        ),
        None
    )

    if not match:
        continue

    real_home = match["score"]["fullTime"]["home"]
    real_away = match["score"]["fullTime"]["away"]

    earned = points(
        prediction["home_pred"],
        prediction["away_pred"],
        real_home,
        real_away
    )

    total_points += earned

    if earned == 3:
        exact_scores += 1

    elif earned == 1:
        correct_winners += 1

total_predictions = len(predictions)

if total_predictions > 0:
    accuracy = round(
        ((exact_scores + correct_winners) / total_predictions) * 100,
        1
    )
else:
    accuracy = 0

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🏆 Punkty",
        total_points
    )

    st.metric(
        "🎯 Idealne wyniki",
        exact_scores
    )

with col2:
    st.metric(
        "✅ Trafieni zwycięzcy",
        correct_winners
    )

    st.metric(
        "📈 Skuteczność",
        f"{accuracy}%"
    )

st.divider()

st.subheader("Podsumowanie")

st.write(f"Gracz: **{username}**")
st.write(f"Liczba zapisanych typów: **{total_predictions}**")
st.write(f"Łączna liczba punktów: **{total_points}**")
