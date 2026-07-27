import pandas as pd
import streamlit as st

def load_clean_data():
    df = pd.read_csv("data/processed/players_clean.csv")
    return df

def load_css(path="assets/style.css"):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

