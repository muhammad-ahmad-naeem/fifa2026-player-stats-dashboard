import streamlit as st
from cleaning import load_clean_data

st.set_page_config(page_title="FIFA 2026 Dashboard", layout="wide")
st.title("⚽ FIFA 2026 Player Stats Dashboard")

df = load_clean_data()

col1,col2,col3=st.columns(3)
col1.metric("Total Players: ", len(df))
col2.metric("Total Teams: ", df["team"].nunique())
col3.metric("Total Goals: ", int(df["goals"].sum()))

st.subheader("Player Data")
st.dataframe(df)
