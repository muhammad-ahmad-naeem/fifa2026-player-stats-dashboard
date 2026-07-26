# FIFA 2026 Player Stats Dashboard

A Streamlit dashboard for exploring FIFA 2026 player and team statistics.

## Project Structure
- `data/` — raw scraped data and cleaned/processed datasets
- `scraper/` — scripts to pull player data
- `notebooks/` — EDA and prototyping
- `app/` — Streamlit application (pages, cleaning, metrics, charts)
- `assets/` — branding and CSS

## Setup
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/Home.py
```

## Data Source
_TODO: describe where the data comes from_

## Methodology
_TODO: describe cleaning/metric logic_