import streamlit as st
import pandas as pd
from cleaning import load_clean_data
from metrics import per_90, score_player
from charts import ranking_bar_chart

st.set_page_config(page_title="FIFA 2026 Dashboard", layout="wide")
st.title("📊 Advanced Stats & Rankings")

df = load_clean_data()

st.caption(
    "Set a minimum minutes-played threshold to exclude small-sample players "
    "from the rankings below."
)
min_minutes = int(df["minutes_played"].min())
max_minutes = int(df["minutes_played"].max())
minutes_threshold = st.slider(
    "Minimum minutes played",
    min_value=min_minutes,
    max_value=max_minutes,
    value=min_minutes,
)

qualifying_df = df[df["minutes_played"] >= minutes_threshold].copy()

# =========================================================
# SECTION 1: Top Scorers (Goals per 90)
# =========================================================
st.divider()
st.subheader("Top Scorers")
st.caption("Ranked by goals per 90 minutes played.")

scorers_df = qualifying_df.copy()
scorers_df["goals_per_90"] = scorers_df.apply(
    lambda row: per_90(row["minutes_played"], row["goals"]), axis=1
)
scorers_df = scorers_df.dropna(subset=["goals_per_90"]).sort_values(
    "goals_per_90", ascending=False
)

top_n_scorers = st.slider("Players to show", 5, 25, 10, key="top_n_scorers")

if scorers_df.empty:
    st.info("No players meet the current minutes threshold.")
else:
    fig_scorers = ranking_bar_chart(
        scorers_df, name_col="player_name", value_col="goals_per_90",
        value_label="Goals per 90", top_n=top_n_scorers
    )
    st.plotly_chart(fig_scorers, use_container_width=True)

# =========================================================
# SECTION 2: Top Playmakers (Assists per 90)
# =========================================================
st.divider()
st.subheader("Top Playmakers")
st.caption("Ranked by assists per 90 minutes played.")

playmakers_df = qualifying_df.copy()
playmakers_df["assists_per_90"] = playmakers_df.apply(
    lambda row: per_90(row["minutes_played"], row["assists"]), axis=1
)
playmakers_df = playmakers_df.dropna(subset=["assists_per_90"]).sort_values(
    "assists_per_90", ascending=False
)

top_n_playmakers = st.slider("Players to show", 5, 25, 10, key="top_n_playmakers")

if playmakers_df.empty:
    st.info("No players meet the current minutes threshold.")
else:
    fig_playmakers = ranking_bar_chart(
        playmakers_df, name_col="player_name", value_col="assists_per_90",
        value_label="Assists per 90", top_n=top_n_playmakers
    )
    st.plotly_chart(fig_playmakers, use_container_width=True)

# =========================================================
# SECTION 3: Best Overall Impact
# =========================================================
st.divider()
st.subheader("Best Overall Impact")
st.caption(
    "Ranked by Impact Score. Each player's z-scores are computed against the full "
    "pool of players at their position, so the underlying comparison stays "
    "statistically meaningful — the minutes filter above only controls who is "
    "eligible to appear in this list."
)

impact_rows = []
for position, position_group in df.groupby("position"):
    for _, player_row in position_group.iterrows():
        if player_row["minutes_played"] < minutes_threshold:
            continue
        score = score_player(player_row, position_group)
        impact_rows.append({
            "player_name": player_row["player_name"],
            "position": position,
            "impact_score": score,
        })

impact_df = pd.DataFrame(impact_rows).dropna(subset=["impact_score"])
impact_df = impact_df.sort_values("impact_score", ascending=False)

top_n_impact = st.slider("Players to show", 5, 25, 10, key="top_n_impact")

if impact_df.empty:
    st.info("No players meet the current minutes threshold.")
else:
    fig_impact = ranking_bar_chart(
        impact_df, name_col="player_name", value_col="impact_score",
        value_label="Impact Score", top_n=top_n_impact
    )
    st.plotly_chart(fig_impact, use_container_width=True)