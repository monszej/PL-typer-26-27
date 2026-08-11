import streamlit as st
import pandas as pd

from database import get_conn

st.title("📝 Moje Typy")

if "username" not in st.session_state:
    st.warning("Najpierw się zaloguj")
    st.stop()

conn = get_conn()

df = pd.read_sql_query(
    """
    SELECT
        match_id,
        home_pred,
        away_pred
    FROM predictions
    WHERE username = ?
    ORDER BY match_id
    """,
    conn,
    params=(st.session_state.username,)
)

if len(df) == 0:
    st.info("Nie zapisano jeszcze żadnych typów.")
else:
    st.dataframe(
        df,
        use_container_width=True
    )
