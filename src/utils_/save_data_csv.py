from typing import List

import pandas as pd


def save_to_csv(dict_to_load_df: List, name_file: str) -> None:
    data_frame = pd.DataFrame(dict_to_load_df)
    data_frame.to_csv(name_file, mode="w+", index=False)
