"""
utils.py
All the browser-automation and parsing helper functions used by
scrape_players.py. Kept separate so scrape_players.py can stay a short,
readable "what happens" script, while the "how it happens" details 
including all the bot-detection/timing/click workarounds discovered during
debugging  live here.
"""
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
def start_browser(headless: bool = True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,1000")
    options.page_load_strategy = "eager"
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
    )
    return driver
def dismiss_cookie_banner(driver):
    possible_button_ids = [
        "onetrust-accept-btn-handler",
        "onetrust-close-btn-container",
    ]
    for button_id in possible_button_ids:
        try:
            btn = driver.find_element(By.ID, button_id)
            btn.click()
            time.sleep(1)
            return
        except Exception:
            continue  
def wait_for_player_data(driver, timeout: int = 25):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, "main-text"))
    )
def click_tab(driver, tab_name: str):
    driver.switch_to.default_content()
    candidates = driver.find_elements(By.CLASS_NAME, "filter-chip__label")
    for el in candidates:
        if el.text.strip() == tab_name:
            driver.execute_script("arguments[0].click();", el)
            wait_for_player_data(driver, timeout=15)
            time.sleep(1.5)
            return
    raise Exception(f"Tab '{tab_name}' not found among filter-chip__label elements")
def scroll_to_load_all_rows(driver, pause: float = 1.0, max_attempts: int = 40):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(max_attempts):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  
        last_height = new_height
def scrape_current_tab(driver) -> pd.DataFrame:
    driver.switch_to.default_content()
    soup = BeautifulSoup(driver.page_source, "html.parser")
    header_cells = soup.select("th")
    headers = [th.get_text(strip=True) for th in header_cells]
    rows_data = []
    table_rows = soup.select("tbody tr")  
    for row in table_rows:
        name_el = row.select_one("div.main-text")
        if not name_el:
            continue  
        player_name = name_el.get_text(strip=True)
        team_code_el = row.select_one("span.dsk-description")
        position_el = row.select_one("span.dsk-description-info")
        team_code = team_code_el.get_text(strip=True) if team_code_el else None
        position_raw = position_el.get_text(strip=True) if position_el else None
        value_cells = row.select("td.scrollable-column span.value")
        stat_values = [cell.get_text(strip=True) for cell in value_cells]
        row_dict = {
            "player_name": player_name,
            "team_code": team_code,
            "position_raw": position_raw,
        }
        stat_headers = headers[-len(stat_values):] if stat_values else []
        for header, value in zip(stat_headers, stat_values):
            row_dict[header] = value
        rows_data.append(row_dict)
    return pd.DataFrame(rows_data)
