import streamlit as st
import pandas as pd

from database import get_conn
from football_data import get_matches
from scoring import points

st.title("🏆 Ranking")

conn = get_conn()

finished = get_matches("FINISHED")

preds = pd.read_sql_query(
    "SELECT * FROM predictions",
    conn
)

ranking = {}

for _, p in preds.iterrows():

    match = next(
        (
            m
            for m in finished
            if m["id"] == p["match_id"]
        ),
        None
    )

    if not match:
        continue

    rh = match["score"]["fullTime"]["home"]
    ra = match["score"]["fullTime"]["away"]

    ranking[p["username"]] = (
        ranking.get(p["username"], 0)
        + points(
            p["home_pred"],
            p["away_pred"],
            rh,
            ra
        )
    )

df = pd.DataFrame(
    sorted(
        ranking.items(),
        key=lambda x: x[1],
        reverse=True
    ),
    columns=["Gracz", "Punkty"]
)

st.dataframe(
    df,
    use_container_width=True
)
