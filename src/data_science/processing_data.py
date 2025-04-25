import pandas as pd
import numpy as np
import re

df = pd.read_csv("../utils_/hata.csv")

def clean_data(data_frame):
    print("\nHandling Missing Data...")
    data_frame.replace({'—': np.nan, 'N/A': np.nan, '': np.nan}, inplace=True)
    data_frame.dropna(subset=["Price"], inplace=True)
    data_frame.reset_index(drop=True, inplace=True)

    print(f"Cleaned Data: {len(data_frame)} rows remaining.")
    return data_frame

df = clean_data(df)

def convert_columns(df):
    print("Converting Columns...")
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df['Price'] = df['Price'].str.replace('[$,₽/мес. ]', '', regex=True).replace('', np.nan).astype(float)
    print("Data Cleaning Complete!")
    return df

df = convert_columns(df)
df.to_csv("../utils_/hata.csv", index=False)