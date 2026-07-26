import pandas as pd

def load_clean_data():
    df = pd.read_csv("data/processed/players_clean.csv")
    return(df)




