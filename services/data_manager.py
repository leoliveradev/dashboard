import pandas as pd
import streamlit as st
from pathlib import Path

DATA_PATH = Path("data")

class DataManager:

    @staticmethod
    @st.cache_data
    def load_csv(filename):

        file_path = DATA_PATH / filename

        df = pd.read_csv(
            file_path,
            sep=",",
            encoding="cp1252"
        )

        return df
