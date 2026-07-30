import streamlit as st
from cleaning import load_clean_data
from metrics import per_90
from metrics import z_score
from metrics import impact_score
from metrics import score_player, POSITION_STATS

st.set_page_config(page_title="FIFA 2026 Dashboard", layout="wide")
st.title("⚽ FIFA 2026 Player Stats Dashboard")

df = load_clean_data()

# =========================================================
# SECTION 1: Team -> Position -> Player drill-down (Per-90)
# =========================================================

team_names = df["team"].dropna().unique().tolist()
selected_team = st.selectbox(
    "Search for a team ",
    options=team_names,
    index=None,
    placeholder="Team name...."
)

if selected_team:
    st.caption(
        "Totals below are summed across every player currently on this team's roster."
    )

    filter_df = df[df["team"] == selected_team]
    total_goals = int(filter_df["goals"].sum())
    yellow_cards = int(filter_df["yellow_cards"].sum())
    red_cards = int(filter_df["red_cards"].sum())

    col1, col2, col3 = st.columns(3)
    col1.metric("Total goals", total_goals)
    col2.metric("Yellow Cards", yellow_cards)
    col3.metric("Red Cards", red_cards)

    if st.button("Show team roster table", key="show_team_table"):
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
        player_position_goal = int(player_name_position["goals"].sum())
        player_position_red_cards = int(player_name_position["red_cards"].sum())
        player_position_yellow_cards = int(player_name_position["yellow_cards"].sum())

        col4, col5, col6 = st.columns(3)
        col4.metric(f"Goals by {selected_position}", player_position_goal)
        col5.metric(f"Yellow Cards by {selected_position}", player_position_yellow_cards)
        col6.metric(f"Red Cards by {selected_position}", player_position_red_cards)

        if st.button("Show players table", key="show_position_table"):
            st.dataframe(player_name_position)

        player_name_selection = player_name_position["player_name"].dropna().unique().tolist()
        player_name_selected = st.selectbox(
            "Slect a player ",
            options=player_name_selection,
            index=None,
            placeholder="position Name...."
        )
        if player_name_selected:
            st.caption(
                "**Goals per 90** scales a player's goals to a standard 90-minute match, "
                "so players with different amounts of playing time can be fairly compared. "
                "E.g. a player with fewer total goals but far less playing time may in fact "
                "be the more efficient scorer."
            )
            player_name = player_name_position[player_name_position["player_name"] == player_name_selected]
            player_time = player_name["minutes_played"].iloc[0]
            player_goals = player_name["goals"].iloc[0]
            goals = per_90(player_time, player_goals)
            if goals is None:
                st.metric("Goals/90 sec", "N/A")
            else:
                st.metric("Goals/90 sec", round(goals, 2))


# =========================================================
# SECTION 2: Z-score calculation (independent, own dropdowns)
# =========================================================

st.divider()
st.subheader("Z-Score Comparison")
st.caption(
    "A **z-score** shows how far above or below average a player's stat is, "
    "compared only to other players in the same position. A z-score of 0 means "
    "exactly average, positive means above average, negative means below average."
)

player_position_selection_z_score = df["position"].dropna().unique().tolist()
player_position_selected_z_score = st.selectbox(
    "Please Enter Position of Players for Z score",
    options=player_position_selection_z_score,
    index=None,
    placeholder="Enter Position....."
)
if player_position_selected_z_score:
    filter_df_z_score = df[df["position"] == player_position_selected_z_score]

    if st.button("Show players table", key="show_z_score_table"):
        st.dataframe(filter_df_z_score)

    player_names_list_z_score = filter_df_z_score["player_name"].dropna().unique().tolist()
    player_name_list_selected_z_score = st.selectbox(
        "Select a player name",
        options=player_names_list_z_score,
        index=None,
        placeholder="Enter Name....",
        key="z_score_player_select"
    )
    if player_name_list_selected_z_score:
        selected_player_row = filter_df_z_score[
            filter_df_z_score["player_name"] == player_name_list_selected_z_score
        ]
        player_saves_z_score = selected_player_row["saves"].iloc[0]
        player_goals_z_score = selected_player_row["goals"].iloc[0]

        z_score_final = z_score(player_saves_z_score, filter_df_z_score["saves"])
        if z_score_final is None:
            st.metric("Z score (saves)", "N/A")
        else:
            st.metric("Z score (saves)", round(z_score_final, 2))


# =========================================================
# SECTION 3: Impact Score calculation (independent, own dropdowns)
# =========================================================

st.divider()
st.subheader("Impact Score")
st.caption(
    "**Impact Score** combines a player's z-scores across a few stats relevant to "
    "their position (e.g. goals, assists, and shots for a forward) into a single "
    "overall number. It answers: 'overall, is this player above or below average "
    "for their position?' Missing stats are skipped rather than counted as average."
)

Player_position_impact_score = df["position"].dropna().unique().tolist()
player_position_selected_impact_score = st.selectbox(
    "Enter Player position for Calculating Impact Score",
    options=Player_position_impact_score,
    index=None,
    placeholder="Enter position for impact score....",
    key="impact_score_position_select"
)

if player_position_selected_impact_score:
    player_position_df_impact_score = df[df["position"] == player_position_selected_impact_score]

    if st.button("Show players table", key="show_impact_score_table"):
        st.dataframe(player_position_df_impact_score)

    player_names_list_impact_score = player_position_df_impact_score["player_name"].dropna().unique().tolist()
    player_name_selected_impact_score = st.selectbox(
        "Select a player name",
        options=player_names_list_impact_score,
        index=None,
        placeholder="Enter Name....",
        key="impact_score_player_select"
    )

    if player_name_selected_impact_score:
        selected_player_row_impact_score = player_position_df_impact_score[
            player_position_df_impact_score["player_name"] == player_name_selected_impact_score
        ].iloc[0]

        final_impact_score = score_player(
            selected_player_row_impact_score,
            player_position_df_impact_score
        )

        if final_impact_score is None:
            st.metric("Impact Score", "N/A")
        else:
            st.metric("Impact Score", round(final_impact_score, 2))