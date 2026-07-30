"""
config.py:
 no logic. Keeping these separate from the scraping code
means changing the target URL or which tabs to scrape doesn't require
touching any actual scraping logic in utils.py / scrape_players.py.
"""
PAGE_URL = "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/statistics/player-statistics"
TABS = [
    "adidas Golden Boot",
    "Attacking",
    "Distribution",
    "Defending",
    "Discipline",
    "Goalkeeping",
    "Movement",
    "Physical",
]
# Output paths
RAW_OUTPUT_DIR = "data/raw"
RAW_OUTPUT_FILE = "data/raw/players_raw.csv"
