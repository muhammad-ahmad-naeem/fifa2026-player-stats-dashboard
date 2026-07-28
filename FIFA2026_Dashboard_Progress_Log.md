# FIFA 2026 Player Stats Dashboard — Progress Log

*Living project history and design-decision record. Update this file whenever a phase or major milestone is completed.*

Last updated: **Phase 4 completion**

---

## 1. Project Summary

A Streamlit-based interactive dashboard for exploring FIFA 2026 player and team statistics. Users can browse teams, filter by player position, drill into individual players, and now compare two teams head-to-head with statistically grounded results.

**Team roles:**
- Streamlit application (pages, filters, metrics, charts) — this document's author
- Data scraping and cleaning — Hiba

---

## 2. Tech Stack

| Component | Tool |
|---|---|
| Frontend / App Framework | Streamlit |
| Data Handling | pandas |
| Statistical Calculations | NumPy |
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
│   └── processed/
│       ├── players_clean.csv        # player-level data (currently placeholder)
│       └── team_summary.csv         # team-level aggregates (now in active use)
│
├── scraper/                         # scraping scripts (Hiba) — not yet started
├── notebooks/                       # EDA / cleaning development (Hiba)
│
├── app/
│   ├── Home.py
│   ├── cleaning.py                  # load_clean_data(), load_team_summary()
│   ├── metrics.py                   # per_90, z_score, compare_teams, CORE_COMPARISON_STATS
│   ├── charts.py                    # planned (Phase 5)
│   └── pages/
│       ├── 1_Player_Explorer.py     # complete
│       ├── 2_Team_Comparison.py     # complete
│       └── 3_Advanced_Stats.py      # planned (Phase 5)
│
├── assets/                          # planned (Phase 6)
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 4. Data

### 4.1 Player-Level Data (`players_clean.csv`)
Placeholder schema, 16 national teams:
```
player_id, player_name, team, nationality, position, age, height_cm, weight_kg,
appearances, minutes_played, goals, assists, shots_on_target, pass_accuracy_pct,
tackles, saves, clean_sheets, yellow_cards, red_cards, market_value_million_eur
```

### 4.2 Team-Level Data (`team_summary.csv`) — **new in Phase 4**
One row per team (16 rows), aggregated from player-level data:
```
team, total_players, total_goals, total_assists, total_shots_on_target,
total_tackles, total_saves, total_clean_sheets, avg_pass_accuracy_pct,
avg_age, avg_market_value_m, total_yellow_cards, total_red_cards
```

**Status:** currently synthetic placeholder data, generated to match the real schema exactly. **Must be regenerated from real `players_clean.csv` once Hiba delivers scraped data** — no application code changes required, provided column names stay unchanged (same policy as the player-level file).

---

## 5. Features Completed

### 5.1 Data Loading
- `load_clean_data()` — reads player-level CSV, shared across all pages
- `load_team_summary()` — reads team-level CSV, added in Phase 4, follows the same pattern for consistency

### 5.2 Player Explorer Page
Three-level drill-down: Team → Position → Player, with scoped metric cards at each level. (Unchanged from Phase 2 — see original overview doc for full detail.)

### 5.3 Team Comparison Page — **Phase 4, complete**

**Layout:**
1. Team A / Team B selectors, side by side (`st.columns`)
2. Same-team guard — warning shown, rest of page hidden, if both selectors match
3. Head-to-head summary table — totals + averages, formatted to 2 decimal places
4. Winner callout — states the winning team, or reports a draw
5. **Show Advanced Stats** (expander, hidden by default) — full per-stat breakdown of who won each core stat, plus tiebreaker explanation if used
6. **Show Full Player Data** (expander, hidden by default) — raw player rosters for both teams, side by side

**Core comparison logic (`compare_teams()` in `metrics.py`):**
- Compares two teams across `CORE_COMPARISON_STATS`: `total_goals`, `total_assists`, `total_shots_on_target`, `total_tackles`, `total_clean_sheets`, `avg_pass_accuracy_pct`
- Each stat is worth 1 point, equal weighting
- Most points wins outright
- **Tiebreaker:** if points are equal, fewer combined `total_yellow_cards + total_red_cards` wins (mirrors real-world fair-play tiebreak rules)
- If still tied after the tiebreaker → result is `"draw"`, no winner forced
- Returns a structured dictionary (`winner`, `tiebreaker_used`, `stat_breakdown`, both teams' scores) — the page only displays this, no calculation logic lives in the UI layer

### 5.4 Statistical Metrics Layer (`metrics.py`)
- `per_90()` and `z_score()` — unchanged from Phase 3
- `compare_teams()` and `CORE_COMPARISON_STATS` — new in Phase 4

---

## 6. Key Design Decisions

*(Carried over from Phase 2/3, plus new Phase 4 decisions below.)*

- **Separation of concerns** — `cleaning.py` loads only, `metrics.py` calculates only, pages handle only UI/interaction. `compare_teams()` follows this exactly: no Streamlit code inside it.
- **Comparison group scope for z-scores** — calculated across the full position/team pool, not within a single team, to avoid statistically meaningless small-sample comparisons.
- **Graceful handling of missing/zero data** — "played and produced nothing" vs. "did not play" distinction preserved in `avg_pass_accuracy_pct` (averaged only over players with `minutes_played > 0`).

### New in Phase 4:

- **Strictly two teams per comparison, no multi-team view.** Considered a "winner stays on" challenge loop using `st.session_state`, but deliberately dropped it — added complexity and regression risk outweighed the benefit versus manually re-selecting two teams, which already works cleanly.
- **Core comparison stats deliberately curated, not "every column."** Excluded goalkeeper-only stats (`total_saves`) from the win-count, since they unfairly reward/punish teams based on shot-facing volume rather than actual quality. Excluded profile stats (`avg_age`, `avg_height_cm`) since they don't represent footballing performance.
- **`avg_market_value_m` included as a core stat** — reflects overall squad strength/quality, consistent with how real scouting platforms use market value as a team-strength proxy.
- **Cards reserved for tiebreaker only, never a "core win."** Prevents double-counting discipline as both a main stat and the deciding factor.
- **Both totals and averages shown in the summary table** — avoids the "small squad with a high average vs. large squad with a high total" ambiguity being hidden from the user.
- **All detail sections (Advanced Stats, Full Player Data) hidden by default**, using `st.expander()`. Keeps the page clean on first load; user opts into detail rather than being shown everything at once.
- **Full player data pulled from `players_clean.csv`, not `team_summary.csv`** — the aggregated file can't answer "why" a team's numbers look the way they do; only raw rows can.

---

## 7. Known Caveats

- `team_summary.csv` is synthetic placeholder data (not derived from real scraped players). Numbers are internally consistent with each other but not reflective of real FIFA 2026 statistics yet.
- No automated test suite yet for `compare_teams()`, `per_90()`, or `z_score()` — verified so far via manual spot-checks against known matchups (e.g. Brazil vs. Germany).
- Real data pipeline (scraping) has not started as of this update — team comparison and player explorer are both fully decoupled from this dependency and will accept real data with no code changes, provided the schema is unchanged.

---

## 8. Roadmap

**Phase 1 — Foundation** — mostly complete
- [x] Folder structure
- [x] Placeholder data
- [x] Data loading function
- [x] Home page displays data
- [ ] KPI summary row on Home page

**Phase 2 — Player Explorer** — complete

**Phase 3 — Statistical Metrics Layer** — in progress
- [x] Per-90 normalization function
- [x] Z-score comparison function
- [ ] Combined "impact score" metric — *possibly already started, `impact_score` import present in Team Comparison page; needs confirmation*
- [ ] Formal test suite for metric functions

**Phase 4 — Team Comparison Page** — ✅ **complete**
- [x] Team-level aggregation (`team_summary.csv`)
- [x] Two-team comparison view
- [x] Winner logic with tiebreaker
- [x] Advanced stats breakdown (expandable)
- [x] Full player data view (expandable)
- [~] Multi-team comparison — deliberately descoped, not planned

**Phase 5 — Advanced Stats & Visualization** — not started
- [ ] Reusable chart functions (Plotly)
- [ ] Rankings (e.g. top scorers per-90)
- [ ] Correlation analysis (e.g. market value vs. goals)

**Phase 6 — Polish** — not started
- [ ] Branding / stylesheet
- [ ] Layout consistency pass across all pages
- [ ] Swap in real cleaned data
- [ ] Full click-through QA pass

---

## 9. Next Steps

1. Confirm whether `impact_score()` (Phase 3) is already built, or still pending
2. Decide whether to add a formal test suite before starting Phase 5
3. Begin Phase 5 (Advanced Stats & Visualization) — new territory: first use of Plotly in this project
4. Follow up on real data delivery timeline (scraping not yet started)

---

*Prepared as part of the FIFA 2026 Player Stats Dashboard team project.*
