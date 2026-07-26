import streamlit as st
from cleaning import load_clean_data

st.set_page_config(page_title="FIFA 2026 Dashboard", layout="wide")
st.title("⚽ FIFA 2026 Player Stats Dashboard")

df = load_clean_data()

team_names = df["team"].dropna().unique().tolist()
selected_team = st.selectbox(
    "Search for a team ", options=team_names, index=None, placeholder="Team name...."
)

if selected_team:
  filter_df = df[df["team"] == selected_team]
  total_goals = int(filter_df["goals"].sum())
  yellow_cards = int(filter_df["yellow_cards"].sum())
  red_cards = int(filter_df["red_cards"].sum())
  
  col1, col2, col3 = st.columns(3)
  col1.metric("Total goals", total_goals)
  col2.metric("Yellow Cards", yellow_cards)
  col3.metric("Red Cards", red_cards)
  st.dataframe(filter_df)

  player_position = filter_df["position"].dropna().unique().tolist()
  selected_position = st.selectbox(
      "Search for Player position",
      options=player_position,
      index=None,
      placeholder="Position Name....",
  )

  if selected_position:
    player_name_position = filter_df[filter_df["position"] == selected_position]
    player_position_goal=int(player_name_position["goals"].sum())
    player_position_red_cards=int(player_name_position["red_cards"].sum())
    player_position_yellow_cards=int(player_name_position["yellow_cards"].sum())

    col4,col5,col6=st.columns(3)
    col4.metric(f"Goals by {selected_position}",player_position_goal )
    col5.metric(f"Yellow Cards by {selected_position}",player_position_yellow_cards )
    col6.metric(f"Red Cards by {selected_position}",player_position_red_cards )
    
    st.dataframe(player_name_position)