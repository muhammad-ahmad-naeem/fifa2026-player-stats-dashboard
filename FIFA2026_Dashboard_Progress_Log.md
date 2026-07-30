# FIFA 2026 Player Stats Dashboard — Progress Log

*Living project history and design-decision record. Update this file whenever a phase or major milestone is completed.*

Last updated: **Phase 5 completion**

---

## 1. Project Summary

A Streamlit-based interactive dashboard for exploring FIFA 2026 player and team statistics. Users can browse teams, filter by player position, drill into individual players, compare two teams head-to-head, and now explore cross-player rankings (top scorers, top playmakers, best overall impact) with interactive charts.

**Team roles:**
- Streamlit application (pages, filters, metrics, charts) — this document's author
- Data scraping and cleaning — Hiba (scraper pipeline now under active development — see §7)

---

## 2. Tech Stack

| Component | Tool |
|---|---|
| Frontend / App Framework | Streamlit |
| Data Handling | pandas |
| Statistical Calculations | NumPy |
| Charting | Plotly (`plotly.express`) — new in Phase 5 |
| Language | Python 3.14 |
| Version Control | Git / GitHub |
| Environment | Windows, PowerShell, VS Code |

---

## 3. Project Structure

```
fifa2026-player-stats-dashboard/
│
├── data/
│   ├── raw/
│   │   └── players_raw.csv          # new — Hiba's raw scraper output
│   └── processed/
│       ├── clean_data.py            # new — Hiba's cleaning script
│       ├── players_clean.csv        # player-level data (still placeholder — see §7)
│       └── team_summary.csv         # team-level aggregates (still placeholder — see §7)
│
├── scraper/                         # Hiba — actively being built (config, scrape_players, utils)
├── notebooks/                       # EDA / cleaning development (Hiba)
│
├── app/
│   ├── Home.py
│   ├── cleaning.py                  # load_clean_data(), load_team_summary()
│   ├── metrics.py                   # per_90, z_score, impact_score, score_player,
│   │                                 # compare_teams, POSITION_STATS, CORE_COMPARISON_STATS
│   ├── charts.py                    # ranking_bar_chart() — new in Phase 5
│   └── pages/
│       ├── 1_Player_Explorer.py     # complete — refactored in Phase 5 (see §5.4)
│       ├── 2_Team_Comparison.py     # complete
│       └── 3_Advanced_Stats.py      # complete — new in Phase 5
│
├── assets/                          # planned (Phase 6)
├── requirements.txt                 # now includes plotly
├── README.md
└── .gitignore
```

---

## 4. Data

### 4.1 Player-Level Data (`players_clean.csv`)
Still synthetic placeholder data as of this update. Hiba's scraper pipeline (`scraper/`) and cleaning script (`data/processed/clean_data.py`) are now under active development and were merged into `main` this phase — but the actual cleaned CSV output has not yet replaced the placeholder. See §7 (Known Caveats) and §9 (Next Steps).

### 4.2 Team-Level Data (`team_summary.csv`)
Unchanged from Phase 4 — still synthetic placeholder, same regeneration policy (no app code changes required once real data lands, provided column names are unchanged).

---

## 5. Features Completed

### 5.1–5.4 (Phases 1–4)
Unchanged — see prior entries in this log for Data Loading, Player Explorer, Team Comparison, and the original Statistical Metrics Layer.

### 5.5 Advanced Stats & Rankings Page — **Phase 5, complete**

**Layout (`3_Advanced_Stats.py`):**
1. Global minutes-played slider — filters which players are eligible to appear in all three rankings below
2. **Top Scorers** — ranked by `per_90(goals)`, horizontal Plotly bar chart, adjustable top-N (5–25)
3. **Top Playmakers** — ranked by `per_90(assists)`, same chart pattern
4. **Best Overall Impact** — ranked by `score_player()` (Impact Score), cross-position leaderboard, same chart pattern

**Key mechanic:** the minutes-played slider controls *eligibility* to appear in the Best Overall Impact ranking, but each player's z-scores are still computed against the *full* position peer group (not the minutes-filtered subset) — preserving the Phase 2 design decision that peer groups must stay large enough to be statistically meaningful.

### 5.6 Shared Impact Score Function — **Phase 5, complete**

- `score_player(player_row, peer_group_df, position_stats=POSITION_STATS)` added to `metrics.py` — extracts the position-lookup + z-score loop that was previously inline on Player Explorer into a single reusable, Streamlit-free function
- `POSITION_STATS` moved from `1_Player_Explorer.py` into `metrics.py`, alongside `CORE_COMPARISON_STATS`, following the existing "shared constants live next to the calculations that use them" pattern
- `1_Player_Explorer.py` Section 3 refactored to call `score_player()` instead of its own inline loop — both pages now guaranteed to compute Impact Score identically, since they call the same function

### 5.7 Reusable Charting Layer (`charts.py`) — **Phase 5, complete**

- `ranking_bar_chart(ranked_df, name_col, value_col, value_label, top_n)` — one function powering all three Advanced Stats rankings
- Takes an already-sorted dataframe (sorting/filtering stays a page-level concern); function's only job is drawing and top-N slicing
- No Streamlit code inside — pages call `st.plotly_chart()` on the returned figure, same separation-of-concerns pattern as `metrics.py`
- Plotly chosen specifically for built-in hover tooltips; interactivity deliberately kept simple (hover + top-N control, no pan/zoom) — heavier interactivity reserved for future correlation-analysis scatter plots

---

## 6. Key Design Decisions

*(Carried over from Phases 2–4, plus new Phase 5 decisions below.)*

### New in Phase 5:

- **Per-90 rankings only, no raw-count leaderboards.** Raw totals reward playing time over efficiency; per-90 keeps the fairness framing consistent with the rest of the app.
- **Minutes-played slider is global and adjustable**, not a fixed hardcoded threshold — applies uniformly across all three ranking sections rather than three separate filters.
- **Impact Score's peer group is never filtered by the minutes slider**, even though eligibility to appear in the ranking is. Filtering the peer group itself would shrink already-small position pools (e.g. CDMs across 16 teams) and reintroduce the small-sample noise problem the app has avoided since Phase 2.
- **One calculation, two callers.** `score_player()` exists specifically so Player Explorer and Advanced Stats can never silently disagree about a given player's Impact Score — extracted from duplicated inline logic into a single shared function.
- **Chart interactivity deliberately minimal for rankings** (hover + top-N slider only). Reasoning: for a leaderboard, the value of interactivity is inspecting an exact value and controlling list length — pan/zoom adds complexity without adding insight. Reserved for future scatter-plot correlation work, where it's more useful.
- **Plotly over matplotlib for the app layer** — explicitly separate concern from Hiba's matplotlib usage (if any) in her EDA notebooks. App-side interactivity requirements (hover tooltips) were the deciding factor.

---

## 7. Known Caveats

- `players_clean.csv` and `team_summary.csv` are **still synthetic placeholder data** — not yet derived from real scraped players, despite Hiba's scraper pipeline (`scraper/config.py`, `scraper/scrape_players.py`, `scraper/utils.py`) and a new cleaning script (`data/processed/clean_data.py`) landing in `main` this phase via merge. Raw scraper output (`data/raw/players_raw.csv`) is present but not yet the finalized cleaned dataset the app consumes.
- No automated test suite yet for `compare_teams()`, `per_90()`, `z_score()`, `score_player()`, or `ranking_bar_chart()` — still verified via manual spot-checks.
- First multi-contributor merge on this repo completed successfully this phase (Ahmad's `app/` changes + Hiba's `scraper/`/`data/` changes) with no file-level conflicts, due to the clean folder separation between the two contributors' work.

---

## 8. Roadmap

**Phase 1 — Foundation** — mostly complete (unchanged)

**Phase 2 — Player Explorer** — complete

**Phase 3 — Statistical Metrics Layer** — ✅ **complete**
- [x] Per-90 normalization function
- [x] Z-score comparison function
- [x] Combined "impact score" metric — confirmed built and in use (Phase 5 refactored it into `score_player()`, shared across two pages)
- [ ] Formal test suite for metric functions

**Phase 4 — Team Comparison Page** — complete (unchanged)

**Phase 5 — Advanced Stats & Visualization** — ✅ **complete**
- [x] `charts.py` — reusable Plotly ranking bar chart function
- [x] Top Scorers ranking (per-90)
- [x] Top Playmakers ranking (per-90)
- [x] Best Overall Impact ranking (cross-position, via `score_player()`)
- [x] Global minutes-played filter across all rankings
- [x] `POSITION_STATS` and `score_player()` promoted to shared `metrics.py`
- [ ] Correlation analysis (e.g. market value vs. goals) — descoped from Phase 5, candidate for Phase 5b or folded into Phase 6

**Phase 6 — Polish** — not started
- [ ] Branding / stylesheet
- [ ] Layout consistency pass across all pages
- [ ] Swap in real cleaned data (blocked on Hiba's pipeline output)
- [ ] Full click-through QA pass
- [ ] Formal test suite for `metrics.py` functions

---

## 9. Next Steps

1. Confirm whether Hiba's merged scraper pipeline (`scraper/`, `data/processed/clean_data.py`) is functional end-to-end, or still in progress
2. Get a timeline on real `players_clean.csv` / `team_summary.csv` output — this unblocks the "swap in real data" step of Phase 6
3. Decide whether correlation analysis (market value vs. goals, etc.) becomes Phase 5b or gets folded into Phase 6
4. Consider a lightweight test suite for `metrics.py` before further functions are added — now that `score_player()` is shared across two pages, a regression there silently breaks both

---

*Prepared as part of the FIFA 2026 Player Stats Dashboard team project.*
