import pandas as pd
import streamlit as st

def load_clean_data():
    df = pd.read_csv("data/processed/players_clean.csv")
    return df

def load_team_summary():
    df = pd.read_csv("data/processed/team_summary.csv")
    return df
