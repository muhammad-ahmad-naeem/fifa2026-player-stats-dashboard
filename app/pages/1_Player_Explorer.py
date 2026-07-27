import streamlit as st
from cleaning import load_clean_data
from metrics import per_90
from metrics import z_score

st.set_page_config(page_title="FIFA 2026 Dashboard", layout="wide")
st.title("⚽ FIFA 2026 Player Stats Dashboard")

df = load_clean_data()

team_names = df["team"].dropna().unique().tolist()
selected_team = st.selectbox(
    "Search for a team ",
    options=team_names,
    index=None,
    placeholder="Team name...."
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

    player_name_selection=player_name_position["player_name"].dropna().unique().tolist()
    player_name_selected=st.selectbox(
      "Slect a player ",
      options=player_name_selection,
      index=None,
      placeholder="position Name...."
    )
    if player_name_selected:
        player_name=player_name_position[player_name_position["player_name"]== player_name_selected]
        player_time=int(player_name["minutes_played"].iloc[0])
        player_goals=int(player_name["goals"].iloc[0])
        goals=per_90(player_time,player_goals)
        if goals is None:
           st.metric("Goals/90 sec", "N/A")
        else:
            st.metric("Goals/90 sec",round(goals,2))
         # Z score calculation below
        
            player_position_selection_z_score=df["position"].dropna().unique().tolist()
            player_position_selected_z_score=st.selectbox(
                "Please Enter Position of Players for Z score",
                options=player_position_selection_z_score,
                index=None,
                placeholder="Enter Position....."
            )
            if player_position_selected_z_score:
                filter_df_z_score = df[df["position"] == player_position_selected_z_score]
                st.dataframe(filter_df_z_score)
                player_names_list_z_score=filter_df_z_score["player_name"].dropna().unique().tolist()
                player_name_list_selected_z_score=st.selectbox(
                    "Select a player name",
                     options=player_names_list_z_score,
                    index=None,
                    placeholder="Enter Name...."
                )
                if player_name_list_selected_z_score:
                    selected_player_row = filter_df_z_score[filter_df_z_score["player_name"] == player_name_list_selected_z_score]
                    player_saves_z_score = int(selected_player_row["saves"].iloc[0])
                    player_goals_z_score = int(selected_player_row["goals"].iloc[0])
        
                    z_score_final = z_score(player_saves_z_score, filter_df_z_score["saves"])
                    if z_score_final is None:
                        st.metric("Z score (saves)", "N/A")
                    else:
                        st.metric("Z score (saves)", round(z_score_final, 2))


 