import plotly.express as px


def ranking_bar_chart(ranked_df, name_col, value_col, value_label, top_n=10):
    """
    Build a horizontal bar chart for a leaderboard.

    ranked_df   : dataframe already sorted descending by value_col
    name_col    : column with display names (e.g. "player_name")
    value_col   : column with the numeric ranking value (e.g. "goals_per_90")
    value_label : human-readable label for the value axis (e.g. "Goals per 90")
    top_n       : how many rows to display (slicing happens here)

    Returns a Plotly figure. No Streamlit code — page calls st.plotly_chart() on the result.
    """
    display_df = ranked_df.head(top_n)

    fig = px.bar(
        display_df,
        x=value_col,
        y=name_col,
        orientation="h",
        labels={value_col: value_label, name_col: "Player"},
    )

    # Highest value at the top, not the bottom
    fig.update_layout(yaxis={"categoryorder": "total ascending"})

    return fig