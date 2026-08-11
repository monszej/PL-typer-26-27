import streamlit as st
import pandas as pd

from database import get_conn
from football_data import get_matches
from scoring import points

st.title("🏆 Ranking Kolejki")

conn = get_conn()

finished_matches = get_matches("FINISHED")

if len(finished_matches) == 0:
    st.info("Brak zakończonych meczów.")
    st.stop()

matchdays = sorted(
    list(
        set(
            [
                match["matchday"]
                for match in finished_matches
                if match.get("matchday")
            ]
        )
    )
)

selected_matchday = st.selectbox(
    "Wybierz kolejkę",
    matchdays,
    index=len(matchdays) - 1
)

predictions = pd.read_sql_query(
    "SELECT * FROM predictions",
    conn
)

ranking = {}

selected_matches = [
    m
    for m in finished_matches
    if m["matchday"] == selected_matchday
]

for _, prediction in predictions.iterrows():

    match = next(
        (
            m
            for m in selected_matches
            if m["id"] == prediction["match_id"]
        ),
        None
    )

    if not match:
        continue

    user = prediction["username"]

    if user == "admin":
        continue

    real_home = match["score"]["fullTime"]["home"]
    real_away = match["score"]["fullTime"]["away"]

    earned = points(
        prediction["home_pred"],
        prediction["away_pred"],
        real_home,
        real_away
    )

    ranking[user] = ranking.get(user, 0) + earned

if len(ranking) == 0:

    st.info(
        f"Brak punktów dla kolejki {selected_matchday}"
    )

else:

    ranking_df = pd.DataFrame(
        sorted(
            ranking.items(),
            key=lambda x: x[1],
            reverse=True
        ),
        columns=["Gracz", "Punkty"]
    )

    ranking_df.index += 1

    st.subheader(
        f"Kolejka {selected_matchday}"
    )

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

    st.subheader("🥇 TOP 3")

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
