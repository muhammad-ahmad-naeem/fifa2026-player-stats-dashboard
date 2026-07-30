import streamlit as st
from cleaning import load_clean_data
from charts import ranking_bar_chart

st.set_page_config(page_title="FIFA 2026 Dashboard", layout="wide")
st.title("⚽ FIFA 2026 Player Stats Dashboard")

df = load_clean_data()

# =========================================================
# Filters — narrow the KPIs, chart, and table together
# =========================================================
st.caption("Filter by team and/or position to explore a subset of the data.")

filter_col1, filter_col2 = st.columns(2)

team_options = ["All Teams"] + sorted(df["team"].dropna().unique().tolist())
selected_team_filter = filter_col1.selectbox("Team", options=team_options)

position_options = ["All Positions"] + sorted(df["position"].dropna().unique().tolist())
selected_position_filter = filter_col2.selectbox("Position", options=position_options)

filtered_df = df.copy()
if selected_team_filter != "All Teams":
    filtered_df = filtered_df[filtered_df["team"] == selected_team_filter]
if selected_position_filter != "All Positions":
    filtered_df = filtered_df[filtered_df["position"] == selected_position_filter]

# =========================================================
# KPI row — reflects whatever is currently filtered
# =========================================================
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
kpi_col1.metric("Players", len(filtered_df))
kpi_col2.metric("Teams", filtered_df["team"].nunique())
kpi_col3.metric("Goals", int(filtered_df["goals"].sum()))

# =========================================================
# Summary chart — goals by team, within the current filter
# =========================================================
st.divider()
st.subheader("Goals by Team")

if filtered_df.empty:
    st.info("No players match the current filters.")
else:
    team_goals = (
        filtered_df.groupby("team")["goals"]
        .sum()
        .reset_index()
        .sort_values("goals", ascending=False)
    )
    fig = ranking_bar_chart(
        team_goals, name_col="team", value_col="goals",
        value_label="Total Goals", top_n=len(team_goals)
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# Player data table
# =========================================================
st.divider()
st.subheader("Player Data")
st.dataframe(filtered_df)