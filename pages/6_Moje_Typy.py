import streamlit as st
import pandas as pd

from database import get_conn

st.title("📝 Moje Typy")

if "username" not in st.session_state:
    st.warning("Najpierw się zaloguj")
    st.stop()

conn = get_conn()

query = """
SELECT *
FROM predictions
WHERE username = ?
"""

df = pd.read_sql_query(
    query,
    conn,
    params=(st.session_state.username,)
)

st.dataframe(
    df,
    use_container_width=True
)
