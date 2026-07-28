import streamlit as st
import pandas as pd
from cleaning import load_team_summary, load_clean_data
from metrics import per_90, z_score, impact_score, compare_teams, CORE_COMPARISON_STATS


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(page_title="FIFA 2026 Dashboard", layout="wide")
st.title("⚽ FIFA 2026 Team Comparison Dashboard")


# ============================================================
# DATA LOADING
# ============================================================
team_summary_df = load_team_summary()   # team-level aggregated stats
players_df = load_clean_data()          # player-level raw stats

team_list = team_summary_df["team"].unique()


# ============================================================
# TEAM SELECTION
# ============================================================
st.subheader("Select Teams to Compare")

col1, col2 = st.columns(2)
with col1:
    team_a = st.selectbox("Select Team A", team_list)
with col2:
    team_b = st.selectbox("Select Team B", team_list)


# ============================================================
# COMPARISON (only runs if two different teams are selected)
# ============================================================
if team_a == team_b:
    st.warning("Please select two different teams to compare.")

else:
    team_a_data = team_summary_df[team_summary_df["team"] == team_a].iloc[0]
    team_b_data = team_summary_df[team_summary_df["team"] == team_b].iloc[0]

    # ------------------------------------------------------
    # Head-to-Head Summary Table
    # ------------------------------------------------------
    st.divider()
    st.subheader(f"📊 {team_a} vs {team_b} — Head-to-Head Summary")

    display_stats = CORE_COMPARISON_STATS + [
        "avg_market_value_m", "total_yellow_cards", "total_red_cards"
    ]

    comparison_table = pd.DataFrame({
        "Stat": display_stats,
        team_a: [f"{team_a_data[stat]:.2f}" for stat in display_stats],
        team_b: [f"{team_b_data[stat]:.2f}" for stat in display_stats],
    })

    st.table(comparison_table.set_index("Stat"))

    # ------------------------------------------------------
    # Winner Result
    # ------------------------------------------------------
    st.divider()
    st.subheader("🏆 Result")

    result = compare_teams(team_a_data, team_b_data)

    if result["winner"] == "team_a":
        st.success(f"**{team_a}** wins the head-to-head!")
    elif result["winner"] == "team_b":
        st.success(f"**{team_b}** wins the head-to-head!")
    else:
        st.info("It's a draw — even after the discipline tiebreaker.")

    if result.get("tiebreaker_used"):
        st.caption("Decided by fewer total cards (yellow + red).")

    # ------------------------------------------------------
    # Advanced Stats (hidden by default)
    # ------------------------------------------------------
    with st.expander("📈 Show Advanced Stats"):
        for stat, info in result["stat_breakdown"].items():
            if info["winner"] == "team_a":
                winner_label = team_a
            elif info["winner"] == "team_b":
                winner_label = team_b
            else:
                winner_label = "Tie"

            st.write(f"**{stat}**: {winner_label} ({info['team_a_value']} vs {info['team_b_value']})")

        if result["tiebreaker_used"]:
            st.write("*Tiebreaker was used to decide the winner (fewer total cards).*")

    # ------------------------------------------------------
    # Full Player Data (hidden by default)
    # ------------------------------------------------------
    with st.expander("📋 Show Full Player Data"):
        player_col_a, player_col_b = st.columns(2)

        with player_col_a:
            st.write(f"**{team_a} Players**")
            st.dataframe(team_a_players := players_df[players_df["team"] == team_a])

        with player_col_b:
            st.write(f"**{team_b} Players**")
            st.dataframe(team_b_players := players_df[players_df["team"] == team_b])