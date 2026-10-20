import streamlit as st
import pandas as pd
import penaltyblog as pb
import datetime

st.set_page_config(page_title="European Soccer Predictor", layout="centered")
st.title("⚽ Live Match Predictor")

# Built-in sample upcoming fixtures for demonstration
@st.cache_data
def get_match_data():
    data = {
        'Date': ['2026-10-24', '2026-10-25', '2026-10-25', '2026-10-26', '2026-10-26'],
        'Home': ['Arsenal', 'Manchester United', 'Real Madrid', 'Inter Milan', 'Bayern Munich'],
        'Away': ['Chelsea', 'Liverpool', 'Barcelona', 'AC Milan', 'Borussia Dortmund']
    }
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

with st.spinner("Loading fixture schedule..."):
    upcoming = get_match_data()

def calculate_probabilities(home_team, away_team):
    home_poisson = pb.PoissonTeam(home_team, 1.8, 1.2)
    away_poisson = pb.PoissonTeam(away_team, 1.1, 1.5)
    dc = pb.DixonColesMatch(home_poisson, away_poisson)
    dc.fit()
    pred = dc.predict()
    return pred.home_win, pred.draw, pred.away_win, pred.most_likely_score

st.subheader("Upcoming Match Predictions")

if not upcoming.empty:
    for index, row in upcoming.iterrows():
        home = row['Home']
        away = row['Away']
        date = row['Date'].strftime('%b %d, %Y')
        
        with st.expander(f"{date}: {home} vs {away}"):
            hw, d, aw, score = calculate_probabilities(home, away)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Home Win", f"{hw:.1%}")
            col2.metric("Draw", f"{d:.1%}")
            col3.metric("Away Win", f"{aw:.1%}")
            
            st.info(f"Most Likely Scoreline: **{score[0]}-{score[1]}**")
            st.progress(hw)
else:
    st.write("No matches found.")

with st.sidebar:
    st.header("System Status")
    st.success("Engine Active")
    st.text(f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
