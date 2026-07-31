"""
clean_data.py:
Maps raw scraped data (data/raw/players_raw.csv) onto the EXACT schema
defined in DATA_HANDOFF_SPEC.md.
players_clean.csv:
    player_id, player_name, team, position, appearances, minutes_played,
    goals, assists, shots_on_target, pass_accuracy_pct, tackles, saves,
    clean_sheets, yellow_cards, red_cards
team_summary.csv (one row per national team):
    team, total_players, total_goals, total_assists, total_shots_on_target,
    total_tackles, total_saves, total_clean_sheets, avg_pass_accuracy_pct,
    total_yellow_cards, total_red_cards
"""
import os
import pandas as pd
import numpy as np
RAW_PATH = "data/raw/players_raw.csv"
CLEAN_PLAYERS_PATH = "data/processed/players_clean.csv"
TEAM_SUMMARY_PATH = "data/processed/team_summary.csv"
VALID_POSITION_CODES = {"GK", "CB", "RB", "LB", "CDM", "CM", "CAM", "LW", "RW", "ST"}

TEAM_CODE_TO_NAME = {
    "CAN": "Canada", "MEX": "Mexico", "USA": "United States",
    "AUT": "Austria", "BEL": "Belgium", "BIH": "Bosnia and Herzegovina",
    "CRO": "Croatia", "CZE": "Czechia", "ENG": "England", "FRA": "France",
    "GER": "Germany", "NED": "Netherlands", "NOR": "Norway",
    "POR": "Portugal", "SCO": "Scotland", "ESP": "Spain",
    "SWE": "Sweden", "SUI": "Switzerland", "TUR": "Türkiye",
    "ALG": "Algeria", "EGY": "Egypt", "GHA": "Ghana", "MAR": "Morocco",
    "TUN": "Tunisia", "CPV": "Cape Verde", "COD": "DR Congo",
    "ARG": "Argentina", "BRA": "Brazil", "COL": "Colombia",
    "ECU": "Ecuador", "PAR": "Paraguay", "URU": "Uruguay",
    "AUS": "Australia", "IRN": "Iran", "JPN": "Japan", "JOR": "Jordan",
    "KOR": "South Korea", "UZB": "Uzbekistan", "QAT": "Qatar",
    "KSA": "Saudi Arabia", "IRQ": "Iraq",
    "NZL": "New Zealand",
    "CUW": "Curaçao", "HAI": "Haiti",
    "SEN": "Senegal", "CIV": "Côte d'Ivoire", "PAN": "Panama",
    "RSA": "South Africa",
}

UNAVAILABLE_COLUMNS = ["position", "tackles", "clean_sheets"]
FINAL_PLAYER_SCHEMA = [
    "player_id", "player_name", "team", "position", "appearances",
    "minutes_played", "goals", "assists", "shots_on_target",
    "pass_accuracy_pct", "tackles", "saves", "clean_sheets",
    "yellow_cards", "red_cards",
]
NUMERIC_COLUMNS = [
    "appearances", "minutes_played", "goals", "assists", "shots_on_target",
    "pass_accuracy_pct", "tackles", "saves", "clean_sheets",
    "yellow_cards", "red_cards",
]
def load_raw_data(path: str = RAW_PATH) -> pd.DataFrame:
    df = pd.read_csv(path, index_col=False)
    print(f"Loaded {len(df)} raw rows, {len(df.columns)} columns")
    return df
def consolidate_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    base_names = ["assists", "Assists", "team_code", "position_raw"]
    for base in base_names:
        matching_cols = [c for c in df.columns if c == base or c.startswith(base + "_")]
        if not matching_cols:
            continue
        final_col_name = base.lower()  # normalize "Assists" -> "assists"
        combined = df[matching_cols[0]]
        for col in matching_cols[1:]:
            combined = combined.combine_first(df[col])
        df = df.drop(columns=matching_cols)
        df[final_col_name] = combined
    return df
def rename_to_schema(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "Goals": "goals",
        "Minutes Played": "minutes_played",
        "Attempts On Target": "shots_on_target",
        "Passing Accuracy (%)": "pass_accuracy_pct",
        "Yellow Cards": "yellow_cards",
        "Red Cards": "red_cards",
        "Goalkeeper Saves": "saves",
        "position_raw": "position",
    }
    return df.rename(columns=rename_map)
def add_player_id(df: pd.DataFrame) -> pd.DataFrame:
    df["player_id"] = ["P" + str(i + 1).zfill(4) for i in range(len(df))]
    return df
def add_unavailable_columns(df: pd.DataFrame) -> pd.DataFrame:
    for col in UNAVAILABLE_COLUMNS:
        if col not in df.columns:
            df[col] = np.nan
    return df
def fix_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df
def map_team_names(df: pd.DataFrame) -> pd.DataFrame:
    if "team_code" not in df.columns:
        df["team"] = np.nan
        return df
    df["team"] = df["team_code"].map(TEAM_CODE_TO_NAME)
    unmapped_codes = set(df.loc[df["team"].isna() & df["team_code"].notna(), "team_code"])
    if unmapped_codes:
        print(f"\n[FLAG] These team codes have no entry in TEAM_CODE_TO_NAME "
              f"and were left blank - verify and add them: {unmapped_codes}")
    return df.drop(columns=["team_code"])
def validate_positions(df: pd.DataFrame):
    actual_values = set(df["position"].dropna().unique())
    invalid = actual_values - VALID_POSITION_CODES
    if invalid:
        print(f"\n[FLAG] position column contains values NOT in the "
              f"required 10-code scheme: {invalid}. Per spec, these must "
              f"be resolved with the app team, not guessed at.")

def reorder_to_final_schema(df: pd.DataFrame) -> pd.DataFrame:
    existing = [c for c in FINAL_PLAYER_SCHEMA if c in df.columns]
    return df[existing]
def clean_players(raw_path: str = RAW_PATH, output_path: str = CLEAN_PLAYERS_PATH) -> pd.DataFrame:
    df = load_raw_data(raw_path)
    df = consolidate_duplicate_columns(df)
    df = rename_to_schema(df)
    df = add_player_id(df)
    df = map_team_names(df)
    df = add_unavailable_columns(df)
    df = fix_dtypes(df)
    validate_positions(df)
    df = reorder_to_final_schema(df)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} cleaned players to {output_path}")
    missing_cols = [c for c in UNAVAILABLE_COLUMNS if df[c].isna().all()]
    if missing_cols:
        print(f"\n[NOTE] These required columns are entirely blank - see "
              f"module docstring for why each is blocked: {missing_cols}")
    return df
def build_team_summary(players_df: pd.DataFrame, output_path: str = TEAM_SUMMARY_PATH):
    if players_df["team"].isna().all():
        print("\n[SKIPPED] team_summary.csv NOT generated - 'team' is "
              "entirely missing from the current data source (scraper "
              "needs updating to capture it - see module docstring).")
        return None
    agg_spec = {
        "total_players": ("player_id", "count"),
        "total_goals": ("goals", "sum"),
        "total_assists": ("assists", "sum"),
        "total_shots_on_target": ("shots_on_target", "sum"),
        "total_tackles": ("tackles", "sum"),
        "total_saves": ("saves", "sum"),
        "total_clean_sheets": ("clean_sheets", "sum"),
        "avg_pass_accuracy_pct": ("pass_accuracy_pct", "mean"),
        "total_yellow_cards": ("yellow_cards", "sum"),
        "total_red_cards": ("red_cards", "sum"),
    }
    available_agg = {name: (col, fn) for name, (col, fn) in agg_spec.items()
                      if col in players_df.columns}
    missing_stats = [name for name in agg_spec if name not in available_agg]
    if missing_stats:
        print(f"[NOTE] Skipping these team_summary columns - source stat "
              f"missing from players data: {missing_stats}")
    summary = players_df.groupby("team").agg(**available_agg).reset_index()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    summary.to_csv(output_path, index=False)
    print(f"Saved {len(summary)} teams to {output_path}")
    return summary
if __name__ == "__main__":
    players_df = clean_players()
    build_team_summary(players_df)
