import streamlit as st
import pandas as pd

from database import get_conn
from football_data import get_matches

st.set_page_config(
    page_title="Premier League Typer",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Premier League Typer 2026/27")

conn = get_conn()

# Dane
users = pd.read_sql_query(
    "SELECT username FROM users",
    conn
)

predictions = pd.read_sql_query(
    "SELECT * FROM predictions",
    conn
)

scheduled_matches = get_matches("SCHEDULED")
finished_matches = get_matches("FINISHED")

# Statystyki główne
players_count = len(
    users[users["username"] != "admin"]
)

tips_count = len(predictions)

finished_count = len(finished_matches)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "👥 Gracze",
        players_count
    )

with col2:
    st.metric(
        "📝 Zapisane typy",
        tips_count
    )

with col3:
    st.metric(
        "✅ Zakończone mecze",
        finished_count
    )

st.divider()

# Najbliższa kolejka
if scheduled_matches:

    next_matchday = min(
        match["matchday"]
        for match in scheduled_matches
        if match.get("matchday")
    )

    st.subheader(
        f"🏆 Najbliższa kolejka: {next_matchday}"
    )

    upcoming = [
        match
        for match in scheduled_matches
        if match["matchday"] == next_matchday
    ]

    for match in upcoming:

        home = match["homeTeam"]["shortName"]
        away = match["awayTeam"]["shortName"]

        st.write(
            f"⚽ {home} vs {away}"
        )

else:

    st.info(
        "Brak nadchodzących meczów."
    )

st.divider()

st.subheader("📋 Jak korzystać z aplikacji")

st.markdown("""
### ⚽ Typowanie
Wybierz kolejkę i wpisz swoje typy.

### 🏆 Ranking
Sprawdź klasyfikację całego sezonu.

### 🥇 Ranking Kolejki
Zobacz kto najlepiej typował w konkretnej kolejce.

### 📝 Moje Typy
Przegląd wszystkich zapisanych typów.

### 📊 Statystyki
Liczba punktów, trafionych wyników i skuteczność.

### 👤 Mój Profil
Zmiana hasła.
""")

st.divider()

st.caption(
    "Premier League Typer | wersja 1.0"
)
