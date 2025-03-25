import pandas as pd
import numpy as np
import re

df = pd.read_csv("../utils/hata.csv")

def clean_data(data_frame):
    print("\nHandling Missing Data...")
    data_frame.replace({'—': np.nan, 'N/A': np.nan, '': np.nan}, inplace=True)
    data_frame.dropna(subset=["Price"], inplace=True)
    data_frame.reset_index(drop=True, inplace=True)

    print(f"Cleaned Data: {len(data_frame)} rows remaining.")
    return data_frame

df = clean_data(df)

def extract_numeric(value):
    if isinstance(value, str):
        match = re.search(r'\d+', value)  # Find first numeric value
        return float(match.group()) if match else np.nan
    return np.nan


def convert_columns(df):
    print("Converting Columns...")
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df['Price'] = df['Price'].str.replace('[$,₽/мес. ]', '', regex=True).replace('', np.nan).astype(float)
    print("Data Cleaning Complete!")
    return df

df = convert_columns(df)


def show_extreme_listings(df):
    print("\nTop 5 Most Expensive Listings:")
    print(df.nlargest(5, 'Price')["Price"])
    print("\nTop 5 Cheapest Listings:")
    print(df.nsmallest(5, 'Price')["Price"])

show_extreme_listings(df)
