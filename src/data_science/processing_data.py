import pandas as pd
import numpy as np

df = pd.read_csv("../utils/hata.csv")

def clean_data(data_frame):
    print("\nHandling Missing Data...")

    # Replace invalid values with NaN
    data_frame.replace({'—': np.nan, 'N/A': np.nan, '': np.nan}, inplace=True)

    # Drop rows with missing essential values
    data_frame.dropna(subset=["Price"], inplace=True)
    data_frame.reset_index(drop=True, inplace=True)

    print(f"Cleaned Data: {len(data_frame)} rows remaining.")
    return data_frame


df = clean_data(df)