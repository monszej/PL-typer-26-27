import streamlit as st
import pandas as pd

from database import get_conn
from football_data import get_matches
from scoring import points

st.title("🏆 Ranking")

conn = get_conn()

finished_matches = get_matches("FINISHED")

predictions = pd.read_sql_query(
    "SELECT * FROM predictions",
    conn
)

ranking = {}

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

    user = prediction["username"]

if user == "admin":
    continue

earned_points = points(
    prediction["home_pred"],
    prediction["away_pred"],
    real_home,
    real_away
)
    

    if user not in ranking:

        ranking[user] = {
            "points": 0,
            "exact": 0,
            "correct": 0
        }

    ranking[user]["points"] += earned_points

    if earned_points == 3:
        ranking[user]["exact"] += 1

    elif earned_points == 1:
        ranking[user]["correct"] += 1

ranking_df = pd.DataFrame(
    [
        {
            "Gracz": user,
            "Punkty": data["points"],
            "Idealne wyniki": data["exact"],
            "Poprawni zwycięzcy": data["correct"]
        }
        for user, data in ranking.items()
    ]
)

if len(ranking_df) == 0:

    st.info("Brak punktowanych meczów.")

else:

    ranking_df = ranking_df.sort_values(
        by="Punkty",
        ascending=False
    ).reset_index(drop=True)

    ranking_df.index = ranking_df.index + 1

    st.subheader("Tabela")

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

    st.subheader("🏅 Podium")

    if len(ranking_df) >= 1:
        st.success(
            f"🥇 {ranking_df.iloc[0]['Gracz']} - {ranking_df.iloc[0]['Punkty']} pkt"
        )

    if len(ranking_df) >= 2:
        st.info(
            f"🥈 {ranking_df.iloc[1]['Gracz']} - {ranking_df.iloc[1]['Punkty']} pkt"
        )

    if len(ranking_df) >= 3:
        st.warning(
            f"🥉 {ranking_df.iloc[2]['Gracz']} - {ranking_df.iloc[2]['Punkty']} pkt"
        )
