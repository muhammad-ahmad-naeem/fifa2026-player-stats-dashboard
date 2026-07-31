<div align="center">

# ⚽ FIFA 2026 Player Stats Dashboard

**An interactive Streamlit dashboard for exploring FIFA 2026 player and team statistics.**

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Charts-Plotly-3F4F75?logo=plotly&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

</div>

---

## Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Data Source](#data-source)
- [Methodology](#methodology)
- [Project Status](#project-status)
- [Contributors](#contributors)

---

## Features

| Page | What it does |
|---|---|
| 🏠 **Home** | Live-filterable overview (team/position), KPI summary, goals-by-team chart |
| 🔎 **Player Explorer** | Team → Position → Player drill-down, per-90 stats, z-score comparisons, composite Impact Score |
| ⚔️ **Team Comparison** | Head-to-head team stats with a fair-play tiebreaker and expandable advanced/raw-data views |
| 📊 **Advanced Stats** | Top Scorers, Top Playmakers, and Best Overall Impact leaderboards with adjustable filters |

## Tech Stack

| Component | Tool |
|---|---|
| Frontend / App Framework | Streamlit |
| Data Handling | pandas |
| Statistical Calculations | NumPy |
| Charting | Plotly |
| Language | Python 3.14 |
| Version Control | Git / GitHub |

---

## Project Structure

<details>
<summary>Click to expand</summary>

```
fifa2026-player-stats-dashboard/
│
├── data/
│   ├── raw/              # raw scraped data
│   └── processed/        # cleaned datasets used by the app
│
├── scraper/               # scripts that pull player data from the source site
├── notebooks/              # EDA and cleaning prototyping
│
├── app/
│   ├── Home.py
│   ├── cleaning.py         # data loading
│   ├── metrics.py          # per_90, z_score, impact_score, compare_teams, etc.
│   ├── charts.py           # reusable Plotly chart functions
│   └── pages/
│       ├── 1_Player_Explorer.py
│       ├── 2_Team_Comparison.py
│       └── 3_Advanced_Stats.py
│
├── assets/                 # branding and CSS
├── requirements.txt
└── README.md
```

</details>

---

## Setup

<details>
<summary><b>1. Clone and create a virtual environment</b></summary>

```bash
git clone https://github.com/muhammad-ahmad-naeem/fifa2026-player-stats-dashboard.git
cd fifa2026-player-stats-dashboard
python -m venv .venv
```

</details>

<details>
<summary><b>2. Activate it</b></summary>

macOS/Linux:
```bash
source .venv/bin/activate
```

Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

</details>

<details>
<summary><b>3. Install dependencies</b></summary>

```bash
pip install -r requirements.txt
```

</details>

<details>
<summary><b>4. Run the app</b></summary>

```bash
streamlit run app/Home.py
```

</details>

---

## Data Source

Player and team statistics are scraped from FIFA's official 2026 World Cup stats pages (see `scraper/`). The scraping and cleaning pipeline is still in progress — the app currently runs on internally-consistent placeholder data (generated to match the real schema exactly) so development isn't blocked on data delivery. No app code changes are required once real data lands, provided column names stay unchanged.

## Methodology

- **Per-90 normalization** — scales counting stats (goals, assists) to a standard 90 minutes, so players with different amounts of playing time can be fairly compared
- **Z-scores** — measure how far above/below average a player's stat is, calculated against their own position group rather than the full player pool
- **Impact Score** — a composite metric averaging a player's z-scores across a small set of stats relevant to their specific position (e.g. goals/assists/shots for forwards, saves/clean sheets for goalkeepers)
- **Team comparison** — teams are scored across six core stats, one point each; ties are broken by fewest combined cards, mirroring real-world fair-play tiebreak rules

---

## Contributors

| Role | Contributor |
|---|---|
| Streamlit application (pages, filters, metrics, charts) | Ahmad |
| Data scraping and cleaning | Hiba |

---

<div align="center">
<sub>Built for the FIFA 2026 Player Stats Dashboard project.</sub>
</div>
