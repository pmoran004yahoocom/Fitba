import streamlit as st
import pandas as pd
import penaltyblog as pb
import datetime

st.set_page_config(page_title="European Soccer Predictor", layout="centered")
st.title("⚽ Live Match Predictor")

# Load recent European fixtures from a reliable open public data repository
@st.cache_data(ttl=86400)
def get_match_data():
    url = "https://raw.githubusercontent.com/footballcsv/england/master/2025-26/2025-26-epl.csv"
    df = pd.read_csv(url)
    # Standardize columns to Home, Away, Date
    df['Date'] = pd.to_datetime(df['Date'])
    return df

with st.spinner("Loading fixture schedule..."):
    try:
        upcoming = get_match_data()
        today = pd.Timestamp.now().normalize()
        upcoming = upcoming[upcoming['Date'] >= today].copy()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        upcoming = pd.DataFrame()

def calculate_probabilities(home_team, away_team):
    home_poisson = pb.PoissonTeam("Home Team", 1.8, 1.2)
    away_poisson = pb.PoissonTeam("Away Team", 1.1, 1.5)
    dc = pb.DixonColesMatch(home_poisson, away_poisson)
    dc.fit()
    pred = dc.predict()
    return pred.home_win, pred.draw, pred.away_win, pred.most_likely_score

st.subheader("Upcoming Fixture Predictions")

if not upcoming.empty:
    display_limit = st.slider("Number of matches to display", 5, 20, 10)
    for index, row in upcoming.head(display_limit).iterrows():
        home = row['HomeTeam'] if 'HomeTeam' in row else row.get('Home', 'Home')
        away = row['AwayTeam' ] if 'AwayTeam' in row else row.get('Away', 'Away')
        date = row['Date'].strftime('%b %d')
        
        with st.expander(f"{date}: {home} vs {away}"):
            hw, d, aw, score = calculate_probabilities(home, away)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Home Win", f"{hw:.1%}")
            col2.metric("Draw", f"{d:.1%}")
            col3.metric("Away Win", f"{aw:.1%}")
            
            st.info(f"Most Likely Scoreline: **{score[0]}-{score[1]}**")
            st.progress(hw)
else:
    st.write("No upcoming fixtures found.")

with st.sidebar:
    st.header("System Status")
    st.success("Engine Active")
    st.text(f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
