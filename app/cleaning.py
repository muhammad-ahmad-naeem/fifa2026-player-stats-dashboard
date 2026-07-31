import pandas as pd


def load_clean_data():
    """Loads the player-level cleaned data."""
    df = pd.read_csv("data/processed/players_clean.csv")
    return df


def load_team_summary():
    """
    Builds team-level aggregates from players_clean.csv.
    market_value_million_eur doesn't exist in the real data, so it's dropped.
    """
    players_df = load_clean_data()

    team_summary_df = (
        players_df.groupby("team")
        .agg(
            total_goals=("goals", "sum"),
            total_assists=("assists", "sum"),
            total_shots_on_target=("shots_on_target", "sum"),
            total_tackles=("tackles", "sum"),
            total_clean_sheets=("clean_sheets", "sum"),
            avg_pass_accuracy_pct=("pass_accuracy_pct", "mean"),
            total_yellow_cards=("yellow_cards", "sum"),
            total_red_cards=("red_cards", "sum"),
        )
        .reset_index()
    )

    return team_summary_df