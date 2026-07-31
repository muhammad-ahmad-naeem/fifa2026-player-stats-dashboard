"""
make_graphs.py
Builds a set of Matplotlib charts from the cleaned FIFA 2026 data, saving each as a PNG in charts/. 
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
PLAYERS_PATH = "data/processed/players_clean.csv"
TEAM_SUMMARY_PATH = "data/processed/team_summary.csv"
CHARTS_DIR = "charts"
def load_data():
    players_df = pd.read_csv(PLAYERS_PATH)
    team_df = pd.read_csv(TEAM_SUMMARY_PATH)
    return players_df, team_df
def chart_top_scorers(players_df: pd.DataFrame, top_n: int = 10):
    top_scorers = (
        players_df.dropna(subset=["goals"])
        .sort_values("goals", ascending=False)
        .head(top_n)
    )
    plt.figure(figsize=(10, 6))
    plt.barh(top_scorers["player_name"], top_scorers["goals"], color="#1f77b4")
    plt.xlabel("Goals")
    plt.title(f"Top {top_n} Goal Scorers")
    plt.gca().invert_yaxis()  # highest scorer at the top, not the bottom
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/top_scorers.png", dpi=150)
    plt.close()
    print(f"Saved {CHARTS_DIR}/top_scorers.png")
def chart_goals_vs_assists(players_df: pd.DataFrame):
    plot_df = players_df.dropna(subset=["goals", "assists"])
    plt.figure(figsize=(8, 6))
    plt.scatter(plot_df["goals"], plot_df["assists"], alpha=0.6, color="#2ca02c")
    plt.xlabel("Goals")
    plt.ylabel("Assists")
    plt.title("Goals vs Assists (players with both stats recorded)")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/goals_vs_assists.png", dpi=150)
    plt.close()
    print(f"Saved {CHARTS_DIR}/goals_vs_assists.png")
def chart_players_by_position(players_df: pd.DataFrame):
    position_counts = players_df["position"].dropna().value_counts()
    plt.figure(figsize=(8, 6))
    plt.bar(position_counts.index, position_counts.values, color="#ff7f0e")
    plt.xlabel("Position")
    plt.ylabel("Number of Players")
    plt.title("Players by Position")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/players_by_position.png", dpi=150)
    plt.close()
    print(f"Saved {CHARTS_DIR}/players_by_position.png")
def chart_cards_by_team(team_df: pd.DataFrame, top_n: int = 15):
    plot_df = team_df.sort_values(
        "total_yellow_cards", ascending=False
    ).head(top_n)

    plt.figure(figsize=(10, 6))
    plt.bar(plot_df["team"], plot_df["total_yellow_cards"],
            label="Yellow Cards", color="#f1c40f")
    plt.bar(plot_df["team"], plot_df["total_red_cards"],
            bottom=plot_df["total_yellow_cards"],
            label="Red Cards", color="#e74c3c")
    plt.xlabel("Team")
    plt.ylabel("Cards")
    plt.title(f"Discipline Record — Top {top_n} Teams by Yellow Cards")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/cards_by_team.png", dpi=150)
    plt.close()
    print(f"Saved {CHARTS_DIR}/cards_by_team.png")
def chart_minutes_distribution(players_df: pd.DataFrame):
    plot_df = players_df.dropna(subset=["minutes_played"])
    plt.figure(figsize=(8, 6))
    plt.hist(plot_df["minutes_played"], bins=20, color="#9b59b6", edgecolor="white")
    plt.xlabel("Minutes Played")
    plt.ylabel("Number of Players")
    plt.title("Distribution of Minutes Played")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/minutes_distribution.png", dpi=150)
    plt.close()
    print(f"Saved {CHARTS_DIR}/minutes_distribution.png")

def chart_team_goals(team_df: pd.DataFrame, top_n: int = 15):
    plot_df = team_df.sort_values("total_goals", ascending=False).head(top_n)
    plt.figure(figsize=(10, 6))
    plt.bar(plot_df["team"], plot_df["total_goals"], color="#16a085")
    plt.xlabel("Team")
    plt.ylabel("Total Goals")
    plt.title(f"Total Goals Scored — Top {top_n} Teams")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/team_goals.png", dpi=150)
    plt.close()
    print(f"Saved {CHARTS_DIR}/team_goals.png")
def main():
    os.makedirs(CHARTS_DIR, exist_ok=True)
    players_df, team_df = load_data()
    chart_top_scorers(players_df)
    chart_goals_vs_assists(players_df)
    chart_players_by_position(players_df)
    chart_cards_by_team(team_df)
    chart_minutes_distribution(players_df)
    chart_team_goals(team_df)
    print(f"\nAll charts saved to {CHARTS_DIR}/")
if __name__ == "__main__":
    main()
