"""
scrape_players.py:
Main entry point. Visits every tab on FIFA's Player Statistics page,
scrapes each one, merges everything into a single DataFrame keyed by
player name, and saves it as the raw CSV for the cleaning stage.
"""
import os
import pandas as pd
from config import PAGE_URL, TABS, RAW_OUTPUT_DIR, RAW_OUTPUT_FILE
from utils import (
    start_browser,
    dismiss_cookie_banner,
    wait_for_player_data,
    click_tab,
    scroll_to_load_all_rows,
    scrape_current_tab,
)
def scrape_all_tabs(headless: bool = False) -> pd.DataFrame:
    driver = start_browser(headless=headless)
    driver.get(PAGE_URL)
    dismiss_cookie_banner(driver)
    print("Waiting for initial player data to load...")
    wait_for_player_data(driver, timeout=30)  # first load can be slowest

    combined_df = None
    for tab_name in TABS:
        print(f"Scraping tab: {tab_name}")
        try:
            click_tab(driver, tab_name)
        except Exception as e:
            print(f"  Could not click tab '{tab_name}': {e}")
            continue

        scroll_to_load_all_rows(driver)
        tab_df = scrape_current_tab(driver)
        print(f"  Got {len(tab_df)} rows, columns: {list(tab_df.columns)}")
        if "player_name" not in tab_df.columns:
            print(f"  Skipping merge for '{tab_name}' - no player_name column")
            continue

        if combined_df is None:
            combined_df = tab_df
        else:
            safe_tab_name = tab_name.replace(" ", "_")
            combined_df = pd.merge(
                combined_df, tab_df, on="player_name", how="outer",
                suffixes=("", f"_{safe_tab_name}")
            )
    driver.quit()
    return combined_df if combined_df is not None else pd.DataFrame()
if __name__ == "__main__":
    # NOTE: headless=True gets blocked by FIFA's bot detection - confirmed a
    # visible, headless=False browser loads real data reliably, so that's
    # the default here. A Chrome window will pop up and drive itself - don't
    # close it manually, let the script finish.
    df = scrape_all_tabs(headless=False)

    os.makedirs(RAW_OUTPUT_DIR, exist_ok=True)
    df.to_csv(RAW_OUTPUT_FILE, index=False)
    print(f"\nSaved {len(df)} total players to {RAW_OUTPUT_FILE}")
