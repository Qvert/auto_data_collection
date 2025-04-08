import streamlit as st
import pandas as pd


@st.cache_data
def load_data():
    data_frame = pd.read_csv("src/utils_/hata.csv")
    data_frame["Price"] = data_frame["Price"].astype(float)

    return data_frame

df = load_data()
